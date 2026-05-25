import json 
import datetime
from netmiko import ConnectHandler

DEVICES=[
    {
        "name":"cat8kv",
        "device_type":"cisco_ios",
        "host":"10.10.20.48",
        "username":"developer",
        "password":"C1sco12345",
    }
]

COMMANDS=[
    "show version",
    "show inventory",
    "show process cpu sorted"
]

def check_device(device:dict) -> dict:
    try:
        connection_args = {k:v for k,v in device.items() if k!="name"}
        connection = ConnectHandler(**connection_args)
        device_info={}

        for command in COMMANDS:
            output=connection.send_command(command)
            device_info[command]=output
        connection.disconnect()

        return {
            "device name":device['name'],
            "device host":device['host'],
            "check at": str(datetime.datetime.now()),
            "check_result":device_info,
            "status":"checked successfully",
        }

    except Exception as e:
        return {
            "device name":device['name'],
            "device host":device['host'],
            "check at": str(datetime.datetime.now()),
            "error":str(e),
            "status":"checked failed",
        }

def save_report(report:list) -> str:
    filename=f"{datetime.date.today()}_report.json"
    with open(filename,"w") as f:
        json.dump(report,f,indent=2)
    print(f"save report {filename} successfully")
    return filename

def main():
    report=[]

    for device in DEVICES:
        check_result = check_device(device)
        report.append(check_result)
        print(f" {device['name']} is {check_result['status']}")
    filename=save_report(report)

    print(f"save file into {filename}")


if __name__ == "__main__":
    main()