import json
import datetime
from netmiko import ConnectHandler

DEVICE=[
    {
        "name":"cat8kv",
        "device_type":"cisco_ios",
        "host":"10.10.20.48",
        "username":"developer",
        "password":"C1sco12345",
    }
]

def run_full_audit(device:dict)->dict:
    audit={
        "device":device['name'],
        "ip":device['host'],
        "audited_at":str(datetime.datetime.now()),
        "checks":{}
    }

    try:
        connection_args={k:v for k,v in device.items() if k!="name"}
        connection= ConnectHandler(**connection_args)
        print("11111")

        checks={
            "reachability":"show ip interface brief",
            "cpu":"show processes cpu | include CPU",
            "memory":"show processec memory | include Processor",
            "ospf_neighbors":"show ip osfp neighbor",
            "hostname":"show running-config | include hostname",
        }

        for check_name,command in checks.items():
            output=connection.send_command(command)
            audit['checks'][check_name]={
                "command":command,
                "output":output,
                "collected_at":str(datetime.datetime.now()),
            }

        connection.disconnect()
        audit["status"] = "complete"

    except Exception as e:
        audit['status']="failed"
        audit['error']=str(e)


    return audit

def main():

    full_report={
        "audit_date":str(datetime.date.today()),
        "generated_at":str(datetime.datetime.now()),
        "total_devices":len(DEVICE),
        "results":[]
    }    

    for device in DEVICE:
        result = run_full_audit(device)
        full_report['results'].append(result)
    
    filename=f"full_audit_{datetime.date.today()}.json"

    with open(filename,"w") as f:
        json.dump(full_report,f,indent=2)

if __name__=="__main__":
    main()

