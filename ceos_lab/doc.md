# Arista cEOS Containerlab Demo: BGP Peering and API Management

This project demonstrates a basic network topology using two Arista cEOS (Containerized Extensible Operating System) nodes within a Containerlab environment. The lab focuses on:

- **BGP Peering**: Establishing an eBGP session between two cEOS routers.
- **Basic Interface Configuration**: Routed interfaces and VLAN access ports.
- **API Management**: Enabling HTTP-commands, gNMI, and NETCONF for network programmability.

## Topology

The topology consists of two Arista cEOS nodes: `core1` and `core2`. They are connected via their `eth1` interfaces, forming a point-to-point link for BGP peering.

### Nodes

| Name  | Type        | Role                                 | Management IP     |
| ----- | ----------- | ------------------------------------ | ----------------- |
| core1 | Arista cEOS | BGP AS 65001, API Management Enabled | `192.168.122.131` |
| core2 | Arista cEOS | BGP AS 65002, API Management Enabled | `192.168.122.130` |

### Links

*   `core1:eth1` (IP: `10.1.1.1/24`) is connected to `core2:eth1` (IP: `10.1.1.2/24`).

## 📁 Files

*   `ceos.clab.yaml`: Defines the Containerlab topology.
*   `configs/core1-startup-config.cfg`: Startup configuration for `core1`.
*   `configs/core2-startup-config.cfg`: Startup configuration for `core2`.
*   `doc.md`: This documentation file.

## ⚙️ Configuration Highlights

### CORE1 (Arista cEOS)
- **Hostname**: `CORE1`
- **Interfaces**:
  - `Ethernet1`: `10.1.1.1/24` (connected to `core2`)
  - `Ethernet2`: `switchport access vlan 17`
  - `Loopback0`: `10.254.100.1/32`
  - `Vlan17`: `172.17.0.1/24`
- **Routing**:
  - BGP AS `65001`, neighbor `10.1.1.2` (core2 AS `65002`).
  - Redistributes connected routes into BGP.
  - Default route `0.0.0.0/0` via `192.168.122.1`.
- **API Management**: HTTP-commands, gNMI, NETCONF enabled.

### CORE2 (Arista cEOS)
- **Hostname**: `CORE2`
- **Interfaces**:
  - `Ethernet1`: `10.1.1.2/24` (connected to `core1`)
  - `Ethernet2`: `switchport access vlan 18`
  - `Loopback0`: `10.254.100.2/32`
  - `Vlan18`: `172.18.0.1/24`
- **Routing**:
  - BGP AS `65002`, neighbor `10.1.1.1` (core1 AS `65001`).
  - Redistributes connected routes into BGP.
  - Default route `0.0.0.0/0` via `192.168.122.1`.
- **API Management**: HTTP-commands, gNMI, NETCONF enabled.

## 🚀 How to Run

> Prerequisites: [Containerlab](https://containerlab.dev/) and required `ceos` image (`ceos:4.32.0F`).

1.  **Clone this repository:**
    ```bash
    git clone <repository-url>
    cd ceos_lab
    ```
2.  **Deploy the lab:**
    ```bash
    sudo containerlab deploy -t ceos.clab.yaml
    ```
3.  **Access the nodes:**
    You can access the nodes via SSH using their management IP addresses (e.g., `ssh admin@192.168.122.131` for core1).

## 🧪 Testing

1.  **Verify BGP Peering**:
    Log into `core1` or `core2` and check BGP neighbor status:
    ```bash
    show ip bgp summary
    ```
    You should see the BGP session established.

2.  **Verify Reachability**:
    From `core1`, ping `core2`'s loopback or Ethernet1 interface:
    ```bash
    ping 10.254.100.2
    ping 10.1.1.2
    ```
    From `core2`, ping `core1`'s loopback or Ethernet1 interface:
    ```bash
    ping 10.254.100.1
    ping 10.1.1.1
    ```

3.  **Verify API Management**:
    You can use `curl` or a Python script to interact with the enabled APIs (HTTP-commands, gNMI, NETCONF) on the management IPs.

## 🧹 Cleanup

```bash
sudo containerlab destroy -t ceos.clab.yaml
```

## 📌 Notes

*   The lab uses `virbr0` for the management network.
*   The `ceos` image used is `ceos:4.32.0F`.
*   Default credentials for cEOS are `admin/admin`.

---

## 📎 License

This project is open-sourced for educational use. No official affiliation with Arista.
