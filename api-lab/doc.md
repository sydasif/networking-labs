# API Lab with Cisco CSR1000v and Arista cEOS

This project demonstrates network device configuration and data retrieval using APIs with [Containerlab](https://containerlab.dev/). The lab includes:

- **Cisco CSR1000v**: A virtual router used for RESTCONF API interactions (configuration and data retrieval).
- **Arista cEOS**: A virtual switch/router, included for a multi-vendor environment, though not directly used in the API scripts in this specific lab.
- **Two Linux hosts**: Not directly used in the API scripts, but typically included for network connectivity testing.

### Nodes:

| Name | Type           | Role                     |
| ---- | -------------- | ------------------------ |
| r1   | Cisco CSR1000v | RESTCONF API target      |
| r2   | Arista cEOS    | Multi-vendor environment |

## 📁 Files

- `lab.clab.yaml` – Containerlab topology file
- `scripts/config_interface.py` – Python script to configure an interface on `r1` using RESTCONF.
- `scripts/get_interface_data.py` – Python script to retrieve interface data from `r1` using RESTCONF.

## ⚙️ Configuration

### Cisco CSR1000v (r1) Initial Configuration

The Cisco CSR1000v will be automatically configured by Containerlab with basic connectivity. For RESTCONF access, ensure the following is configured (usually enabled by default in vrnetlab images):

```
restconf
ip http authentication local
ip http secure-server
username admin privilege 15 secret admin
```

### Arista cEOS (r2) Initial Configuration

The Arista cEOS will be automatically configured by Containerlab with basic connectivity.

## 🚀 How to Run

> Prerequisites: [Containerlab](https://containerlab.dev/) and required images (`vrnetlab/cisco_csr1000v`, `asifsyd/ceos`, `alpine`)

1. Clone this repository:

   ```bash
   git clone <your-repo-url>
   cd api-lab
   ```

2. Deploy the lab:

   ```bash
   sudo containerlab deploy -t lab.clab.yaml
   ```

3. Execute the API scripts:

   ```bash
   python3 scripts/config_interface.py
   python3 scripts/get_interface_data.py
   ```

## 🧪 Testing

After running the `config_interface.py` script, you can verify the configuration on `r1` by logging into its console or by running `get_interface_data.py` and checking the output for the configured Loopback interface.

To access `r1` console:

```bash
sudo containerlab tools netns exec clab-api-lab-r1 bash
# Then inside the container:
vtysh
show running-config interface Loopback0
```

## 🧹 Cleanup

```bash
sudo containerlab destroy -t lab.clab.yaml
```

## 📌 Notes

* The `config_interface.py` script configures `Loopback0` with IP `172.16.1.100/24`.
* The scripts use `verify=False` to disable SSL certificate verification, which is common in lab environments but should not be used in production.
* The `device["host"]` in the Python scripts (`172.20.20.2`) is the management IP assigned by Containerlab to `r1`.

---

## 📎 License

This project is open-sourced for educational use. No official affiliation with Cisco or Arista.
