import requests
import json
import urllib3

# SSL xəbərdarlıqlarını gizlədirik
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = "16.16.141.142"
QRADAR_TOKEN = "7535d031-9617-4852-995f-097c5b32b5f7"

# Ən universal və POST dəstəkləyən API yolu Reference Data-dır
url = f"https://{QRADAR_IP}/api/reference_data/sets"

headers = {
    'SEC': QRADAR_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def final_test():
    # QRadar-da test məqsədli bir siyahı (Reference Set) yaradırıq
    payload = {
        "element_type": "ALN",
        "name": "GitHub_Automation_Final_Test"
    }
    
    print(f"--- QRadar Bağlantı Testi ---")
    try:
        response = requests.post(url, headers=headers, json=payload, verify=False, timeout=20)
        
        print(f"Status Kodu: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ UGURLU! GitHub QRadar ilə rəsmi şəkildə əlaqə qurdu.")
        elif response.status_code == 409:
            print("✅ UGURLU! Obyekt artıq mövcuddur (Bağlantı var).")
        elif response.status_code == 401:
            print("❌ XƏTA: Token (SEC header) rədd edildi. Admin -> Authorized Services hissəsində tokeni yoxla.")
        else:
            print(f"❌ Server cavabı: {response.text}")

    except Exception as e:
        print(f"💥 Bağlantı xətası: {str(e)}")

if __name__ == "__main__":
    final_test()
