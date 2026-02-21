import requests

def taramayi_baslat():
    # ANA SUNUCULAR
    sunucular = [
        "https://andro.okan9gote10sokan.cfd/checklist/",
        "https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/",
        "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/",
        "https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof/"
    ]
    
    # KANAL İSİM VARYASYONLARI
    kanallar = [
        "atv", "show", "showtv", "showmax", "tv8", "tv8bucuk", "a2tv", "a2",
        "trt1", "trthaber", "trtspor", "trtspor2", "trtbelgesel", "trtmuzik",
        "kanald", "star", "startv", "fox", "now", "teve2", "tlc", "dmax",
        "haberturk", "cnnturk", "ayayin", "ahaber", "aspor", "szctv", "halktv",
        "sozcutv", "ekotv", "tv100", "tgrthaber", "24tv", "ulketv", "tv4"
    ]
    
    bulunanlar = []
    print("Tarama basliyor...")

    for s in sunucular:
        for kanal in kanallar:
            # Her sunucu için farklı format denemeleri
            if "andro" in s:
                denemeler = [f"androstreamlive{kanal}.m3u8", f"{kanal}.m3u8"]
            else:
                denemeler = [f"{kanal}/{kanal}_720p.m3u8", f"{kanal}/{kanal}.m3u8"]
            
            for d in denemeler:
                test_url = f"{s}{d}"
                try:
                    r = requests.head(test_url, timeout=2)
                    if r.status_code == 200:
                        print(f"BULDUM: {test_url}")
                        bulunanlar.append(f"#EXTINF:-1,{kanal.upper()}\n{test_url}")
                        break
                except:
                    continue

    if bulunanlar:
        with open("atv.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(bulunanlar))
        return True
    return False

if __name__ == "__main__":
    taramayi_baslat()
