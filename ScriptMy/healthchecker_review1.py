import json 
import datetime
from netmiko import ConnectHandler

DEVICES=[
    {
        "name":"cat8v",
        "device_type":"cisco_ios",
        "host":"10.10.20.48",
        "username":"developer",
        "password":"C1sco12345"
    }
]

COMMANDS=[
        "show version",
        "show platform",
        "show ip interface brief",
        "show processes cpu sort",
]

def device_check(device:dict)->dict:
    print(f"check device :{device['name']}({device['host']})")

    try:
        connection_args={k:v for k,v in device.items() if k!= "name"}
        connection = ConnectHandler(**connection_args)

        result={}

        for command in COMMANDS:
            output=connection.send_command(command)
            result[command] = output

        connection.disconnect()

        return {
            "devicename":device['name'],
            "devicehost":device['host'],
            "devicestatus":"reachable",
            "checkat":str(datetime.datetime.now()),
            "result":result,
        }


    except Exception as e:
        return{
            "devicename":device['name'],
            "devicehost":device['host'],
            "devicestatus":"unreachable",
            "checkat":str(datetime.datetime.now()),
            "error":str(e)
        }

def save_report(report:list) -> str:
    filename=f"report_{datetime.date.today()}.txt"

    with open(filename,"w") as f:
        json.dump(report,f,indent=2)
        print(f"save {filename} successfully")
    return filename

def main():
    print(f"checking devices now ")
    result=[]

    for device in DEVICES:
        checkresult=device_check(device)
        result.append(checkresult)
        status="successfully" if checkresult['devicestatus']=="reachable" else "failed"
        print(f"device connect {status}")

    save_report(result)

if __name__ == "__main__":
    main()
