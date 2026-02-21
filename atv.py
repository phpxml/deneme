import requests
import re
import sys

def get_atv_link():
    # ATV'nin yayın anahtarlarını barındıran sayfa
    url = "https://v.atv.com.tr/videolar/canli-yayin"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Referer": "https://www.atv.com.tr/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # JSON veya sayfa içindeki m3u8 linkini ayıkla
        match = re.search(r'(https://[^\s^"]+?\.m3u8[^\s^"]*)', response.text)
        if match:
            # Tokenlı linki temizle
            return match.group(1).replace('\\/', '/')
        return None
    except:
        return None

link = get_atv_link()
if link:
    with open("atv.m3u", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV HD\n{link}\n")
    print("Link başarıyla güncellendi.")
else:
    print("Link bulunamadı!")
    sys.exit(1)

