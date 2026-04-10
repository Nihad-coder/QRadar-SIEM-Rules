import os
import requests
import json

# Məlumatları bura birbaşa yazırıq ki, heç bir şübhə qalmasın
QRADAR_IP = "16.16.141.142"
QRADAR_TOKEN = "7535d031-9617-4852-995f-097c5b32b5f7"

# Bu endpoint demək olar ki, hər sistemdə POST-u dəstəkləyir
url = f"https://{QRADAR_IP}/api/reference_data/sets"

headers = {
    'SEC': QRADAR_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def sync_test():
    # Test məqsədli sadə bir Reference Set yaradırıq
    test_data = {
        "element_type": "ALN",
        "name": "GitHub_Sync_Test"
    }
    
    print(f"QRadar-a bağlanmağa çalışılır: {QRADAR_IP}...")
    
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.post(url, headers=headers, json=test_data, verify=False)
        
        if response.status_code in [200, 201]:
            print("✅ MÜKƏMMƏL! GitHub QRadar-a qoşuldu və test məlumatını yaratdı.")
        elif response.status_code == 409:
            print("✅ Artıq mövcuddur: Test obyekti artıq QRadar-da var (Bağlantı uğurludur).")
        else:
            print(f"❌ Server cavabı: {response.status_code}")
            print(f"Detallar: {response.text}")
            
    except Exception as e:
        print(f"💥 Qoşulma zamanı ciddi xəta: {e}")

if __name__ == "__main__":
    sync_test()
