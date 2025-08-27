"""Tests connectivity to ContainerLab devices and retrieves interface status."""

import os
import sys

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result


def test_icmp_reachability(nr):
    """Tests ICMP connectivity to all hosts in the Nornir inventory."""
    print("Testing ICMP connectivity to all hosts in inventory")
    reachable_hosts = []

    for host in nr.inventory.hosts.values():
        response = os.system(f"ping -c 1 -W 2 {host.hostname} > /dev/null 2>&1")

        if response == 0:
            reachable_hosts.append(host.name)
            print(f"{host.name} ({host.hostname}): Reachable")
        else:
            print(f"{host.name} ({host.hostname}): Unreachable")

    return reachable_hosts


def get_device_interface_status(task):
    """Retrieves and prints interface status for a network device."""
    # Containerlab → Netmiko platform mapping
    platform_map = {"arista_ceos": "arista_eos", "cisco_iol": "cisco_ios"}
    raw_platform = task.host.get("platform")

    # Skip unsupported platforms
    if raw_platform not in platform_map:
        print(f"[SKIPPED] {task.host}: Unsupported platform '{raw_platform}'")
        return

    # Set platform to Netmiko-compatible value
    task.host.platform = platform_map[raw_platform]

    # Test Basic connectivity
    result = task.run(
        task=netmiko_send_command,
        command_string="show ip interface brief",
        use_textfsm=False,
    )
    print_result(result)


if __name__ == "__main__":
    print("Connectivity Validation Test....")
    print("=" * 40)
    nr = InitNornir(config_file="config.yaml")

    # test ICMP connectivity
    icmp_reachable_hosts = test_icmp_reachability(nr)

    if icmp_reachable_hosts:
        print(f"\nFound {len(icmp_reachable_hosts)} reachable devices")
        # test device management connectivity
        nr.run(task=get_device_interface_status)
    else:
        print("No devices reachable - check routing configuration")
        sys.exit(1)
