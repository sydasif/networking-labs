from pathlib import Path

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

# Containerlab → Netmiko platform mapping
platform_map = {"arista_ceos": "arista_eos", "cisco_iol": "cisco_ios"}


def push_host_config(task):
    raw_platform = task.host.get("platform")

    # Skip unsupported platforms
    if raw_platform not in platform_map:
        print(f"[SKIPPED] {task.host}: Unsupported platform '{raw_platform}'")
        return

    # Set platform to Netmiko-compatible value
    task.host.platform = platform_map[raw_platform]

    # Build config file path: configs/hostname.ios
    config_file = Path(f"configs/{task.host.name.lower()}.ios")

    if not config_file.exists():
        print(f"[SKIPPED] {task.host}: Config file '{config_file}' not found")
        return

    # Send config from file
    task.run(task=netmiko_send_config, config_file=str(config_file))


nr = InitNornir(config_file="config.yaml")
results = nr.run(task=push_host_config)

print_result(results)
