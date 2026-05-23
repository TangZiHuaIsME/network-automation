import json
import datetime
import os
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



def create_fold()->str:
    filename=f"backup/{datetime.date.today()}"
    os.makedirs(filename,exist_ok=True)
    print(f"create filename {filename} successful ...")
    return filename


def backup_config(device:dict,filename:str)->dict:
    try:
        connection_args={k:v for k,v in device.items() if k !="name"}
        connection=ConnectHandler(**connection_args)

        config = connection.send_command("show running-config")
        connection.disconnect()

        name=f"{filename}/{datetime.date.today()}_backup.txt"

        with open(name,"w") as f:
            f.write(config)
        
        return{
            "devicename":device['name'],
            "devicehost":device['host'],
            "status":"reachable",
            "backupat":str(datetime.datetime.now()),
            "config":str(config)
        }
    
    except Exception as e:

        return{
            "devicename":device['name'],
            "devicehost":device['host'],
            "status":"unreachable",
            "backupat":str(datetime.datetime.now()),
            "error":str(e)
        }

def main():

    name=create_fold()

    for device in DEVICES:
        check_result=backup_config(device,name)
        print(f"{check_result}")

if __name__ == "__main__":
    main()