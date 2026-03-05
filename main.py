import requests, base64, re, os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.utils import platform

# --- AYARLAR ---
REPO = "phpxml/hab"
BASE_PATH = "/sdcard/Documents/Github/Handy/"
TOKEN_FILE = BASE_PATH + "config.txt"
FILE1, LOCAL1 = "test.m3u", BASE_PATH + "test.txt"
FILE2, LOCAL2 = "test2.m3u", BASE_PATH + "test2.txt"

def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

class HandyControlApp(App):
    def build(self):
        # Ana Arka Plan
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        # Durum Göstergesi (Güncelleme sayısı burada görünecek)
        self.label = Label(text="İşlem Bekleniyor...", font_size='20sp', size_hint=(1, 0.2))
        
        # Ana Butonlar
        btn1 = Button(text="TEST GÜNCELLE", size_hint=(1, 0.2), background_color=(0.1, 0.5, 0.8, 1))
        btn1.bind(on_press=lambda x: self.islem(FILE1, LOCAL1, "aralik"))
        
        btn2 = Button(text="TEST 2 GÜNCELLE", size_hint=(1, 0.2), background_color=(0.8, 0.4, 0.1, 1))
        btn2.bind(on_press=lambda x: self.islem(FILE2, LOCAL2, "sifirla"))

        # Düzenleme Butonu
        btn_edit = Button(text="DOSYALARI DÜZENLE", size_hint=(1, 0.15), background_color=(0.3, 0.3, 0.3, 1))
        btn_edit.bind(on_press=self.show_edit_menu)

        # Alt Satır (INFO ve ÇIKIŞ)
        bottom_row = BoxLayout(spacing=10, size_hint=(1, 0.15))
        
        btn_info = Button(text="INFO", background_color=(0.4, 0.2, 0.5, 1))
        btn_info.bind(on_press=self.show_info)
        
        btn_exit = Button(text="ÇIKIŞ", background_color=(0.7, 0.1, 0.1, 1))
        btn_exit.bind(on_press=self.stop)

        bottom_row.add_widget(btn_info)
        bottom_row.add_widget(btn_exit)

        # Ekleme sırası (Versiyon etiketi buradan kaldırıldı)
        self.layout.add_widget(self.label)
        self.layout.add_widget(btn1)
        self.layout.add_widget(btn2)
        self.layout.add_widget(btn_edit)
        self.layout.add_widget(bottom_row)
        
        return self.layout

    def show_edit_menu(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        p = Popup(title='Dosya Seçin', content=content, size_hint=(0.8, 0.5))
        
        b1 = Button(text="test.txt Düzenle"); b1.bind(on_press=lambda x: [self.dosya_ac(LOCAL1), p.dismiss()])
        b2 = Button(text="test2.txt Düzenle"); b2.bind(on_press=lambda x: [self.dosya_ac(LOCAL2), p.dismiss()])
        bc = Button(text="config.txt (Token)"); bc.bind(on_press=lambda x: [self.dosya_ac(TOKEN_FILE), p.dismiss()])
        
        content.add_widget(b1); content.add_widget(b2); content.add_widget(bc)
        p.open()

    def show_info(self, instance):
        # İstediğin versiyon bilgisi ve dosya yolları
        info_text = (
            "[b]Berlin 2026 ver : 1.0[/b]\n\n"
            "[b]KLASÖR YOLU:[/b]\n"
            f"{BASE_PATH}\n\n"
            "[b]DOSYALAR:[/b]\n"
            "• config.txt (Token)\n"
            "• test.txt\n"
            "• test2.txt"
        )
        msg = Label(text=info_text, markup=True, halign='center', font_size='14sp')
        btn = Button(text="KAPAT", size_hint=(1, 0.25))
        box = BoxLayout(orientation='vertical', padding=20, spacing=10)
        box.add_widget(msg); box.add_widget(btn)
        
        popup = Popup(title='Bilgi', content=box, size_hint=(0.85, 0.65))
        btn.bind(on_press=popup.dismiss)
        popup.open()

    def islem(self, github_file, local_file, mod):
        self.label.text = "Güncelleniyor..."
        token = get_token()
        if not token: 
            self.label.text = "HATA: Token bulunamadı!"
            return

        headers = {"Authorization": f"token {token}"}
        url = f"https://api.github.com/repos/{REPO}/contents/{github_file}"

        try:
            r = requests.get(url, headers=headers)
            sha = r.json()['sha'] if r.status_code == 200 else None
            content_old = base64.b64decode(r.json()['content']).decode('utf-8') if r.status_code == 200 else ""
            
            if not os.path.exists(local_file):
                self.label.text = f"HATA: {os.path.basename(local_file)} yok!"
                return

            with open(local_file, "r", encoding="utf-8") as f:
                yerel = f.read().strip()

            # Güncelleme sayısını bul ve artır
            match = re.search(r"Kopya Sayisi: (\d+)", content_old)
            new_count = (int(match.group(1)) + 1) if match else 1

            if mod == "aralik":
                pattern = r"handy_update_giris.*?handy_update_cikis"
                yeni_blog = f"handy_update_giris\n# Kopya Sayisi: {new_count}\n\n{yerel}\n\nhandy_update_cikis"
                yeni_icerik = re.sub(pattern, yeni_blog, content_old, flags=re.DOTALL) if re.search(pattern, content_old, flags=re.DOTALL) else f"{content_old}\n\n{yeni_blog}"
            else:
                yeni_icerik = f"# Kopya Sayisi: {new_count}\n\n{yerel}"

            payload = {
                "message": f"Update {new_count}",
                "content": base64.b64encode(yeni_icerik.encode('utf-8')).decode('utf-8'),
                "sha": sha
            } if sha else {
                "message": "Initial",
                "content": base64.b64encode(yeni_icerik.encode('utf-8')).decode('utf-8')
            }

            res = requests.put(url, json=payload, headers=headers)
            if res.status_code in [200, 201]:
                self.label.text = f"BAŞARILI! (Kopya: {new_count})"
            else:
                self.label.text = f"Hata Kodu: {res.status_code}"
        except Exception as e:
            self.label.text = f"Hata: {str(e)[:20]}"

    def dosya_ac(self, yol):
        if platform == 'android':
            try:
                from jnius import autoclass, cast
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                File = autoclass('java.io.File')
                
                file = File(yol)
                uri = Uri.fromFile(file)
                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(uri, "text/plain")
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                
                chooser = Intent.createChooser(intent, cast('java.lang.CharSequence', autoclass('java.lang.String')("Düzenleyici Seçin")))
                currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
                currentActivity.startActivity(chooser)
            except Exception as e:
                self.label.text = "Seçici başlatılamadı."
        else:
            self.label.text = f"Açılıyor: {os.path.basename(yol)}"

if __name__ == "__main__":
    HandyControlApp().run()
