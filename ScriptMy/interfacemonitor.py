import time
import datetime
from netmiko import ConnectHandler

DEVICES=[
    {
        "name":"cat8kv",
        "device_type":"cisco_ios",
        "host":"10.10.20.48",
        "username":"developer",
        "password":"C1sco12345"
    }
]

def get_interface_status(device:dict) -> dict :
    try:

        connection_args={k:v for k,v in device.items() if k!="name"}
        connection=ConnectHandler(**connection_args)

        interfaceinfo=connection.send_command("show ip interface brief")
        connection.disconnect()

        interfacestatus={}


        lines=interfaceinfo.splitlines()        
        for line in lines:
            parts=line.split()
            if len(parts)>=6 and parts[0] !="Interface":
                interfacestatus[parts[0]]=parts[4]
        return interfacestatus


    

    except Exception as e:
        return{
            "e":str(e)
        }

def main():
    previous_state={}
    current_state={}

    while True:
        for device in DEVICES:
            current_state=get_interface_status(device)
            
            for interface , status in current_state.items():
                previous_status=previous_state.get(interface)
                if previous_status is None :
                    print(f"{device['name']}{interface}"
                        f"status:{status}"
                    )
                elif previous_status == "up" and status != "up":
                    print(f"alert {device['name']} {interface} went down")
                elif previous_status != "up" and status =="up":
                    print(f"{device['name']} {interface} is up")
            previous_state = current_state



if __name__ == "__main__":
    main()