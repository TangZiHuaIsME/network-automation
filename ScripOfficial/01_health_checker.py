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

COMMANDS = [
    "show version",
    "show processes cpu",
    "show ip interface brief",
]

def check_device(device: dict) -> dict:
    print(f"  Connecting to {device['name']} ({device['host']})...")
    try:
        connection_args = {k: v for k, v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)
        result = {}
        for command in COMMANDS:
            output = connection.send_command(command)
            result[command] = output
        connection.disconnect()
        return {
            "device": device["name"],
            "device_ip": device["host"],
            "status": "reachable",
            "checked_at": str(datetime.datetime.now()),
            "data": result,
        }
    except Exception as e:
        return {
            "device": device["name"],
            "device_ip": device["host"],
            "status": "unreachable",
            "checked_at": str(datetime.datetime.now()),
            "error": str(e),
        }

def save_report(report: list):
    filename = f"report_{datetime.date.today()}.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n  Report saved → {filename}")

def main():
    print(f"\n Network Health Check — {datetime.datetime.now()}\n")
    report = []
    for device in DEVICES:
        result = check_device(device)
        report.append(result)
        icon = "✓" if result["status"] == "reachable" else "✗"
        print(f"  {icon} {result['device']} — {result['status']}")
    save_report(report)

if __name__ == "__main__":
    main()
