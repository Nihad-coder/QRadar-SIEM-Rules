import requests
import urllib3

# Bütün xəbərdarlıqları və mürəkkəbliyi kənara qoyuruq
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = "16.16.141.142"
QRADAR_TOKEN = "7535d031-9617-4852-995f-097c5b32b5f7"

# Ən sadə Reference Set metodu: Birbaşa element əlavə etmək
# 'GitHub_Test_Set' adında siyahıya 'Rule_1_Active' yazısını atırıq
url = f"https://{QRADAR_IP}/api/reference_data/sets/GitHub_Test_Set"

headers = {
    'SEC': QRADAR_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def final_push():
    # QRadar bu formatda siyahı gözləyir: ["element"]
    payload = ["Rule_1_Active"]
    
    print(f"QRadar-a məlumat göndərilir...")
    try:
        # verify=False mütləqdir, timeout-u da qoyuruq
        response = requests.post(url, headers=headers, json=payload, verify=False, timeout=20)
        
        print(f"Status Kodu: {response.status_code}")
        if response.status_code in [200, 201]:
            print("✅ UGURLU! Məlumat QRadar-a çatdı.")
        else:
            print(f"❌ Server rədd etdi: {response.text}")
            
    except Exception as e:
        print(f"💥 Qoşulma xətası: {str(e)}")

if __name__ == "__main__":
    final_push()
