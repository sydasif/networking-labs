"""Tests connectivity to ContainerLab devices and retrieves interface status."""

import logging
import os
import sys

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def test_icmp_reachability(nr):
    """Tests ICMP connectivity to all hosts in the Nornir inventory."""
    logging.info("Testing ICMP connectivity to all hosts in inventory")
    reachable_hosts = []

    for host in nr.inventory.hosts.values():
        # Using os.system for ping for simplicity in a lab environment
        response = os.system(f"ping -c 1 -W 2 {host.hostname} > /dev/null 2>&1")

        if response == 0:
            reachable_hosts.append(host.name)
            logging.info(f"{host.name} ({host.hostname}): Reachable")
        else:
            logging.warning(f"{host.name} ({host.hostname}): Unreachable")

    return reachable_hosts


def get_device_interface_status(task):
    """Retrieves and prints interface status for a network device."""
    # Containerlab → Netmiko platform mapping
    platform_map = {"arista_ceos": "arista_eos", "cisco_iol": "cisco_ios"}
    raw_platform = task.host.get("platform")

    # Skip unsupported platforms
    if raw_platform not in platform_map:
        logging.warning(
            f"[SKIPPED] {task.host.name}: Unsupported platform '{raw_platform}'"
        )
        return

    # Set platform to Netmiko-compatible value
    task.host.platform = platform_map[raw_platform]

    logging.info(f"Retrieving interface status for {task.host.name}")
    try:
        result = task.run(
            task=netmiko_send_command,
            command_string="show ip interface brief",
            use_textfsm=False,
            severity_level=logging.DEBUG,  # Set severity for task results
        )
        print_result(result)
    except Exception as e:
        logging.error(f"Error retrieving interface status for {task.host.name}: {e}")


def main():
    logging.info("Starting Connectivity Validation Test....")
    logging.info("=" * 40)
    nr = InitNornir(config_file="config.yaml")

    # test ICMP connectivity
    icmp_reachable_hosts = test_icmp_reachability(nr)

    if icmp_reachable_hosts:
        logging.info(f"Found {len(icmp_reachable_hosts)} reachable devices")
        # Filter Nornir inventory to only include reachable hosts for further tests
        nr_reachable = nr.filter(name=icmp_reachable_hosts)
        # test device management connectivity
        nr_reachable.run(task=get_device_interface_status)
    else:
        logging.error("No devices reachable - check routing configuration")
        sys.exit(1)


if __name__ == "__main__":
    main()
