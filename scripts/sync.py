import requests
import json
import urllib3

# SSL xəbərdarlıqlarını söndürürük
urllib3.disable_warnings()

QRADAR_IP = "16.16.141.142"
QRADAR_TOKEN = "7535d031-9617-4852-995f-097c5b32b5f7"

# Ən sadə "GET" sorğusu ilə yoxlayaq (Reference sets siyahısını oxumaq)
url = f"https://{QRADAR_IP}/api/reference_data/sets"

headers = {
    'SEC': QRADAR_TOKEN,
    'Accept': 'application/json'
}

print(f"--- BAĞLANTI TESTİ BAŞLADI ---")
print(f"Hədəf: {QRADAR_IP}")

try:
    # Timeout-u 30 saniyə edirik ki, şəbəkə zəif olsa gözləsin
    response = requests.get(url, headers=headers, verify=False, timeout=30)
    
    print(f"Status Kodu: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ UGURLU! QRadar-a qoşulmaq olur və Token işləyir.")
    elif response.status_code == 401:
        print("❌ XƏTA: Token səhvdir və ya Deploy edilməyib (Unauthorized).")
    elif response.status_code == 404:
        print("❌ XƏTA: API yolu tapılmadı (404 Not Found).")
    else:
        print(f"❌ Server cavabı: {response.text}")

except requests.exceptions.Timeout:
    print("💥 XƏTA: Bağlantı vaxt aşımına uğradı (Timeout). Port 443 bağlı ola bilər və ya IP-yə çatılmır.")
except Exception as e:
    print(f"💥 Gözlənilməz xəta: {str(e)}")
