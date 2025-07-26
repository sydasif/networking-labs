# Router-on-a-Stick with Arista cEOS and Cisco IOL

This project demonstrates a "Router-on-a-Stick" configuration using [Containerlab](https://containerlab.dev/). The lab includes:

- **Arista cEOS**: Acts as the Layer 3 router, performing inter-VLAN routing on a single trunk interface.
- **Cisco IOL switch**: Provides VLAN segmentation and access/trunk ports.
- **Two Linux hosts**: Each connected to a separate VLAN.

### Nodes:

| Name | Type        | Role              |
| ---- | ----------- | ----------------- |
| ceos | Arista cEOS | Router-on-a-Stick |
| sw1  | Cisco IOL   | Layer 2 switch    |
| h1   | Linux Host  | VLAN 10 (Users)   |
| h2   | Linux Host  | VLAN 20 (Servers) |

## 📁 Files

- `topology.clab.yaml` – Containerlab topology file

## ⚙️ Configuration

### Cisco IOL Switch Configuration

```bash
vlan 10
vlan 20
!
interface Ethernet0/1
switchport mode access
switchport access vlan 10
!
interface Ethernet0/2
switchport mode access
switchport access vlan 20
!
interface Ethernet0/3
switchport trunk encapsulation dot1q
switchport mode trunk
!
end
write
```

### Arista cEOS Configuration

```bash
hostname ceos
!
interface Ethernet1
 no switchport
!
interface Ethernet1.10
 encapsulation dot1Q vlan 10
 ip address 192.168.10.1/24
!
interface Ethernet1.20
 encapsulation dot1Q vlan 20
 ip address 192.168.20.1/24
!
ip routing
!
end
write
```

## 🚀 How to Run

> Prerequisites: [Containerlab](https://containerlab.dev/) and required images (`ceos`, `IOL`, `alpine`)

1. Clone this repository:

   ```bash
   git clone <your-repo-url>
   cd router-on-a-stick
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
ping 192.168.20.10  # h2
```

## 🧹 Cleanup

```bash
sudo containerlab destroy -t topology.clab.yaml
```

## 📌 Notes

* Make sure your Cisco IOL image is licensed and accessible by Containerlab.
* This lab demonstrates a common "Router-on-a-Stick" setup where a single router interface handles routing for multiple VLANs.

---

## 📎 License

This project is open-sourced for educational use. No official affiliation with Arista or Cisco.