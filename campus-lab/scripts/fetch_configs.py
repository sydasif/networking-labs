"""Gathers configurations and facts from network devices using Nornir and NAPALM."""

import logging
import os

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Map Containerlab platform to NAPALM-supported values
PLATFORM_MAP = {"arista_ceos": "eos", "cisco_iol": "ios"}


def gather_device_data(
    task, getters=None, save_to_file=False, output_dir="fetched_configs"
):
    """
    Gathers specified data (facts, config, etc.) from a network device using NAPALM.

    Args:
        task (nornir.core.task.Task): The Nornir task object.
        getters (list, optional): A list of NAPALM getters to use (e.g., ["facts", "config"]).
                                  Defaults to ["facts"] if None.
        save_to_file (bool): If True, saves the fetched configuration to a file.
        output_dir (str): Directory to save fetched configurations.
    """
    if getters is None:
        getters = ["facts"]

    raw_platform = task.host.get("platform")

    if raw_platform not in PLATFORM_MAP:
        logging.warning(
            f"[SKIPPED] {task.host.name}: Unsupported platform '{raw_platform}' for NAPALM."
        )
        return

    # Set NAPALM-compatible platform name
    task.host.platform = PLATFORM_MAP[raw_platform]

    logging.info(f"Gathering {', '.join(getters)} from {task.host.name}")
    try:
        result = task.run(
            task=napalm_get, getters=getters, severity_level=logging.DEBUG
        )
        print_result(result)

        if save_to_file and "config" in getters:
            # Assuming 'config' getter returns a dictionary with 'running' key
            config_data = result[0].result.get("config", {}).get("running")
            if config_data:
                os.makedirs(output_dir, exist_ok=True)
                filename = os.path.join(output_dir, f"{task.host.name}.cfg")
                with open(filename, "w") as f:
                    f.write(config_data)
                logging.info(
                    f"✅ Saved configuration for {task.host.name} to {filename}"
                )
            else:
                logging.warning(
                    f"No running configuration found for {task.host.name} to save."
                )

    except Exception as e:
        logging.error(f"❌ {task.host.name}: Failed to retrieve data - {e}")


def main():
    logging.info("Starting Configuration and Fact Gathering....")
    logging.info("=" * 40)
    nr = InitNornir(config_file="config.yaml")

    # Filter hosts based on supported platforms before running the task
    supported_hosts = nr.filter(
        filter_func=lambda host: host.get("platform") in PLATFORM_MAP
    )

    if supported_hosts.inventory.hosts:
        # Example: Gather running configuration and save to files
        logging.info(
            "Gathering running configurations and saving to 'fetched_configs' directory."
        )
        results = supported_hosts.run(
            task=gather_device_data,
            getters=["config"],
            save_to_file=True,
            output_dir="fetched_configs",
        )
        # You can also gather facts:
        # logging.info("\nGathering device facts:")
        # results = supported_hosts.run(task=gather_device_data, getters=["facts"])
    else:
        logging.warning("No supported devices found in inventory for data gathering.")


if __name__ == "__main__":
    main()
