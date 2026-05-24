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

HIGH_USAGE_THRESHOLD = 85

def get_bandwidth_status(device:dict) -> dict:

    print(f"connecting {device['name']}({device['host']})")

    try:
        connection_args = {k:v for k,v in device.items() if k!="name"}
        connection = ConnectHandler(**connection_args)
        interfac_info=connection.send_command("show interface")
        connection.disconnect()
        result=[]
        current_interface= None
        input_rate= None
        for line in interfac_info.splitlines():
            line = line.strip()
            if line.startswith("GigabitEthernet") or line.startswith("Loopback"):
                current_interface = line.split()[0]
                input_rate= None
            
            elif "input rate" in line and current_interface:
                try:
                    part=line.split()
                    input_rate=int(part[4])
                except (ValueError,IndexError):
                    input_rate= None
            elif "output rate" in line and current_interface and input_rate is not None:
                try:
                    part=line.split()
                    output_rate=int(part[4])
                    utilisation= round((output_rate + input_rate) / 1000000,2)
                    result.append({
                        "current_interface":current_interface,
                        "input_rate":input_rate,
                        "output_rate":output_rate,
                        "utilisation":utilisation,
                        "high_usage": utilisation > HIGH_USAGE_THRESHOLD
                    })
                except (ValueError,IndexError):
                    pass
                input_rate= None
        high_usage = [i for i in result if i['high_usage']]
    
        return {
        "devicename":device['name'],
        "devicehost":device['host'],
        "devicecheckat":str(datetime.datetime.now()),
        "result":result,
        "status": "Alarm" if high_usage else "Normal",
        }

    except Exception as e:
        return {
        "devicename":device['name'],
        "devicehost":device['host'],
        "devicecheckat":str(datetime.datetime.now()),
        "error":str(e),
        "status":"failed",
    }

def main():
    print(f"checking bandwidth_monitor at {datetime.datetime.now()}")
    result = []
    for device in DEVICES:
        checkresult = get_bandwidth_status(device)
        result.append(checkresult)
        print(checkresult)
        print(f"{device['name']} is {checkresult['status']}")
        if checkresult['status'] == "Alarm":
            for interface in checkresult['result']:
                print(f"HIGH USAGE : {interface['current_interface']} -- {interface['uitlisation']}Mbps")

    filename=f"{datetime.date.today()}_bandwidth_monitor.json"
    
    with open(filename,"w") as f:
        json.dump(result,f,indent=2)

if __name__ == "__main__":
    main()


#why we need to reset input_rate twice:

# GigabitEthernet1 is up, line protocol is up
# 5 minute input rate 5000 bits/sec
# 5 minute output rate 4000 bits/sec
# 20 second input rate 1100 bits/sec
# 20 second output rate 900 bits/sec
# GigabitEthernet2 is up, line protocol is up
# 5 minute input rate 100 bits/sec
# 5 minute output rate 200 bits/sec

# GigabitEthernet1 is up...
#   5 minute input rate 5000 bits/sec
#   5 minute output rate 4000 bits/sec
# GigabitEthernet2 is up...
#   5 minute output rate 0 bits/sec  <-- (No input line printed by router!)