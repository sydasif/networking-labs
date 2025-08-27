# Inter-VLAN Routing with Arista cEOS and Cisco IOL

This project demonstrates a basic inter-VLAN routing setup using [Containerlab](https://containerlab.dev/). The lab includes:

- **Arista cEOS**: Acts as the Layer 3 router performing inter-VLAN routing.
- **Cisco IOL switch**: Provides VLAN segmentation and access/trunk ports.
- **Two Linux hosts**: Each connected to a separate VLAN.

### Nodes:

| Name | Type        | Role              |
| ---- | ----------- | ----------------- |
| ceos | Arista cEOS | Inter-VLAN router |
| sw1  | Cisco IOL   | Layer 2 switch    |
| h1   | Linux Host  | VLAN 10 (Users)   |
| h2   | Linux Host  | VLAN 20 (Servers) |

## 📁 Files

- `topology.clab.yaml` – Containerlab topology file

## ⚙️ Configuration

### Arista cEOS Configuration

```shell
vlan 10
 name USERS
vlan 20
 name SERVERS

interface Vlan10
 ip address 192.168.10.1/24
 no shutdown

interface Vlan20
 ip address 192.168.20.1/24
 no shutdown

interface Ethernet1
 switchport trunk allowed vlan 10,20
 switchport mode trunk
 no shutdown

ip routing
end
write memory
```

### Cisco IOL Switch Configuration

```shell
vlan 10
 name USERS
vlan 20
 name SERVERS

interface Ethernet0/1
 switchport mode access
 switchport access vlan 10
 no shutdown

interface Ethernet0/2
 switchport mode access
 switchport access vlan 20
 no shutdown

interface Ethernet0/3
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan 10,20
 no shutdown

end
write memory
```

## 🚀 How to Run

> Prerequisites: [Containerlab](https://containerlab.dev/) and required images (`ceos`, `IOL`, `alpine`)

1. Clone this repository:

   ```bash
   git clone <your-repo-url>
   cd inter-vlan-routing
   ```

2. Deploy the lab:

   ```bash
   sudo containerlab deploy -t topology.clab.yaml
   ```

3. Access console to configure the IOL switch (manual step):

   ```bash
   ssh admin@sw1
   ```

## 🧪 Testing

Configure hosts inside the containers:

### Test connectivity:

From **h1**:

```bash
ping 192.168.10.1   # cEOS gateway
ping 192.168.20.10  # h2
```

From **h2**:

```bash
ping 192.168.20.1
ping 192.168.10.10
```

## 🧹 Cleanup

```bash
sudo containerlab destroy -t topology.clab.yaml
```

## 📌 Notes

* Make sure your Cisco IOL image is licensed and accessible by Containerlab.
* This lab replicates a common enterprise setup with L2 access and L3 core separation.

---

## 📎 License

This project is open-sourced for educational use. No official affiliation with Arista or Cisco.
