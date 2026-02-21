import requests
import re
import sys

def get_real_atv_hd_with_token():
    # ATV'nin ana yayın API'si
    url = "https://v.atv.com.tr/videolar/canli-yayin"
    
    # Senin Note 10+ kimliğin ve Türkiye'deymişsin gibi davranan başlıklar
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; samsung SM-N975F Build/SP1A.210812.016) IPTV Pro/9.1.15",
        "Referer": "https://www.atv.com.tr/",
        "X-Forwarded-For": "88.230.128.12", # Türkiye'den rastgele bir ev IP'si taklidi
        "X-Real-IP": "88.230.128.12",
        "Accept-Language": "tr-TR,tr;q=0.9",
        "X-Requested-With": "com.turkuvaz.atv"
    }

    try:
        session = requests.Session()
        # Sunucuya "Ben Türkiye'deyim" sinyali göndererek ana yayını istiyoruz
        response = session.get(url, headers=headers, timeout=15)
        content = response.text
        
        # Regex ile hem m3u8'i hem de senin paylaştığın st= ve e= gibi parametreleri yakalıyoruz
        # Özellikle 'atvavrupa' olmayan, içinde 'atvhd' geçen linklere odaklanıyoruz
        links = re.findall(r'(https:[^\s^"]+?\.m3u8\?[^\s^"]+)', content)
        
        for raw_link in links:
            clean_link = raw_link.replace('\\/', '/')
            # Avrupa yayını gelirse pas geç, ana yayını (atvhd veya master) bul
            if "atvavrupa" not in clean_link:
                final_link = clean_link.split('"')[0].split("'")[0]
                return final_link
                
    except Exception as e:
        print(f"Hata: {e}")
    return None

link = get_real_atv_hd_with_token()
if link:
    with open("atv.m3u", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV HD (Canlı)\n{link}\n")
    print(f"Türkiye yayını ve token yakalandı: {link}")
else:
    print("Link yakalanamadı, sunucu hala Avrupa'ya yönlendiriyor olabilir.")
    sys.exit(1)
