# Network Automation Toolkit

A practical toolkit for enterprise network operations — built from real-world experience managing 1,000+ device environments.

Covers configuration backup, health checks, device inventory collection, and log analysis across multi-vendor networks using Python and Ansible.

---

## What's Inside

| Folder / File | What it does |
|---|---|
| `network_automation_python_scripts/` | Python scripts using Netmiko & Nornir — device login, config collection, log parsing |
| `network_automation_python_nornir/` | Nornir-based parallel execution across large device inventories |
| `network_automation_playbooks/` | Ansible playbooks for network automation tasks |
| `backup_playbook.yml` | Ansible playbook — automated config backup with timestamped files |
| `health_check_playbook.yml` | Ansible playbook — health check across all devices in inventory |
| `inventory.ini` | Device inventory file |
| `backup/` | Output folder for configuration backups |

---

## Tech Stack

- **Python** — Netmiko, Nornir, NAPALM
- **Ansible** — Playbooks for backup and health checks
- **Protocols** — SSH, NETCONF, REST API
- **Platforms** — Huawei VRP, Cisco IOS-XE

---

## Background

Built and used during 3.5 years of enterprise network operations — originally written to replace manual tasks that took 2–3 hours per shift across environments with 1,000+ network devices.

---

## Author

Eddie Tang (唐梓华) — Network Automation Engineer  
[tangzihua.com](https://www.tangzihua.com) · [LinkedIn](https://linkedin.com/in/eddie-tang-071798418)
