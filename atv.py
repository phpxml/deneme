import requests
import re
import sys

def get_link_with_proxy():
    url = "https://v.atv.com.tr/videolar/canli-yayin"
    
    # Türkiye Proxy taklidi (Halkasız/Public proxy deniyoruz)
    # Eğer bu çalışmazsa Türkiye tabanlı bir VPN/Proxy adresi bulup buraya yazabiliriz
    proxies = {
        "http": "http://88.230.128.12:8080", 
        "https": "http://88.230.128.12:8080"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; samsung SM-N975F Build/SP1A.210812.016) IPTV Pro/9.1.15",
        "Referer": "https://www.atv.com.tr/",
        "X-Requested-With": "com.turkuvaz.atv",
        "Accept-Language": "tr-TR,tr;q=0.9"
    }

    try:
        # Önce proxy ile dene, olmazsa normal devam et (session yönetimi)
        session = requests.Session()
        try:
            response = session.get(url, headers=headers, proxies=proxies, timeout=10)
        except:
            response = session.get(url, headers=headers, timeout=15)
            
        content = response.text
        
        # Tokenlı linkleri bul (st= ve e= parametrelerini yakalar)
        matches = re.findall(r'(https:[^\s^"]+?\.m3u8\?[^\s^"]+)', content)
        
        for link in matches:
            clean_link = link.replace('\\/', '/')
            # Senin Almanya IP'nden dolayı gelen 'atvavrupa'yı değil, 'atvhd'yi seçmeye zorluyoruz
            if "atvavrupa" not in clean_link:
                return clean_link.split('"')[0].split("'")[0]
                
    except Exception as e:
        print(f"Hata: {e}")
    return None

link = get_link_with_proxy()
if link:
    with open("atv.m3u", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV HD (TR)\n{link}\n")
    print(f"Token Yakalandı: {link}")
else:
    print("HATA: Link bulunamadı! ATV hala blokluyor olabilir.")
    sys.exit(1)
