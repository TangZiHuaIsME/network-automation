import json
import datetime
from netmiko import ConnectHandler

DEVICES=[
    {
        "name":"CORE",
        "device_type":"cisco_ios",
        "host":"ip",
        "username":"developer",
        "password":"password",
    },

]

COMMANDS=[
    "show ip interface brief | include 2",
    "show version | include virtual",
    "show platform",
    "show processes cpu sorted",
    "show memory statistics",
]



def check_device(device:dict) -> dict:
    print(f"connecting to {device['name']}({device['host']})......")

    try:
        connection_args={k:v for k,v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)

        result={}

        for commend in COMMANDS:
            output = connection.send_command(commend)
            result[commend] = output
        
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

