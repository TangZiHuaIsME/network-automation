import time
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

POLL_INTERVAL = 60

def get_interface_status(device: dict) -> dict:
    try:
        connection_args = {k: v for k, v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)
        output = connection.send_command("show ip interface brief")
        connection.disconnect()

        interfaces = {}
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 6 and parts[0] != "Interface":
                interfaces[parts[0]] = parts[4]
        return interfaces

    except Exception as e:
        print(f"  ERROR connecting to {device['name']}: {e}")
        return {}

def main():
    print(f"\n Interface Monitor Started — {datetime.datetime.now()}")
    print(f"  Polling every {POLL_INTERVAL} seconds. Press Ctrl+C to stop.\n")

    previous_state = {}

    while True:
        for device in DEVICES:
            current_state = get_interface_status(device)

            for interface, status in current_state.items():
                previous_status = previous_state.get(interface)

                if previous_status is None:
                    print(f"  [INIT] {device['name']} {interface}: {status}")
                elif previous_status == "up" and status != "up":
                    print(f"  [ALERT] {datetime.datetime.now()} — "
                          f"{device['name']} {interface} went DOWN")
                elif previous_status != "up" and status == "up":
                    print(f"  [RECOVERY] {datetime.datetime.now()} — "
                          f"{device['name']} {interface} is back UP")

            previous_state = current_state

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
