from ttp import ttp
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

def get_interface_info(device:dict) -> dict:
    try:

        connection_args={k:v for k,v in device.items() if k != "name"}
        connection = ConnectHandler(**connection_args)

        output= connection.send_command("show ip interface brief")
        print(output)
        connection.disconnect()
        
        template="{{Interface}}              {{IP-Address}}      {{OK?}} {{Method}} {{Status}}                {{Protocol}}"
        parser=ttp(data=output,template=template)
        parser.parse()

        parser_data=parser.result()[0][0]
        print(json.dumps(parser_data,indent=4))
        return {
            "devicename":device['name'],
            "devicehost":device['host'],
            "data":parser_data,
            "checkat":str(datetime.datetime.now()),
            "status":"successfully",
        }




    except Exception as e:
        return {
            "devicename":device['name'],
            "devicehost":device['host'],
            "error":str(e),
            "checkat":str(datetime.datetime.now()),
            "status":"failed",
        }

def main():
    result=[]
    for device in DEVICES:
        checkresult= get_interface_info(device)
        result.append(checkresult)
        print(checkresult)
    
    filename=(f"{datetime.date.today()}_test_ttp.json")
    with open(filename,"w") as f:
        json.dump(result,f,indent=2)
    print(f"save file in {filename} ")

if __name__ == "__main__":
    main()