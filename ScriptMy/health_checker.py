import json
import datetime
from netmiko import ConnectHandler


DEVICES=[
    {
        "name":"cat8k",
        "device_type":"cisco_ios",
        "host":"10.10.20.48",
        "username":"developer",
        "password":"C1sco12345",
    }
]

COMMANDS=[
    "show version",
    "show platform",
    "show ip interface brief",
]

def check_device(device: dict)->dict:
    print(f"connectiong device {device['name']}({device['host']})")

    try:

        connection_args={k:v for k,v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)

        result={}
        for command in COMMANDS :
            output = connection.send_command(command)
            result[command] = output
        
        connection.disconnect()

        return{
            "devicename":device['name'],
            "deviceip":device['host'],
            "status":"reachable",
            "checkat":str(datetime.datetime.now()),
            "check_result":str(result)
        }
    
    except Exception as e:
        return{
            "devicename":device['name'],
            "deviceip":device['host'],
            "status":"unreachable",
            "checkat":str(datetime.datetime.now()),
            "erro":str(e)
        }
def save_report(report:list):
    filename=(f"report_{datetime.date.today()}.json")
    with open(filename,"w") as f:
        json.dump(report,f,indent=2)
    print(f"save {filename} successfully")

def main():

    print(f"start to check device .....")
    result=[]

    for device in DEVICES:
        output=check_device(device)
        result.append(output)
        icon="successfully" if output["status"] == "reachable" else "failed"
        print(f"conneting device {output["devicename"]} {icon}")
    
    save_report(result)

if __name__ == "__main__":
    main()





    
