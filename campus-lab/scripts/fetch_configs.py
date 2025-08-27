from nornir import InitNornir

# from nornir.core.exceptions import NornirExecutionError
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

# Map Containerlab platform to NAPALM-supported values
platform_map = {"arista_ceos": "eos", "cisco_iol": "ios"}


def gather_required_facts(task):
    raw_platform = task.host.get("platform")

    # Set NAPALM-compatible platform name
    task.host.platform = platform_map[raw_platform]

    try:
        task.run(task=napalm_get, getters=["facts"])
    except Exception as e:
        print(f"[ERROR] {task.host}: Failed to retrieve facts - {e}")
        raise e


nr = InitNornir(config_file="config.yaml")

# Filter hosts based on supported platforms before running the task
supported_hosts = nr.filter(
    filter_func=lambda host: host.get("platform") in platform_map
)

results = supported_hosts.run(task=gather_required_facts)

# Print all results from the filtered hosts
print_result(results)
