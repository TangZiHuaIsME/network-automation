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

CONFIG_COMMANDS=[
    "ntp server 8.8.8.1",
    "snmp-server community public RO", 
    # "interface GigabitEthernet1",
    # "ip address 1.1.1.1 255.255.255.0",
    # "no shutdown",
]

def get_config_result(device:dict,commands:list) -> dict:
    try:
        connection_args={k:v for k,v in device.items() if k!="name"}
        connection = ConnectHandler(**connection_args)

        output = connection.send_config_set(commands)
        connection.disconnect()

        return {
            "devicename":device['name'],
            "devicehost":device['host'],
            "checkat":str(datetime.datetime.now()),
            "status":"configure successfully",
            "output":output
        }

    except Exception as e:
        return {
            "devicename":device['name'],
            "devicehost":device['host'],
            "checkat":str(datetime.datetime.now()),
            "status":"configure failed",
            "error":str(e)
        }

def main():
    print("configure now  ..........")
    filename = f"{datetime.date.today()}_config_result.json"
    result=[]
    for device in DEVICES:
        check_result = get_config_result(device,CONFIG_COMMANDS)
        result.append(check_result)
        print(f"configure {device['name']} {check_result['status']}")
    
    with open(filename,"w") as f:
        json.dump(result,f,indent=2)
    print(f"save result into {filename}")


if __name__ == "__main__":
    main()