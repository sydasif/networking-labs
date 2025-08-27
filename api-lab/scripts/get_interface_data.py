import json
import logging
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Disable SSL warnings for lab use only
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_interface_data(host, port, username, password, interface_name=None):
    """
    Retrieves network interface data using RESTCONF.

    Args:
        host (str): The IP address or hostname of the device.
        port (int): The port number for RESTCONF (e.g., 443).
        username (str): The username for authentication.
        password (str): The password for authentication.
        interface_name (str, optional): The name of a specific interface to retrieve data for.
                                        If None, data for all interfaces will be retrieved.

    Returns:
        dict or None: A dictionary containing the interface data, or None if the request fails.
    """
    logging.info(f"Attempting to retrieve interface data from {host}")

    base_url = f"https://{host}:{port}/restconf/data/ietf-interfaces:interfaces"
    if interface_name:
        url = f"{base_url}/interface={interface_name}"
    else:
        url = base_url

    headers = {"Accept": "application/yang-data+json"}

    try:
        response = requests.get(
            url,
            headers=headers,
            auth=HTTPBasicAuth(username, password),
            verify=False,
            timeout=10,
        )

        if response.status_code == 200:
            logging.info(
                f"✅ Successfully retrieved interface data. Status Code: {response.status_code}"
            )
            return response.json().get("ietf-interfaces:interfaces")
        logging.error(
            f"❌ Failed to retrieve interface data. Status Code: {response.status_code}"
        )
        logging.error(f"Response: {response.text}")
        return None
    except requests.exceptions.ConnectionError as e:
        logging.error(f"❌ Connection error to {host}:{port}: {e}")
        return None
    except requests.exceptions.Timeout:
        logging.error(f"❌ Request timed out for {host}:{port}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ An error occurred during the request: {e}")
        return None


if __name__ == "__main__":
    # Example usage:
    # Device details
    DEVICE_HOST = "172.20.20.2"  # CSR1000v RESTCONF IP
    DEVICE_PORT = 443
    DEVICE_USERNAME = "admin"
    DEVICE_PASSWORD = "admin"

    print("Retrieving data for all interfaces:")
    all_interfaces_data = get_interface_data(
        DEVICE_HOST, DEVICE_PORT, DEVICE_USERNAME, DEVICE_PASSWORD
    )
    if all_interfaces_data:
        pprint(all_interfaces_data)
    else:
        print("Failed to retrieve all interface data.")

    print("\nRetrieving data for Loopback0:")
    loopback_interface_data = get_interface_data(
        DEVICE_HOST,
        DEVICE_PORT,
        DEVICE_USERNAME,
        DEVICE_PASSWORD,
        interface_name="Loopback0",
    )
    if loopback_interface_data:
        pprint(loopback_interface_data)
    else:
        print("Failed to retrieve Loopback0 interface data.")
