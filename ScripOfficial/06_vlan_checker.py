import json
import datetime
from netmiko import ConnectHandler

DEVICES = [
    {
        "name": "Core-Switch-01",
        "device_type": "cisco_ios",
        "host": "10.10.20.48",
        "username": "admin",
        "password": "C1sco12345",
    },
]

REQUIRED_VLANS = ["1", "10", "20", "30"]

def get_vlans(device: dict) -> dict:
    print(f"  Checking VLANs on {device['name']}...")
    try:
        connection_args = {k: v for k, v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)
        output = connection.send_command("show vlan brief")
        connection.disconnect()

        vlans_found = []
        for line in output.splitlines():
            parts = line.split()
            if parts and parts[0].isdigit():
                vlans_found.append(parts[0])

        missing = [v for v in REQUIRED_VLANS if v not in vlans_found]

        return {
            "device": device["name"],
            "vlans_found": vlans_found,
            "required_vlans": REQUIRED_VLANS,
            "missing_vlans": missing,
            "status": "compliant" if not missing else "non-compliant",
            "checked_at": str(datetime.datetime.now()),
        }
    except Exception as e:
        return {
            "device": device["name"],
            "status": "failed",
            "error": str(e),
        }

def main():
    print(f"\n VLAN Compliance Check — {datetime.datetime.now()}\n")
    results = []
    for device in DEVICES:
        result = get_vlans(device)
        results.append(result)
        icon = "✓" if result["status"] == "compliant" else "✗"
        print(f"  {icon} {result['device']} — {result['status']}")
        if result.get("missing_vlans"):
            print(f"    Missing VLANs: {result['missing_vlans']}")

    filename = f"vlan_report_{datetime.date.today()}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Report saved → {filename}")

if __name__ == "__main__":
    main()
