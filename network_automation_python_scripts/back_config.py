import json
import datetime
from netmiko import ConnectHandler
import os

DEVICES=[
    {
        "name":"cat8kv",
        "device_type":"cisco_ios",
        "host":"10.10.20.48",
        "username":"developer",
        "password":"C1sco12345",
    }
]
def make_backup_folder() -> str:
    foldname = f"{datetime.date.today()}_backup"
    os.makedirs(foldname,exist_ok = True)
    return foldname

def back_config(device: dict,foldname: str) -> dict :
    try:

        connection_args = {k:v for k,v in device.items() if k!= "name"}
        connection = ConnectHandler(**connection_args)

        output = connection.send_command("show running-config")
        connection.disconnect()

        filename=f"./{foldname}/back.json"
        with open(filename,"w") as f:
         f.write(output)
        print(f"save backup config into {filename}")
        
        return{
            "devicename":device['name'],
            "devicehost":device['host'],
            "status":"backup config successfully",
            "checkat":str(datetime.datetime.now()),
            "config":output,
        }
    
    except Exception as e :
        return{
            "devicename":device['name'],
            "devicehost":device['host'],
            "status":"backup config failed",
            "checkat":str(datetime.datetime.now()),
            "error":str(e),
        }

def main():
    foldname=make_backup_folder()
    result = []
    for device in DEVICES:
        check_result = back_config(device,foldname)
        result.append(check_result)
        print(f"{device['name']} {check_result['status']}")
    

if __name__ == "__main__":
    main()