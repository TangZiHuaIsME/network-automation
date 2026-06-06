import json
import datetime
from netmiko import ConnectHandler


DEVICE=[
    {
        "name":"cat8k",
        "device_type":"cisco_ios",
        "host":"10.10.20.48",
        "username":"developer",
        "password":"C1sco12345"
    }
]

COMMANDS=[
    "ntp server 1.1.1.1",
]

def config_set(device: dict) -> dict:
    try:
        connection_args={k:v for k,v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)

        result = connection.send_config_set(COMMANDS)
        connection.disconnect()

        return{
            "result":result,
            "checkat":str(datetime.datetime.now()),
            "status":"configure successfully",
        }

    
    except Exception as e:
        return{
            "checkat":str(datetime.datetime.now()),
            "status":"configure failed",
            "error":str(e)
        }

def main():
    result=[]

    for device in DEVICE:
        check_result=config_set(device)
        result.append(check_result)
        print(f"configing {device['name']} {check_result['status']}")
        print(f"{check_result}")


if __name__ == "__main__":
    main()