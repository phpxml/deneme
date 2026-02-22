import requests
import re

def kanald_link_al():
    url = "https://www.kanald.com.tr/canli-yayin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.kanald.com.tr/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # m3u8 linkini temiz bir şekilde ayıklıyoruz
        match = re.search(r'https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*', response.text)
        if match:
            # HTML karakterlerini (varsa) temizle
            clean_link = match.group(0).replace('&amp;', '&')
            return clean_link
    except:
        return None
    return None

yeni_link = kanald_link_al()

if yeni_link:
    with open("kanald_canli.m3u", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,Kanal D HD\n{yeni_link}")
    print("Link başarıyla güncellendi.")
