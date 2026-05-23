import os
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

def create_backup_folder() -> str:
    folder = f"backups/{datetime.date.today()}"
    os.makedirs(folder, exist_ok=True)
    return folder

def backup_device(device: dict, folder: str) -> dict:
    print(f"  Backing up {device['name']} ({device['host']})...")
    try:
        connection_args = {k: v for k, v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)
        config = connection.send_command("show running-config")
        connection.disconnect()

        filename = f"{folder}/{device['name']}_{datetime.date.today()}.txt"
        with open(filename, "w") as f:
            f.write(config)

        return {
            "device": device["name"],
            "status": "success",
            "file": filename,
            "backed_up_at": str(datetime.datetime.now()),
        }
    except Exception as e:
        return {
            "device": device["name"],
            "status": "failed",
            "error": str(e),
            "backed_up_at": str(datetime.datetime.now()),
        }

def main():
    print(f"\n Config Backup — {datetime.datetime.now()}\n")
    folder = create_backup_folder()
    results = []
    for device in DEVICES:
        result = backup_device(device, folder)
        results.append(result)
        icon = "✓" if result["status"] == "success" else "✗"
        print(f"  {icon} {result['device']} — {result['status']}")
    print(f"\n  All backups saved → {folder}/")

if __name__ == "__main__":
    main()
