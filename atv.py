import requests
import re
import sys

def get_token_link():
    # ATV'nin canlı yayın verilerini sakladığı gizli API yolları
    endpoints = [
        "https://v.atv.com.tr/videolar/canli-yayin",
        "https://www.atv.com.tr/canli-yayin",
        "https://v.atv.com.tr/api/video/canli-yayin"
    ]
    
    # Senin Note 10+ ve IPTV Pro kimliğin (User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; samsung SM-N975F Build/SP1A.210812.016) IPTV Pro/9.1.15",
        "Referer": "https://www.atv.com.tr/",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        session = requests.Session()
        for url in endpoints:
            print(f"Deneniyor: {url}")
            response = session.get(url, headers=headers, timeout=15)
            content = response.text
            
            # Regex: m3u8 uzantılı ve içinde token olan (veya olmayan) tüm linkleri bul
            # Özellikle 'atvavrupa' olmayanları filtrele
            links = re.findall(r'(https:[^\s^"]+?\.m3u8[^\s^"]*)', content)
            
            for raw_link in links:
                clean_link = raw_link.replace('\\/', '/')
                # Avrupa yayınını ele, asıl yayını (atvhd veya master) bul
                if "atvavrupa" not in clean_link and ("atv" in clean_link or "master" in clean_link):
                    # Linkin tırnaklarını temizle
                    final_link = clean_link.split('"')[0].split("'")[0]
                    # Token kontrolü (Linkin sonunda ?t= veya ?token= olmalı)
                    return final_link
                    
    except Exception as e:
        print(f"Hata: {e}")
    return None

link = get_token_link()
if link:
    with open("atv.m3u", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV HD (Canlı)\n{link}\n")
    print(f"BULDUM: {link}")
else:
    print("Hata: Tokenlı link bulunamadı!")
    sys.exit(1)
