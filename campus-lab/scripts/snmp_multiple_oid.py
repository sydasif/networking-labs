"""Retrieves multiple SNMP OIDs from network devices using Nornir and pysnmp."""

import asyncio
import logging

from nornir import InitNornir
from nornir.core.task import Result
from pysnmp.hlapi.v3arch.asyncio import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    get_cmd,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def snmp_get_multiple_oids_task(task, oids, community="public"):
    """
    Nornir task to perform an SNMP GET operation for multiple OIDs.

    Args:
        task (nornir.core.task.Task): The Nornir task object.
        oids (list): A list of OID strings to retrieve (e.g., ["SNMPv2-MIB,sysDescr,0", "SNMPv2-MIB,sysName,0"]).
        community (str): The SNMP community string.

    Returns:
        nornir.core.task.Result: The result of the SNMP GET operation.
    """
    logging.info(
        f"Attempting SNMP GET for multiple OIDs on {task.host.name} ({task.host.hostname})"
    )
    snmp_engine = SnmpEngine()

    try:
        transport = await UdpTransportTarget.create((task.host.hostname, 161))

        object_types = []
        for oid_str in oids:
            oid_parts = oid_str.split(",")
            if len(oid_parts) == 3:
                object_types.append(
                    ObjectType(
                        ObjectIdentity(
                            oid_parts[0].strip(),
                            oid_parts[1].strip(),
                            int(oid_parts[2].strip()),
                        )
                    )
                )
            else:
                object_types.append(
                    ObjectType(ObjectIdentity(oid_str))
                )  # Assume it's a full OID string

        result = await get_cmd(
            snmp_engine,
            CommunityData(community, mpModel=1),  # SNMP v2c
            transport,
            ContextData(),
            *object_types,
        )

        error_indication, error_status, error_index, var_binds = result

        if error_indication:
            error_message = f"Error: {error_indication}"
            logging.error(f"❌ {task.host.name}: {error_message}")
            return Result(host=task.host, result=error_message, failed=True)
        if error_status:
            error_message = (
                f"SNMP Error: {error_status.prettyPrint()} at index {error_index}"
            )
            logging.error(f"❌ {task.host.name}: {error_message}")
            return Result(host=task.host, result=error_message, failed=True)
        output = "\n".join([
            " = ".join([x.prettyPrint() for x in var_bind]) for var_bind in var_binds
        ])
        logging.info(f"✅ {task.host.name}: SNMP GET successful for multiple OIDs.")
        return Result(host=task.host, result=output)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logging.error(f"❌ {task.host.name}: {error_message}")
        return Result(host=task.host, result=error_message, failed=True)
    finally:
        snmp_engine.close_dispatcher()


async def main_async():
    logging.info("Starting SNMP GET Multiple OIDs Operation....")
    logging.info("=" * 40)
    nr = InitNornir(config_file="config.yaml")

    # Filter to only run on devices where SNMP is expected to be enabled (e.g., Cisco IOL)
    snmp_devices = nr.filter(platform="cisco_iol")

    if snmp_devices.inventory.hosts:
        oids_to_get = [
            "SNMPv2-MIB,sysDescr,0",
            "SNMPv2-MIB,sysName,0",
            "SNMPv2-MIB,sysUpTime,0",
        ]
        result = await snmp_devices.run(
            task=snmp_get_multiple_oids_task, oids=oids_to_get, community="public"
        )
        for host_name, host_result in result.items():
            if host_result.failed:
                logging.error(f"Result for {host_name}: {host_result.result}")
            else:
                logging.info(f"Result for {host_name}:\n{host_result.result}")
    else:
        logging.warning(
            "No Cisco IOL devices found in inventory for SNMP GET Multiple OIDs."
        )


if __name__ == "__main__":
    asyncio.run(main_async())
