from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth

url = "https://172.20.20.2/restconf/data/ietf-interfaces:interfaces"

headers = {"Accept": "application/yang-data+json"}

# Disable warnings for self-signed certs
requests.packages.urllib3.disable_warnings()

response = requests.get(
    url, headers=headers, auth=HTTPBasicAuth("admin", "admin"), verify=False
)

if response.status_code == 200:
    # print("Interfaces Data:")
    pprint(response.json().get("ietf-interfaces:interfaces"))
else:
    print(f"Request failed with status code {response.status_code}")


# Example output:

# {'interface': [{'description': 'Containerlab management interface',
#                 'enabled': True,
#                 'ietf-ip:ipv4': {'address': [{'ip': '10.0.0.15',
#                                               'netmask': '255.255.255.0'}]},
#                 'ietf-ip:ipv6': {'address': [{'ip': '2001:db8::2',
#                                               'prefix-length': 64}]},
#                 'name': 'GigabitEthernet1',
#                 'type': 'iana-if-type:ethernetCsmacd'},
#                {'enabled': False,
#                 'ietf-ip:ipv4': {},
#                 'ietf-ip:ipv6': {},
#                 'name': 'GigabitEthernet2',
#                 'type': 'iana-if-type:ethernetCsmacd'}]}
