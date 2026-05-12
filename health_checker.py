import json
import datetime
from netmiko import ConnectHandler

DEVICES=[
    {
        "name":"CORE-ROUTER-01",
        "device_type":"huawei",
        "host":"192.168.1.1",
        "username":"admin",
        "password":"password",
    },
    {
        "name":"Core-Switch-01",
        "device_type":"huawei",
        "host":"192.168.1.8",
        "username":"admin",
        "password":"password",
    },
    {
        "name":"Core-Switch-01",
        "device_type":"huawei",
        "host":"192.168.1.2",
        "username":"admin",
        "password":"password",
    },
]

COMMANDS=[
    "display cpu-usage",
    "display version",
    "display interface brief",
]

def check_device(device:dict) -> dict:
    print(f"connecting to {device['name']}({device['host']})......")

    try:
        connection_args={k:v for k,v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_arg)

        result={}

        for commend in COMMANDS:
            output = connection.send_command(commend)
            result[commend] = input
        
        connection.disconnect()

        return{
            "device":device["name"],
            "device_ip":device["host"],
            "checkat":str(datetime.datetime.now()),
            "data":result,
            "status":"reachable"
        }
    except Exception as e:
        return{
            "device":device["name"],
            "device_ip":device["host"],
            "checkat":str(datetime.datetime.now()),
            "error":str(e),
            "status":"unreachable"
        }
def save_report(report:list):
    filename=f"TheReport_{datetime.date.today()}.json"
    with open(filename,"w") as f :
        json.dump(report,f,indent=2)
    print(f"\n save {filename} successfully")

def main():
    print(f"\n start to check devices ")
    result=[]

    for device in DEVICES:
        check_result=check_device(device)
        result.append(check_result)
        icon= "Connect Successfuly" if check_result['status'] == "reachable" else "Connect failed"
        print(icon + f"\n {device['name']} status: {check_result['status']}")
    save_report(result)

if __name__ == "__main__":
    main()

