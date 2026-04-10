import os
import requests
import json

# GitHub Secrets
QRADAR_IP = os.getenv('QRADAR_IP')
QRADAR_TOKEN = os.getenv('QRADAR_TOKEN')

# QRadar API-da qaydaları oxumaq və ya yaratmaq üçün rəsmi yol budur
# Diqqət: /api/analytics/rules çox vaxt GET üçündür, biz POST-u yoxlayırıq
url = f"https://{QRADAR_IP}/api/analytics/rules"

headers = {
    'SEC': QRADAR_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def sync_rules():
    rules_dir = 'rules/'
    
    if not os.path.exists(rules_dir):
        print("Səhv: rules/ qovluğu tapılmadı!")
        return

    for filename in os.listdir(rules_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(rules_dir, filename)
            with open(file_path, 'r') as f:
                try:
                    rule_data = json.load(f)
                    print(f"Hazırlanır: {filename}...")
                    
                    # QRadar-a göndəririk
                    response = requests.post(url, headers=headers, json=rule_data, verify=False)
                    
                    if response.status_code in [200, 201]:
                        print(f"✅ Uğurlu: {filename}")
                    else:
                        print(f"❌ Xəta ({filename}): Status {response.status_code}")
                        print(f"Server cavabı: {response.text}")
                        
                except Exception as e:
                    print(f"⚠️ {filename} işlənərkən xəta: {e}")

if __name__ == "__main__":
    # SSL xəbərdarlıqlarını gizlədirik (Verify=False istifadə etdiyimiz üçün)
    requests.packages.urllib3.disable_warnings()
    sync_rules()
