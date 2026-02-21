import requests
import re
import sys

def get_final_atv_link():
    # Durak 1: Ana Sayfa (HTML içindeki JS yollarını bulmak için)
    base_url = "https://www.atv.com.tr/canli-yayin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; samsung SM-N975F Build/SP1A.210812.016) IPTV Pro/9.1.15",
        "Referer": "https://www.atv.com.tr/",
        "Accept": "*/*"
    }

    try:
        session = requests.Session()
        print("1. Durak: Ana sayfa taranıyor...")
        main_page = session.get(base_url, headers=headers, timeout=15).text
        
        # Durak 2: Sayfadaki tüm JS ve API beslemelerini listele
        # Hem m3u8 arıyoruz hem de link barındırabilecek v.atv.com.tr gibi adresleri
        potential_sources = re.findall(r'src="([^"]+?\.js[^"]*)"', main_page)
        potential_sources.append("https://v.atv.com.tr/videolar/canli-yayin") # Kritik API durağı
        
        for source in potential_sources:
            if source.startswith('/'):
                source = "https://www.atv.com.tr" + source
            
            print(f"Zincir Takibi: {source} inceleniyor...")
            content = session.get(source, headers=headers, timeout=10).text
            
            # Durak 3: API/JS yanıtı içindeki o nihai player linkini (m3u8) yakala
            match = re.search(r'(https:[^\s^"]+?\.m3u8[^\s^"]*)', content)
            if match:
                final_link = match.group(1).replace('\\/', '/')
                # Linkin sonundaki çöp karakterleri temizle (tırnak vs.)
                final_link = final_link.split('"')[0].split("'")[0]
                return final_link
                
    except Exception as e:
        print(f"Zincir koptu: {e}")
    return None

# M3U oluşturma
final_url = get_final_atv_link()
if final_url:
    with open("atv.m3u", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV HD\n{final_url}\n")
    print("BİNGÖL! Zincirin sonundaki link yakalandı.")
else:
    print("Zincir takip edildi ama linke ulaşılamadı.")
    sys.exit(1)
