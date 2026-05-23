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

def parse_version(output: str) -> dict:
    info = {"model": "unknown", "version": "unknown", "serial": "unknown"}
    for line in output.splitlines():
        line = line.strip()
        if "Cisco IOS XE Software" in line:
            parts = line.split("Version")
            if len(parts) > 1:
                info["version"] = parts[1].strip().split(",")[0]
        if "cisco" in line.lower() and "processor" in line.lower():
            info["model"] = line.split()[1]
        if "Processor board ID" in line:
            info["serial"] = line.split()[-1]
    return info

def collect_inventory(device: dict) -> dict:
    print(f"  Collecting inventory from {device['name']}...")
    try:
        connection_args = {k: v for k, v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)
        version_output = connection.send_command("show version")
        hostname_output = connection.send_command("show running-config | include hostname")
        connection.disconnect()

        parsed = parse_version(version_output)
        hostname = hostname_output.replace("hostname", "").strip()

        return {
            "device": device["name"],
            "ip": device["host"],
            "hostname": hostname,
            "model": parsed["model"],
            "version": parsed["version"],
            "serial": parsed["serial"],
            "collected_at": str(datetime.datetime.now()),
            "status": "success",
        }
    except Exception as e:
        return {
            "device": device["name"],
            "ip": device["host"],
            "status": "failed",
            "error": str(e),
        }

def main():
    print(f"\n Device Inventory — {datetime.datetime.now()}\n")
    inventory = []
    for device in DEVICES:
        result = collect_inventory(device)
        inventory.append(result)
        icon = "✓" if result["status"] == "success" else "✗"
        print(f"  {icon} {result['device']} — {result.get('model', 'failed')}")

    filename = f"inventory_{datetime.date.today()}.json"
    with open(filename, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"\n  Inventory saved → {filename}")

if __name__ == "__main__":
    main()
