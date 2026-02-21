#!/bin/bash

# --- AYARLAR ---
# Sabit yol yerine bulunduğu klasörü kullanmasını sağlıyoruz
cd "$(dirname "$0")"

# Sistem yollarını tanımla
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Playlist Klasörünü Hazırla
mkdir -p playlist
rm -f playlist/*.m3u8

# --- KANALLARI İŞLE ---
echo ">>> Kanallar taranıyor..."

if [ -f "link.json" ]; then
    cat link.json | jq -c '.[]' | while read -r i; do
        name=$(echo "$i" | jq -r '.name')
        target_url=$(echo "$i" | jq -r '.url')
        
        echo ">>> $name güncelleniyor..."

        # Manifest linkini cımbızla
        raw_manifest=$(curl -i -s --max-time 30 "$target_url" | grep -o "https://manifest.googlevideo.com[^[:space:]\"']*" | head -n 1 | tr -d '\r\n')

        if [ ! -z "$raw_manifest" ] && [[ "$raw_manifest" == http* ]]; then
            cat <<EOF > "playlist/${name}.m3u8"
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=1280000,RESOLUTION=1280x720
$raw_manifest
EOF
            echo "   [OK] $name yazıldı."
        else
            echo "   [!] HATA: $name link bulunamadı."
        fi
        sleep 1
    done
fi

# --- ANA PLAYLIST (M3U) OLUŞTURMA ---
echo ">>> Ana playlist birleştiriliyor..."
echo "#EXTM3U" > playlist/playlist.m3u

for file in playlist/*.m3u8; do
    [ -s "$file" ] || continue
    fname=$(basename "$file" .m3u8)
    
    if grep -q "googlevideo" "$file"; then
        echo "#EXTINF:-1,$fname" >> playlist/playlist.m3u
        # BURAYI KENDİ REPO ADINA GÖRE DÜZELTTİM
        echo "https://raw.githubusercontent.com/phpxml/deneme/main/playlist/${fname}.m3u8?t=$(date +%s)" >> playlist/playlist.m3u
    fi
done
