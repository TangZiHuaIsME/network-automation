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

def check_ospf_neighbors(device: dict) -> dict:
    print(f"  Checking OSPF neighbors on {device['name']}...")
    try:
        connection_args = {k: v for k, v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)
        output = connection.send_command("show ip ospf neighbor")
        connection.disconnect()

        neighbors = []
        problematic = []

        for line in output.splitlines():
            if "FULL" in line or "2WAY" in line or "EXSTART" in line:
                parts = line.split()
                neighbor = {
                    "neighbor_id": parts[0],
                    "state": parts[2],
                    "interface": parts[-1],
                }
                neighbors.append(neighbor)
                if "FULL" not in parts[2]:
                    problematic.append(neighbor)

        return {
            "device": device["name"],
            "total_neighbors": len(neighbors),
            "neighbors": neighbors,
            "problematic_neighbors": problematic,
            "status": "healthy" if not problematic else "degraded",
            "checked_at": str(datetime.datetime.now()),
        }
    except Exception as e:
        return {
            "device": device["name"],
            "status": "failed",
            "error": str(e),
        }

def main():
    print(f"\n OSPF Neighbor Check — {datetime.datetime.now()}\n")
    results = []
    for device in DEVICES:
        result = check_ospf_neighbors(device)
        results.append(result)
        icon = "✓" if result["status"] == "healthy" else "✗"
        print(f"  {icon} {result['device']} — {result['status']}")
        print(f"    Total neighbors: {result.get('total_neighbors', 0)}")
        if result.get("problematic_neighbors"):
            print(f"    Problematic: {result['problematic_neighbors']}")

    filename = f"ospf_report_{datetime.date.today()}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Report saved → {filename}")

if __name__ == "__main__":
    main()
