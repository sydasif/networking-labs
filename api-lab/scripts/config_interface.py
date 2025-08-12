import json

import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

# Your simple inputs
ip_address = "172.16.1.100"
netmask = "255.255.255.0"
interface = "Loopback0"

# Device details
device = {
    "host": "172.20.20.2",  # CSR1000v RESTCONF IP
    "port": 443,
    "username": "admin",
    "password": "admin",
}

# Build JSON payload automatically
payload = {
    "ietf-interfaces:interface": {
        "name": interface,
        "description": "Configured by RESTCONF",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {"address": [{"ip": ip_address, "netmask": netmask}]},
    }
}

# Disable SSL warnings (lab use only)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Send RESTCONF request
url = f"https://{device['host']}:{device['port']}/restconf/data/ietf-interfaces:interfaces/interface={interface}"
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json",
}

response = requests.put(
    url,
    data=json.dumps(payload),
    auth=HTTPBasicAuth(device["username"], device["password"]),
    headers=headers,
    verify=False,
)

# Print result
if response.status_code in [200, 201, 204]:
    print(f"✅ Interface {interface} configured successfully.")
else:
    print(f"❌ Failed with status code {response.status_code}")
    print(response.text)
