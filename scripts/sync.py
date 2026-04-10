import os
import json
import requests

# QRadar məlumatları (GitHub Secrets-dən gələcək)
QRADAR_IP = os.getenv('QRADAR_IP')
API_TOKEN = os.getenv('QRADAR_TOKEN')

# QRadar API başlığı
headers = {
    'SEC': API_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def push_rule_to_qradar(file_path):
    with open(file_path, 'r') as f:
        rule_data = json.load(f)
    
    # QRadar-da qayda yaratmaq və ya yeniləmək üçün endpoint
    # Qeyd: Bu sadələşdirilmiş bir nümunədir
    url = f"https://{QRADAR_IP}/api/analytics/rules"
    
    print(f"Gah göndərilir: {rule_data['name']}...")
    
    # SSL yoxlamasını (verify=False) laboratoriya mühiti üçün söndürürük
    response = requests.post(url, headers=headers, data=json.dumps(rule_data), verify=False)
    
    if response.status_code == 201 or response.status_code == 200:
        print(f"Uğurlu: {rule_data['name']} QRadar-a göndərildi.")
    else:
        print(f"Xəta baş verdi: {response.status_code} - {response.text}")

# Rules qovluğundakı bütün .json fayllarını tap və göndər
rules_dir = 'rules/'
for filename in os.listdir(rules_dir):
    if filename.endswith('.json'):
        push_rule_to_qradar(os.path.join(rules_dir, filename))
