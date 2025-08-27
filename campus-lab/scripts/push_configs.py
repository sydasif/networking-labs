"""Pushes configurations to network devices using Nornir and Netmiko."""

import logging
from pathlib import Path

from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Containerlab → Netmiko platform mapping
PLATFORM_MAP = {"arista_ceos": "arista_eos", "cisco_iol": "cisco_ios"}


def push_host_config(task, config_dir="configs"):
    """
    Pushes configuration from a file to a network device.

    Args:
        task (nornir.core.task.Task): The Nornir task object.
        config_dir (str): The directory where configuration files are located.
    """
    raw_platform = task.host.get("platform")

    if raw_platform not in PLATFORM_MAP:
        logging.warning(
            f"[SKIPPED] {task.host.name}: Unsupported platform '{raw_platform}' for configuration push."
        )
        return

    task.host.platform = PLATFORM_MAP[raw_platform]

    # Determine config file extension based on platform
    if task.host.platform == "cisco_ios":
        file_extension = "ios"
    elif task.host.platform == "arista_eos":
        file_extension = "cfg"  # or .conf, .txt
    else:
        logging.warning(
            f"[SKIPPED] {task.host.name}: Unknown file extension for platform '{task.host.platform}'."
        )
        return

    config_file = Path(config_dir) / f"{task.host.name.lower()}.{file_extension}"

    if not config_file.exists():
        logging.warning(
            f"[SKIPPED] {task.host.name}: Config file '{config_file}' not found."
        )
        return

    logging.info(f"Pushing configuration from {config_file} to {task.host.name}")
    try:
        result = task.run(
            task=netmiko_send_config,
            config_file=str(config_file),
            severity_level=logging.DEBUG,
        )
        logging.info(f"✅ Configuration applied successfully on {task.host.name}")
        print_result(result)
    except Exception as e:
        logging.error(f"❌ Failed to push configuration to {task.host.name}: {e}")


def main():
    logging.info("Starting Configuration Push....")
    logging.info("=" * 40)
    nr = InitNornir(config_file="config.yaml")

    # Filter hosts based on supported platforms
    supported_hosts = nr.filter(
        filter_func=lambda host: host.get("platform") in PLATFORM_MAP
    )

    if supported_hosts.inventory.hosts:
        supported_hosts.run(task=push_host_config, config_dir="configs")
    else:
        logging.warning(
            "No supported devices found in inventory for configuration push."
        )


if __name__ == "__main__":
    main()
