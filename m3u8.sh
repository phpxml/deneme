#!/bin/bash

# --- AYARLAR ---
# Senin GitHub deponun adı 'deneme' olduğu için dizini buna göre güncelledim
PROJE_DIR="/root/deneme"
cd $PROJE_DIR || { echo "Dizin bulunamadı!"; exit 1; }

# Sistem yollarını tanımla (Cron çalışırken hata almamak için)
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Git Güvenlik Ayarı: Ana dalda olduğumuzdan emin olalım
git checkout main || git checkout -b main

# Playlist Klasörünü Hazırla (Her seferinde temiz bir liste için)
mkdir -p playlist
rm -f playlist/*.m3u8

# --- KANALLARI İŞLE ---
echo ">>> Kanallar taranıyor ve Google Manifest linkleri alınıyor..."

cat link.json | jq -c '.[]' | while read -r i; do
    name=$(echo "$i" | jq -r '.name')
    target_url=$(echo "$i" | jq -r '.url')
    
    echo ">>> $name güncelleniyor..."

    raw_manifest=$(curl -i -s --max-time 30 "$target_url" | grep -o "https://manifest.googlevideo.com[^[:space:]\"']*" | head -n 1 | tr -d '\r\n')

    if [ ! -z "$raw_manifest" ] && [[ "$raw_manifest" == http* ]]; then
        cat <<EOF > "playlist/${name}.m3u8"
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=1280000,RESOLUTION=1280x720
$raw_manifest
EOF
        echo "   [OK] $name başarıyla dosyaya yazıldı."
    else
        echo "   [!] HATA: $name için link bulunamadı. Sunucu yanıt vermedi veya yayın kapalı."
    fi
    
    sleep 1
done

# --- ANA PLAYLIST (M3U) OLUŞTURMA ---
echo ">>> Ana playlist (m3u) birleştiriliyor..."
echo "#EXTM3U" > playlist/playlist.m3u

for file in playlist/*.m3u8; do
    [ -s "$file" ] || continue
    fname=$(basename "$file" .m3u8)
    
    if grep -q "googlevideo" "$file"; then
        echo "#EXTINF:-1,$fname" >> playlist/playlist.m3u
        # BURASI GÜNCELLENDİ: Kullanıcı adı 'phpxml', repo adı 'deneme' yapıldı
        echo "https://raw.githubusercontent.com/phpxml/deneme/main/playlist/${fname}.m3u8?t=$(date +%s)" >> playlist/playlist.m3u
    fi
done

# --- GITHUB PUSH ---
echo ">>> GitHub'a gönderiliyor..."
git add .
if ! git diff-index --quiet HEAD --; then
    git commit -m "Manifest Refresh: $(date +'%d-%m-%Y %H:%M')"
    git push origin HEAD:main --force
    echo ">>> İşlem Başarılı: GitHub güncellendi."
else
    echo ">>> Değişiklik yok, push atlandı."
fi
