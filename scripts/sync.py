import os
import requests
import json

# GitHub Secrets-dən məlumatları götürürük
QRADAR_IP = os.getenv('QRADAR_IP')
QRADAR_TOKEN = os.getenv('QRADAR_TOKEN')

# QRadar API URL (Qaydaların siyahısı üçün)
# Qeyd: Bir çox QRadar versiyasında qaydalar 'analytics/rules' yerinə 'offense_management/rules' altında olur
url = f"https://{QRADAR_IP}/api/offense_management/rules"

headers = {
    'SEC': QRADAR_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def sync_rules():
    rules_dir = 'rules/'
    
    for filename in os.listdir(rules_dir):
        if filename.endswith('.json'):
            with open(os.path.join(rules_dir, filename), 'r') as f:
                try:
                    rule_data = json.load(f)
                    rule_name = rule_data.get('name', filename)
                    
                    print(f"Göndərilir: {rule_name}...")
                    
                    # Verify=False SSL sertifikat xətasının qarşısını alır
                    response = requests.post(url, headers=headers, data=json.dumps(rule_data), verify=False)
                    
                    if response.status_code == 201 or response.status_code == 200:
                        print(f"✅ Uğurlu: {rule_name} QRadar-a əlavə edildi.")
                    else:
                        print(f"❌ Xəta baş verdi ({rule_name}): {response.status_code} - {response.text}")
                
                except Exception as e:
                    print(f"⚠️ Fayl oxunarkən xəta ({filename}): {str(e)}")

if __name__ == "__main__":
    sync_rules()
