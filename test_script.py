#!/usr/bin/env python3
import json
import subprocess

def get_k8s_pods():
    # Esempio: recupera i pod nel namespace default usando kubectl
    try:
        cmd = ["kubectl", "get", "pods", "-o", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        hosts = []
        for item in data.get("items", []):
            pod_name = item["metadata"]["name"]
            # Prende l'IP del pod se disponibile
            pod_ip = item["status"].get("podIP", "127.0.0.1")
            hosts.append((pod_name, pod_ip))
        return hosts
    except Exception as e:
        # Fallback di test se kubectl non è disponibile in locale
        return [("ubuntu-pod-test-1", "10.244.0.15")]

def main():
    pods = get_k8s_pods()
    
    inventory = {
        "_meta": {
            "hostvars": {}
        },
        "k8s_pods": {
            "hosts": [],
            "vars": {
                "ansible_user": "root"
            }
        }
    }

    for name, ip in pods:
        inventory["k8s_pods"]["hosts"].append(name)
        inventory["_meta"]["hostvars"][name] = {
            "ansible_host": ip
        }

    print(json.dumps(inventory, indent=2))

if __name__ == "__main__":
    main()
