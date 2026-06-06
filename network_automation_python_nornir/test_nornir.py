import os
import sys
import datetime
import json
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get

def inspect_network_task(task):

    try:

        napalm_result = task.run(
            task=napalm_get,
            getters=["interfaces"]
        )

        interface_data = napalm_result.result["interfaces"]

        return{
            "status":"success",
            "checkat":str(datetime.datetime.now()),
            "interfaces_count":len(interface_data),
            "raw_data":interface_data
        }
    except Exception as e:
        return{
            "status":"failed",
            "check_at":str(datetime.datetime.now()),
            "error":str(e)
        }

def main():

    nr = InitNornir(config_file="config.yaml")
    cisco_devices = nr.filter(name="cat8kv-01")
    
    all_result = cisco_devices.run(task=inspect_network_task)

    final_report = {}
    for host_name, task_result in all_result.items():
        final_report[host_name] = task_result[0].result

    filename = f"{datetime.date.today()}_nornir_test.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=4, ensure_ascii=False)
    
    print(f"脚本运行成功，数据已成功写入：{filename}")

if __name__ == "__main__":
    main()