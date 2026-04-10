import os
import requests
import json
import urllib3

# SSL xəbərdarlıqlarını söndürürük
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
    # 1. ADDIM: Reference Set-in mövcudluğunu yoxlayırıq, yoxdursa yaradırıq
    check_url = f"https://{QRADAR_IP}/api/reference_data/sets/{SET_NAME}"
    print(f"Yoxlanılır: {SET_NAME}...")
    
    check_res = requests.get(check_url, headers=headers, verify=False)
    
    if check_res.status_code == 404:
        print(f"Siyahı tapılmadı. Yaradılır...")
        create_url = f"https://{QRADAR_IP}/api/reference_data/sets"
        create_payload = {"element_type": "ALN", "name": SET_NAME}
        requests.post(create_url, headers=headers, json=create_payload, verify=False)
    
    # 2. ADDIM: Qaydaları oxuyub siyahıya əlavə edirik
    rules_dir = 'rules/'
    data_url = f"https://{QRADAR_IP}/api/reference_data/sets/bulk_load/{SET_NAME}"
    
    rule_names = []
    for filename in os.listdir(rules_dir):
        if filename.endswith('.json'):
            with open(os.path.join(rules_dir, filename), 'r') as f:
                content = json.load(f)
                rule_names.append(content.get('name', filename))

    # Bütün qaydaları bir dəfəyə (bulk load) göndəririk
    print(f"Qaydalar göndərilir: {rule_names}")
    response = requests.post(data_url, headers=headers, json=rule_names, verify=False)
    
    if response.status_code in [200, 201]:
        print("✅ Mükəmməl! Bütün qaydalar QRadar-a uğurla sinxron edildi.")
    else:
        print(f"❌ Xəta: {response.status_code} - {response.text}")

if __name__ == "__main__":
    sync()
