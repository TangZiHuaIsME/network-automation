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

HIGH_USAGE_THRESHOLD = 80

def get_bandwidth_stats(device: dict) -> dict:
    print(f"  Collecting bandwidth stats from {device['name']}...")
    try:
        connection_args = {k: v for k, v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)
        output = connection.send_command("show interfaces")
        connection.disconnect()

        interfaces = []
        current_interface = None

        for line in output.splitlines():
            line = line.strip()
            if line.startswith("GigabitEthernet") or line.startswith("Loopback"):
                current_interface = line.split()[0]
            if "input rate" in line and current_interface:
                parts = line.split()
                try:
                    input_rate = int(parts[0])
                    output_rate = int(parts[4])
                    utilisation = round((input_rate + output_rate) / 2000000, 2)
                    interfaces.append({
                        "interface": current_interface,
                        "input_rate_bps": input_rate,
                        "output_rate_bps": output_rate,
                        "utilisation_mbps": utilisation,
                        "high_usage": utilisation > HIGH_USAGE_THRESHOLD,
                    })
                except (ValueError, IndexError):
                    pass

        high_usage = [i for i in interfaces if i["high_usage"]]

        return {
            "device": device["name"],
            "interfaces": interfaces,
            "high_usage_interfaces": high_usage,
            "status": "alert" if high_usage else "normal",
            "collected_at": str(datetime.datetime.now()),
        }
    except Exception as e:
        return {
            "device": device["name"],
            "status": "failed",
            "error": str(e),
        }

def main():
    print(f"\n Bandwidth Monitor — {datetime.datetime.now()}\n")
    results = []
    for device in DEVICES:
        result = get_bandwidth_stats(device)
        results.append(result)
        icon = "✓" if result["status"] == "normal" else "⚠"
        print(f"  {icon} {result['device']} — {result['status']}")
        if result.get("high_usage_interfaces"):
            for iface in result["high_usage_interfaces"]:
                print(f"    HIGH USAGE: {iface['interface']} — "
                      f"{iface['utilisation_mbps']} Mbps")

    filename = f"bandwidth_report_{datetime.date.today()}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Report saved → {filename}")

if __name__ == "__main__":
    main()
