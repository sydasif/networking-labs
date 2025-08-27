import asyncio

from pysnmp.hlapi.v3arch.asyncio import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    get_cmd,
)


async def run():
    snmp_engine = SnmpEngine()
    ip = "192.168.122.10"
    transport = await UdpTransportTarget.create((ip, 161))

    oids = [
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0)),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysUpTime", 0)),
    ]

    result = await get_cmd(
        snmp_engine, CommunityData("public", mpModel=1), transport, ContextData(), *oids
    )

    error_indication, error_status, error_index, var_binds = result

    if error_indication:
        print(f"[!] Error: {error_indication}")
    elif error_status:
        print(f"[!] SNMP Error: {error_status.prettyPrint()} at index {error_index}")
    else:
        print(f"SNMP Data for {ip}:")
        for var_bind in var_binds:
            print(" = ".join([x.prettyPrint() for x in var_bind]))

    snmp_engine.close_dispatcher()


if __name__ == "__main__":
    asyncio.run(run())
