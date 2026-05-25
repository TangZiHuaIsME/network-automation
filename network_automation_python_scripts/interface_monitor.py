import json
import time
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

POLL_INTERVAL = 60

def get_interface_info(device:dict) -> dict:
    try:

        connection_args={k:v for k,v in device.items() if k!= "name"}
        connection = ConnectHandler(**connection_args)
        output = connection.send_command("show ip interface brief")
        connection.disconnect()
        interface_status={}

        for line in output.splitlines():
            line=line.strip()
            parts=line.split()
            if len(parts)>= 5 and parts[0] != "interface":
                interface_status[parts[0]] = parts[4]
        return interface_status
        # return {
        #     "device name":device['name'],
        #     "device host":device['host'],
        #     "interface_status":interface_status,
        #     "checkat":str(datetime.datetime.now()),
        #     "status":"get devce interface successfully",
        # }

    except Exception as e:

        return {
            "error":str(r)
        }
        # return {
        #     "device name":device['name'],
        #     "device host":device['host'],
        #     "error":str(e),
        #     "checkat":str(datetime.datetime.now()),
        #     "status":"get devce interface failed",
        # }

    
def main():
    previs_status = None
    while True:
        for device in DEVICES:
            status = get_interface_info(device)
            for interface, current_status in status.items():
                if current_status == "up" and previs_status is None:
                    print(f"INIT {device['name']} {interface} is up")
                elif current_status == "down" and previs_status == "up":
                    print(f"ALERT {device['name']} {interface} == down")
                elif current_status == "up" and previs_status == "up":
                    print(f"NORMAL {device['name']} {interface} is up" )
                elif current_status == "up" and previous_state == "down":
                    print(f"RECOVERY {device['name']} {interface} is back up")
            previs_status = current_status
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()

