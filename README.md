# OBS Asistan

Herhangi bir üniversitenin Öğrenci Bilgi Sistemi (OBS) için Python tabanlı modern bir otomasyon ve raporlama aracıdır.

## ⚠️ Yasal Uyarı

Bu proje **bağımsız bir öğrenci projesidir**. Herhangi bir üniversiteyle resmi bağlantısı yoktur. Sadece kendi hesabınızla kişisel amaçlarla kullanmanız amaçlanmıştır.

## ✨ Özellikler

- 🔐 **Otomatik & Güvenli Giriş**: Selenium ile OBS'ye giriş, şifrelenmiş oturum çerezlerini yerel olarak saklama ve süresi dolduğunda otomatik yenileme.
- 📚 **Not Takibi & Görüntüleme**: Dönem derslerini, sınav türlerini (vize, final, ödev vb.), notları ve harf notlarını anlık listeleme.
- 📅 **Ders Programı**: Haftalık ders saatlerini, derslikleri ve öğretim elemanlarını düzenli şekilde görüntüleme.
- 💬 **Mesajlar**: OBS gelen kutusundaki mesajları ve okunma durumlarını takip etme.
- 📢 **Duyurular**: Üniversite duyurularını HTML temizliği ile listeleme ve `--duyuru-detay` ile tam metin okuma.
- 📆 **Akademik Takvim**: Güncel akademik takvim etkinliklerini ve durumlarını görme.
- 📊 **Excel Raporu (.xlsx)**: Tüm OBS verilerini (Öğrenci, Notlar, Ders Programı, Mesajlar, Duyurular, Takvim) sekmelere ayrılmış tek bir Excel tablosuna aktarma.
- 🌐 **Modern HTML Raporu (.html)**: Şık, mobil uyumlu ve temiz bir web arayüzünde tüm verileri tek tıkla raporlama.
- 🔔 **Periyodik Not Takip Modu & Telegram Bildirimi**: Arka planda çalışarak yeni bir sınav notu açıklandığı anda notu anında yakalama.

## 🚀 Kurulum

```bash
pip install -r requirements.txt
```

## 📖 Kullanım

```bash
# Giriş yap / Çerezleri yenile
python scripts/tum_verileri_cek.py --login

# Tüm verileri çek ve özet göster
python scripts/tum_verileri_cek.py --tumu

# Notları listele
python scripts/tum_verileri_cek.py --notlar

# Ders programını görüntüle
python scripts/tum_verileri_cek.py --program

# Gelen mesajları listele
python scripts/tum_verileri_cek.py --mesajlar

# Duyuruları listele
python scripts/tum_verileri_cek.py --duyurular

# Belirli bir duyurunun tam metnini oku
python scripts/tum_verileri_cek.py --duyuru-detay 1

# Akademik takvimi listele
python scripts/tum_verileri_cek.py --takvim

# Excel (.xlsx) raporu oluştur
python scripts/tum_verileri_cek.py --excel

# HTML (.html) web raporu oluştur
python scripts/tum_verileri_cek.py --html

# Yeni not takip modunu başlat (Varsayılan 30 dk)
python scripts/tum_verileri_cek.py --takip
```

## ⚙️ Yapılandırma (Opsiyonel)

Telegram üzerinden anlık bildirim almak isterseniz:
1. `config.example.json` dosyasını `config.json` olarak kopyalayın.
2. BotFather'dan aldığınız token'ı ve Chat ID'nizi girin.
*(Not: `config.json` dosyası `.gitignore` ile korunmaktadır ve asla GitHub'a gitmez.)*

## 📜 Lisans

MIT License
