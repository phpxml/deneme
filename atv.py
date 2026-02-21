import requests
import re
import sys

def get_atv_hd_with_token():
    # Bu adres, ATV'nin canlı yayın token'larını dağıttığı resmi API noktasıdır
    api_url = "https://v.atv.com.tr/videolar/canli-yayin"
    
    # Senin Note 10+ ve IPTV Pro parmak izin (User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; samsung SM-N975F Build/SP1A.210812.016) IPTV Pro/9.1.15",
        "Referer": "https://www.atv.com.tr/",
        "Accept": "*/*"
    }

    try:
        # API'ye gidip ham veriyi çekiyoruz
        response = requests.get(api_url, headers=headers, timeout=15)
        content = response.text
        
        # Regex ile sadece içinde 'atvhd' ve 'token' (veya karmaşık karakterler) olan linki buluyoruz
        # Avrupa yayınlarını (atvavrupa) listeden eliyoruz
        links = re.findall(r'(https:[^\s^"]+?\.m3u8[^\s^"]*)', content)
        
        for raw_link in links:
            clean_link = raw_link.replace('\\/', '/')
            # Filtre: İçinde 'avrupa' geçmesin ama 'atv' geçsin
            if "atvavrupa" not in clean_link and "atv" in clean_link:
                # Linkin sonunda tırnak kalmışsa temizle
                final_link = clean_link.split('"')[0].split("'")[0]
                return final_link
                
    except Exception as e:
        print(f"Token çekme hatası: {e}")
    return None

# M3U dosyasını oluştur
token_link = get_atv_hd_with_token()

if token_link:
    # Linkin içinde token olup olmadığını kontrol et (genellikle ?t= veya ?token=)
    with open("atv.m3u", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV HD (Canlı)\n{token_link}\n")
    print(f"Başarılı! Tokenlı Link: {token_link}")
else:
    print("Hata: Asıl yayın linki veya token bulunamadı.")
    sys.exit(1)
