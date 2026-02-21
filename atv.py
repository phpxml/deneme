import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def idm_logic_grabber():
    # 1. IDM gibi tarayıcıyı hazırlıyoruz (Gizli mod)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 2. Ağ trafiğini dinlemek için logları açıyoruz (Sniffing)
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options, desired_capabilities=caps)

    try:
        # 3. Sayfaya gidiyoruz ve IDM gibi bekliyoruz
        driver.get("https://www.atv.com.tr/canli-yayin")
        time.sleep(15) # Sayfanın ve player'ın tüm tokenları çözmesi için süre veriyoruz

        # 4. IDM'in yaptığı gibi "Network" loglarını tarıyoruz
        logs = driver.get_log("performance")
        
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if "Network.requestServedFromCache" in log["method"] or "Network.requestWillBeSent" in log["method"]:
                url = log["params"].get("request", {}).get("url", "")
                # Player'ın en son ulaştığı m3u8 linkini yakala
                if "master.m3u8" in url or "atv.m3u8" in url:
                    # Tokenlı ve her şey bitmiş nihai linki bulduk!
                    return url
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        driver.quit()
    return None

# Linki al ve dosyaya yaz
final_url = idm_logic_grabber()
if final_url:
    with open("atv.m3u", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1,ATV HD\n{final_url}\n")
    print("Link IDM mantığıyla başarıyla yakalandı!")
