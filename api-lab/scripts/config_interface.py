import json
import logging

import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Disable SSL warnings for lab use only
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def configure_interface(
    host, port, username, password, interface_name, ip_address, netmask
):
    """
    Configures a network interface using RESTCONF.

    Args:
        host (str): The IP address or hostname of the device.
        port (int): The port number for RESTCONF (e.g., 443).
        username (str): The username for authentication.
        password (str): The password for authentication.
        interface_name (str): The name of the interface to configure (e.g., "Loopback0").
        ip_address (str): The IP address to assign to the interface.
        netmask (str): The netmask to assign to the interface.
    """
    logging.info(f"Attempting to configure interface {interface_name} on {host}")

    payload = {
        "ietf-interfaces:interface": {
            "name": interface_name,
            "description": "Configured by RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {"address": [{"ip": ip_address, "netmask": netmask}]},
        }
    }

    url = f"https://{host}:{port}/restconf/data/ietf-interfaces:interfaces/interface={interface_name}"
    headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json",
    }

    try:
        response = requests.put(
            url,
            data=json.dumps(payload),
            auth=HTTPBasicAuth(username, password),
            headers=headers,
            verify=False,
            timeout=10,
        )

        if response.status_code in [200, 201, 204]:
            logging.info(
                f"✅ Interface {interface_name} configured successfully. Status Code: {response.status_code}"
            )
            return True
        logging.error(
            f"❌ Failed to configure interface {interface_name}. Status Code: {response.status_code}"
        )
        logging.error(f"Response: {response.text}")
        return False
    except requests.exceptions.ConnectionError as e:
        logging.error(f"❌ Connection error to {host}:{port}: {e}")
        return False
    except requests.exceptions.Timeout:
        logging.error(f"❌ Request timed out for {host}:{port}")
        return False
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ An error occurred during the request: {e}")
        return False


if __name__ == "__main__":
    # Example usage:
    # Device details
    DEVICE_HOST = "172.20.20.2"  # CSR1000v RESTCONF IP
    DEVICE_PORT = 443
    DEVICE_USERNAME = "admin"
    DEVICE_PASSWORD = "admin"

    # Interface details
    INTERFACE_NAME = "Loopback0"
    IP_ADDRESS = "172.16.1.100"
    NETMASK = "255.255.255.0"

    success = configure_interface(
        DEVICE_HOST,
        DEVICE_PORT,
        DEVICE_USERNAME,
        DEVICE_PASSWORD,
        INTERFACE_NAME,
        IP_ADDRESS,
        NETMASK,
    )

    if success:
        print(f"Script finished: Interface {INTERFACE_NAME} configuration successful.")
    else:
        print(f"Script finished: Interface {INTERFACE_NAME} configuration failed.")
