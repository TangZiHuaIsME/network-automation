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

VLANS =["1001","1002","1003","1004"]

def get_vlans_info(device:dict) -> dict:
    try:

        connection_args={k:v for k,v in device.items() if k!= "name"}
        connection = ConnectHandler(**connection_args)

        output = connection.send_command("show vlan brief")
        connection.disconnect()
        result=[]
        for line in output.splitlines():
            part = line.split()
            if part and part[0].isdigit():
                result.append(part[0])

        lacksvlan=[ i for i in VLANS if i not in result]

        return{
            "devicename":device['name'],
            "devicehost":device['host'],
            "checkat":str(datetime.datetime.now()),
            "devicevlan":result,
            "requirevlan":VLANS,
            "lacksvlan":lacksvlan,
            "status":"vlan check abnormal " if lacksvlan else "vlan check normal",
        }

    except Exception as e:
        return{
            "devicename":device['name'],
            "devicehost":device['host'],
            "checkat":str(datetime.datetime.now()),
            "error":str(e),
            "status":"failed"
        }

def main():
    filename=f"{datetime.date.today()}_check_vlan_report.json"
    result=[]
    for device in DEVICES:
        check_result=get_vlans_info(device)
        result.append(check_result)
        print(f"the {device['name']} is {check_result['status']}")

    with open(filename,"w") as f:
        json.dump(result,f,indent=2)
    print(f"save {filename} successfully")

if __name__ =="__main__":
    main()