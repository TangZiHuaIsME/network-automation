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

def run_audit(device:dict) -> dict:
    audit = {
        "devicename":device['name'],
        "devicehost":device['host'],
        "checkat":str(datetime.datetime.now()),
        "result":{}
    }

    try:

        checklist={
            "interface":   "show ip interface brief",
            "cpu":            "show processes cpu | include CPU",
            "memory":         "show processes memory | include Processor",
            "ospf_neighbors": "show ip ospf neighbor",
            "hostname":       "show running-config | include hostname",
            "inventory":      "show inventory",
        }

        connection_args = {k:v for k,v in device.items() if k!= "name"}
        connection = ConnectHandler(**connection_args)

        for description,command in checklist.items():
            audit['result'][description] = connection.send_command(command)
        audit['status'] ="complete"

        connection.disconnect()

    except Exception as e:
        audit['status'] = "failed"
        audit['error'] = str(e)

    return audit

def main():
    filename = f"{datetime.date.today()}_audit.json"

    audit=[]

    for device in DEVICES:
        check_result=run_audit(device)
        audit.append(check_result)
        print(f"{check_result}")
    
    with open(filename,"w") as f:
        json.dump(audit,f)
    print(f"\n saved the audit into {filename}")
if __name__ == "__main__":
    main()
