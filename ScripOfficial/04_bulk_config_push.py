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

CONFIG_COMMANDS = [
    "ntp server 8.8.8.8",
    "logging host 192.168.1.100",
    "snmp-server community public RO",
]

def push_config(device: dict, commands: list) -> dict:
    print(f"  Pushing config to {device['name']} ({device['host']})...")
    try:
        connection_args = {k: v for k, v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)
        output = connection.send_config_set(commands)
        connection.disconnect()

        return {
            "device": device["name"],
            "status": "success",
            "commands_pushed": len(commands),
            "output": output,
            "pushed_at": str(datetime.datetime.now()),
        }
    except Exception as e:
        return {
            "device": device["name"],
            "status": "failed",
            "error": str(e),
            "pushed_at": str(datetime.datetime.now()),
        }

def main():
    print(f"\n Bulk Config Push — {datetime.datetime.now()}\n")
    print(f"  Commands: {len(CONFIG_COMMANDS)} | Devices: {len(DEVICES)}\n")

    results = []
    for device in DEVICES:
        result = push_config(device, CONFIG_COMMANDS)
        results.append(result)
        icon = "✓" if result["status"] == "success" else "✗"
        print(f"  {icon} {result['device']} — {result['status']}")

    filename = f"push_report_{datetime.date.today()}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Report saved → {filename}")

if __name__ == "__main__":
    main()
