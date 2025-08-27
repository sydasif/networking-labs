"""Configures SNMP on network devices using Nornir and Netmiko."""

import logging

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def configure_snmp(task):
    """
    Configures SNMP on a network device.
    Assumes SNMP configuration commands are available in task.host["snmp_config"].
    """
    logging.info(f"Attempting to configure SNMP on {task.host.name}")

    # Ensure platform is set for Netmiko
    platform_map = {"arista_ceos": "arista_eos", "cisco_iol": "cisco_ios"}
    raw_platform = task.host.get("platform")
    if raw_platform not in platform_map:
        logging.warning(
            f"[SKIPPED] {task.host.name}: Unsupported platform '{raw_platform}' for SNMP configuration."
        )
        return

    task.host.platform = platform_map[raw_platform]

    # SNMP configuration commands - these could also be in a file or Jinja template
    # For this example, we'll assume they are part of the host data if needed,
    # or use a default set for Cisco IOS.
    # The original script had hardcoded SNMP config, so we'll use that as a default
    # for Cisco IOS devices.
    if task.host.platform == "cisco_ios":
        snmp_config = [
            "access-list 99 permit 192.168.122.1",  # Host allowed to poll SNMP
            "snmp-server community public RO 99",  # Bind SNMP to ACL
            "snmp-server location Lab",
            "snmp-server contact admin@example.com",
        ]
    else:
        logging.info(
            f"No specific SNMP configuration defined for {task.host.name} ({task.host.platform}). Skipping."
        )
        return

    try:
        result = task.run(
            task=netmiko_send_config,
            config_commands=snmp_config,
            severity_level=logging.DEBUG,
        )
        logging.info(f"✅ SNMP configuration applied successfully on {task.host.name}")
        print_result(result)
    except Exception as e:
        logging.error(f"❌ Failed to configure SNMP on {task.host.name}: {e}")


def main():
    logging.info("Starting SNMP Configuration....")
    logging.info("=" * 40)
    nr = InitNornir(config_file="config.yaml")

    # Filter to only run on devices that support SNMP configuration (e.g., Cisco IOS)
    # In this lab, RTR, ACCESS1, ACCESS2 are Cisco IOL
    cisco_devices = nr.filter(platform="cisco_iol")

    if cisco_devices.inventory.hosts:
        cisco_devices.run(task=configure_snmp)
    else:
        logging.warning("No Cisco IOL devices found in inventory to configure SNMP.")


if __name__ == "__main__":
    main()
