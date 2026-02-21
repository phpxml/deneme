import requests
import re
import os

def idm_grabber():
    url = "https://www.atv.com.tr/canli-yayin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.atv.com.tr/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        # IDM'in yaptığı gibi sayfa içinde hazır bekleyen m3u8 linkini cımbızla çekiyoruz
        match = re.search(r'(https://[^\s^"]+?\.m3u8[^\s^"]*)', response.text)
        if match:
            return match.group(1).replace('\\/', '/')
    except Exception as e:
        print(f"Hata: {e}")
    return None

atv_link = idm_grabber()
if atv_link:
    with open("atv.m3u", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV HD\n{atv_link}\n")
    print("Link yakalandı!")
else:
    print("Link bulunamadı!")
    exit(1) # Hata olduğunu Actions'a bildir
