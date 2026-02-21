import requests
from bs4 import BeautifulSoup
import datetime
import re

def start_hunting():
    # 1. Günün tarihini al ve URL'yi oluştur
    simdi = datetime.datetime.now()
    bugun_str = simdi.strftime("%d-%m-%Y")
    target_url = f"https://stbstalker.alaaeldinee.com/{simdi.year}/{simdi.month:02d}/smart-stb-emu-pro-{bugun_str}.html?m=1"
    
    print(f"[{bugun_str}] Sayfası kontrol ediliyor...")
    
    try:
        response = requests.get(target_url, timeout=10)
        if response.status_code != 200: return

        # 2. Sayfa içeriğini temizle ve verileri eşleştir
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()
        
        # Regex ile Panel, MAC ve Expire eşleşmelerini bul
        panels = re.findall(r'Panel\s*>\s*(http://[\w\.:/-]+)', content)
        macs = re.findall(r'Mac\s*>\s*([0-9A-F:]{17})', content)
        expires = re.findall(r'Expires\s*>\s*(.*?)\s*\(', content)

        with open("gunluk_calisanlar.txt", "w", encoding="utf-8") as f:
            f.write(f"--- {bugun_str} TARİHLİ ÇALIŞAN LİSTESİ ---\n")
            
            for p, m, e in zip(panels, macs, expires):
                # 3. Elle yaptığın testi kod yapsın (Timeout testi)
                try:
                    # Portalın canlı olup olmadığını 3 saniyede test eder
                    test = requests.get(p.rstrip('/'), timeout=3)
                    durum = "AKTİF" if test.status_code < 500 else "PASİF"
                except:
                    durum = "ERİŞİM YOK (Engel olabilir)"

                if durum == "AKTİF":
                    f.write(f"\nPORTAL : {p}\n")
                    f.write(f"MAC : {m}\n")
                    f.write(f"📆 Expired on : {e}\n")
                    f.write("-" * 30 + "\n")
        
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    start_hunting()

