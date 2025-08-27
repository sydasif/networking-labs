from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.122.10",
    "username": "admin",  # replace with your actual username
    "password": "admin",  # replace with your password
    # "secret": "cisco",  # enable password
}

snmp_config = [
    "access-list 99 permit 192.168.122.1",  # Host allowed to poll SNMP
    "snmp-server community public RO 99",  # Bind SNMP to ACL
    "snmp-server location Lab",
    "snmp-server contact admin@example.com",
]

try:
    conn = ConnectHandler(**device)
    conn.enable()
    output = conn.send_config_set(snmp_config)
    print("[✓] SNMP config applied:")
    print(output)
    conn.disconnect()
except Exception as e:
    print(f"[!] Connection or configuration failed: {e}")
