import requests
import json

# Məlumatları bura birbaşa, dırnaq içində yazırıq
QRADAR_IP = "16.16.141.142"
QRADAR_TOKEN = "7535d031-9617-4852-995f-097c5b32b5f7"

# Bu API yolu (Reference Sets) QRadar-da ən stabil yoldur
url = f"https://{QRADAR_IP}/api/reference_data/sets"

headers = {
    'SEC': QRADAR_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def sync_test():
    # Sadə bir test obyekti
    test_data = {
        "element_type": "ALN",
        "name": "GitHub_Connection_Test"
    }
    
    print(f"QRadar-a ({QRADAR_IP}) bağlanmağa çalışılır...")
    
    try:
        # SSL sertifikat yoxlamasını söndürürük
        requests.packages.urllib3.disable_warnings()
        response = requests.post(url, headers=headers, json=test_data, verify=False, timeout=15)
        
        if response.status_code in [200, 201]:
            print("✅ ƏLA! Bağlantı quruldu və test obyekti yaradıldı.")
        elif response.status_code == 409:
            print("✅ Bağlantı uğurludur! (Obyekt artıq QRadar-da mövcuddur).")
        else:
            print(f"❌ Xəta kodu: {response.status_code}")
            print(f"Serverin cavabı: {response.text}")
            
    except Exception as e:
        print(f"💥 Bağlantı baş tutmadı! Səbəb: {str(e)}")

if __name__ == "__main__":
    sync_test()
