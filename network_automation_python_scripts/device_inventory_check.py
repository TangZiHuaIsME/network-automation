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
    },

]


def get_detail_info(info:str) -> dict:
    info={
        "model":"unknow",
        "serial":"unknow",
        "version":"unknow",
    }

    for line in info.splitlines():
        parts=line.strip()
        if "Cisco IOS XE Software" in line and "version" in line:
            part=line.split("version")
            if len(parts) > 1:
                info['version']=part[1].strip().split(",")[1]
        if "cisco" in parts.lower() and "processor" in parts.lower():
            info[model]=parts[1]
        if "Processor board ID" in line:
            info['serial']=parts[-1]

    return info

def get_device_info(device:dict) -> dict:
    try:

        connection_args = {k:v for k,v in device.items() if k!= "name"}
        connection = ConnectHandler(**connection_args)

        info_output= connection.send_command("show version")
        host_output= connection.send_command("show running-config | include host")

        connection.disconnect()

        info = get_detail_info(info)
        hostname= host_output.replace("hostname","").strip()

        return{
            "devicename":device['name'],
            "devicehost":device['host'],
            "model":info['model'],
            "hostname": hostname,
            "serial":info['serial'],
            "version":info['version'],
            "checkat":str(datetime.datetime.now()),
            "status":"successfully"
        }

    except Exception as e:
        return{
            "devicename":device['name'],
            "devicehost":device['host'],
            "error":str(e),
            "checkat":str(datetime.datetime.now()),
            "status":"failed",
        }

def main():
    print("device checking ------")
    filename = f"device_inventory_{datetime.date.today()}.json"
    result = []
    for device in DEVICES:
        check_result = get_device_info(device)
        result.append(check_result)
        print(f"run script {check_result}")
    
    with open(filename,"w") as f:
        json.dump(result,f,indent=2)
    print(f"save file in {filename}")

if __name__ == "__main__":
    main()
