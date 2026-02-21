import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Gerçek bir Chrome tarayıcı açıyoruz (IDM gibi)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Ağ trafiğini dinlemeye başlıyoruz (Sniffing)
        found_url = None

        async def intercept_request(request):
            nonlocal found_url
            # Player'ın sunucuya attığı o nihai m3u8 isteğini yakalıyoruz
            if ".m3u8" in request.url and "atv" in request.url:
                found_url = request.url

        page.on("request", intercept_request)

        # Sayfaya gidiyoruz ve player'ın yüklenmesini bekliyoruz
        await page.goto("https://www.atv.com.tr/canli-yayin", wait_until="networkidle")
        
        # Player'ın linki oluşturması için biraz süre tanıyalım
        await asyncio.sleep(10) 

        if found_url:
            with open("atv.m3u", "w") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1,ATV HD\n{found_url}\n")
            print(f"IDM Mantığı Başarılı! Link Yakalandı: {found_url}")
        else:
            print("Link bulunamadı, tarayıcı trafiği göremedi.")
            exit(1)

        await browser.close()

asyncio.run(run())

