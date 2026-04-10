import os
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = "16.16.141.142"
QRADAR_TOKEN = "7535d031-9617-4852-995f-097c5b32b5f7"
SET_NAME = "GitHub_SIEM_Rules_List"

headers = {
    'SEC': QRADAR_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def sync():
    # 1. Addım: Reference Set yaratmağa çalışırıq (yoxdursa)
    create_url = f"https://{QRADAR_IP}/api/reference_data/sets"
    payload = {"element_type": "ALN", "name": SET_NAME}
    
    print(f"Siyahı yoxlanılır: {SET_NAME}")
    requests.post(create_url, headers=headers, json=payload, verify=False)

    # 2. Addım: Qaydaları oxuyub siyahıya əlavə edirik
    data_url = f"https://{QRADAR_IP}/api/reference_data/sets/{SET_NAME}"
    rules_dir = 'rules/'
    
    for filename in os.listdir(rules_dir):
        if filename.endswith('.json'):
            with open(os.path.join(rules_dir, filename), 'r') as f:
                rule_content = json.load(f)
                rule_name = rule_content.get('name', filename)
                
                # QRadar bu formatda qəbul edir: ["element1", "element2"]
                response = requests.post(data_url, headers=headers, json=[rule_name], verify=False)
                
                if response.status_code in [200, 201]:
                    print(f"✅ Əlavə edildi: {rule_name}")
                else:
                    print(f"❌ {rule_name} üçün xəta: {response.status_code}")

if __name__ == "__main__":
    sync()
