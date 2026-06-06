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

def get_audit_info(device:dict) -> dict:
    result_list = {
        "device_name":device['name'],
        "device_host":device['host'],
        "result":{}
    }

    check_list = {
        "version":"show version",
        "cpu":"show processes cpu ",
        "inventory":"show inventory",

    }


    try:
        connection_args = {k:v for k,v in device.items() if k!= "name"}
        connection = ConnectHandler(**connection_args)
        for info,command in check_list.items():
            result_list['result'][info]=connection.send_command(command)
        connection.disconnect()


        result_list['result']['status']="get audit successfully"
        return {
            "status":result_list['result']['status'],
            "result":result_list,
        }



    
    except Exception as e:
        result_list['result']['status']="get audit failed"
        result_list['result']['error']=str(e)
        return{
            "status":result_list['result']['status'],
            "error":result_list['result']['error'],
            "result":result_list,
        }

def main():
    result=[]

    for device in DEVICES:
        print("--------------")
        check_result= get_audit_info(device)
        result.append(check_result)
        print(f"{check_result['status']}")
    
    filename=f"{datetime.date.today()}_audit.json"

    with open(filename,"w") as f:
        json.dump(result,f,indent=4)
    print(f"save file in {filename}")

if __name__ == "__main__":
    main()