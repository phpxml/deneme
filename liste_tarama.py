import requests

def taramayi_baslat():
    # ANA SUNUCULAR (Senin paylaştığın o sağlam kaynaklar)
    sunucular = [
        "https://andro.okan9gote10sokan.cfd/checklist/", # <--- Checklist burada!
        "https://rmtftbjlne.turknet.ercdn.net/bpeytmnqyp/",
        "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/",
        "https://rkhubpaomb.turknet.ercdn.net/fwjkgpasof/"
    ]
    
    # 1. AŞAMA: HAZIR LİSTE DOSYASI VAR MI?
    liste_dosyalari = [
        "playlist.m3u", "playlist.m3u8", "channels.m3u", "channels.m3u8",
        "index.m3u8", "tv.m3u", "iptv.m3u", "liste.m3u", "all.m3u", "andro.m3u"
    ]

    # 2. AŞAMA: KANAL İSİM VARYASYONLARI
    kanallar = [
        "atv", "show", "showtv", "showmax", "tv8", "tv8bucuk", "a2tv", "a2",
        "trt1", "trthaber", "trtspor", "trtspor2", "trtbelgesel", "trtmuzik",
        "kanald", "star", "startv", "fox", "now", "teve2", "tlc", "dmax",
        "haberturk", "cnnturk", "ayayin", "ahaber", "aspor", "szctv", "halktv",
        "sozcutv", "ekotv", "tv100", "tgrthaber", "24tv", "ulketv", "tv4", "minikasocuk"
    ]
    
    bulunanlar = []
    print("Checklist ve Turknet sunucuları taranıyor...")

    # ÖNCE TOPLU LİSTE KONTROLÜ
    for s in sunucular:
        for l in liste_dosyalari:
            url = f"{s}{l}"
            try:
                r = requests.get(url, timeout=3)
                if r.status_code == 200 and "#EXTM3U" in r.text:
                    print(f"BULDUM! Toplu liste bulundu: {url}")
                    with open("atv.m3u", "w", encoding="utf-8") as f:
                        f.write(r.text)
                    return True
            except:
                continue

    # EĞER LİSTE YOKSA, MANUEL TARAMA (Suffix/Prefix Deneyerek)
    print("Toplu liste yok, kanallar tek tek aranıyor...")
    for kanal in kanallar:
        for s in sunucular:
            # Her sunucu tipi için farklı bir deneme mantığı
            if "andro" in s:
                # Andro sunucusu için 'androstreamlive' kalıbı
                denemeler = [f"androstreamlive{kanal}.m3u8", f"androstream{kanal}.m3u8", f"{kanal}.m3u8"]
            else:
                # Turknet sunucuları için klasör/dosya kalıbı
                denemeler = [f"{kanal}/{kanal}_720p.m3u8", f"{kanal}/{kanal}.m3u8", f"{kanal}/{kanal}_1080p.m3u8"]
            
            for d in denemeler:
                test_url = f"{s}{d}"
                try:
                    r = requests.head(test_url, timeout=2)
                    if r.status_code == 200:
                        print(f"YAKALANDI: {kanal.upper()} -> {test_url}")
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

