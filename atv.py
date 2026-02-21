import requests
import re

def get_atv_link():
    try:
        url = "https://www.atv.com.tr/canli-yayin"
        # Kendimizi bir tarayıcı gibi tanıtıyoruz (User-Agent)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Referer": "https://www.atv.com.tr/"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        # Sayfa kaynağındaki m3u8 uzantılı dinamik linki yakalıyoruz
        match = re.search(r'(https://[^\s^"]+?\.m3u8[^\s^"]*)', response.text)
        
        if match:
            # Kaçış karakterlerini temizliyoruz
            raw_url = match.group(1).replace('\\/', '/')
            return raw_url
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None
    return None

# M3U formatında dosyayı oluştur
atv_link = get_atv_link()
if atv_link:
    with open("atv.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1,ATV HD\n")
        f.write(f"{atv_link}\n")
    print("atv.m3u başarıyla güncellendi.")
else:
    print("Link bulunamadı!")
