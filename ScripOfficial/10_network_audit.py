import json
import datetime
from netmiko import ConnectHandler

DEVICES = [
    {
        "name": "Core-Router-01",
        "device_type": "cisco_ios",
        "host": "10.10.20.48",
        "username": "admin",
        "password": "C1sco12345",
    },
]

def run_full_audit(device: dict) -> dict:
    print(f"\n  Auditing {device['name']} ({device['host']})...")
    audit = {
        "device": device["name"],
        "ip": device["host"],
        "audited_at": str(datetime.datetime.now()),
        "checks": {}
    }

    try:
        connection_args = {k: v for k, v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)

        checks = {
            "reachability":   "show ip interface brief",
            "cpu":            "show processes cpu | include CPU",
            "memory":         "show processes memory | include Processor",
            "ospf_neighbors": "show ip ospf neighbor",
            "hostname":       "show running-config | include hostname",
        }

        for check_name, command in checks.items():
            output = connection.send_command(command)
            audit["checks"][check_name] = {
                "command": command,
                "output": output,
                "collected_at": str(datetime.datetime.now()),
            }

        connection.disconnect()
        audit["status"] = "complete"

    except Exception as e:
        audit["status"] = "failed"
        audit["error"] = str(e)

    return audit

def main():
    print(f"\n Full Network Audit — {datetime.datetime.now()}")
    print(f"  Devices: {len(DEVICES)}\n")

    full_report = {
        "audit_date": str(datetime.date.today()),
        "generated_at": str(datetime.datetime.now()),
        "total_devices": len(DEVICES),
        "results": []
    }

    for device in DEVICES:
        result = run_full_audit(device)
        full_report["results"].append(result)
        icon = "✓" if result["status"] == "complete" else "✗"
        print(f"  {icon} {result['device']} — {result['status']}")

    filename = f"full_audit_{datetime.date.today()}.json"
    with open(filename, "w") as f:
        json.dump(full_report, f, indent=2)

    print(f"\n  Full audit saved → {filename}")

if __name__ == "__main__":
    main()
