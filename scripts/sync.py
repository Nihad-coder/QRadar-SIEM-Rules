import os
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Melumatlari birbasa bura yaziriq
QRADAR_IP = "16.16.141.142"
QRADAR_TOKEN = "7535d031-9617-4852-995f-097c5b32b5f7"

# Reference Set endpoint-i melumat yazmaq ucun en stabil yoldur
url = f"https://{QRADAR_IP}/api/reference_data/sets/GitHub_Automation_Final_Test"

headers = {
    'SEC': QRADAR_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def sync_rules():
    rules_dir = 'rules/'
    print(f"--- QRadar Qayda Sinxronizasiyasi Basladi ---")

    for filename in os.listdir(rules_dir):
        if filename.endswith('.json'):
            with open(os.path.join(rules_dir, filename), 'r') as f:
                rule_data = json.load(f)
                rule_name = rule_data.get('name', filename)
                
                # Qaydanin adini QRadar-da bir element kimi yaradiriq
                # Bu, qaydanin sistemde oldugunu subut edir
                payload = [rule_name] 
                
                try:
                    # Melumati QRadar-a gonderirik
                    response = requests.post(url, headers=headers, json=payload, verify=False)
                    if response.status_code in [200, 201]:
                        print(f"✅ Sinxron edildi: {rule_name}")
                    else:
                        print(f"⚠️ {rule_name} gonderilerken server cavabi: {response.status_code}")
                except Exception as e:
                    print(f"❌ Xeta ({filename}): {str(e)}")

if __name__ == "__main__":
    sync_rules()
