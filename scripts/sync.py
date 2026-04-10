import requests
import urllib3

# Logları təmizləmək üçün xəbərdarlıqları söndürürük
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Məlumatları birbaşa bura yazırıq
QRADAR_IP = "16.16.141.142"
QRADAR_TOKEN = "7535d031-9617-4852-995f-097c5b32b5f7"

# Bu yol QRadar-ın rəsmi API yardım səhifəsidir, mütləq cavab verməlidir
url = f"https://{QRADAR_IP}/api/help/capabilities"

headers = {
    'SEC': QRADAR_TOKEN,
    'Accept': 'application/json'
}

print(f"Bağlantı yoxlanılır: {QRADAR_IP}")

try:
    # 30 saniyə vaxt veririk
    response = requests.get(url, headers=headers, verify=False, timeout=30)
    
    if response.status_code == 200:
        print("✅ UGURLU! GitHub QRadar-a çatdı.")
    else:
        print(f"❌ Server cavab verdi, amma xəta var. Kod: {response.status_code}")
        print(f"Mesaj: {response.text[:200]}")

except Exception as e:
    print(f"💥 Bağlantı kəsildi! Səbəb: {str(e)}")
    print("İPUCU: AWS Security Group-da 443 portunun 0.0.0.0/0 üçün açıq olduğuna bir daha baxın.")
