# OBS Asistan 🎓

Herhangi bir üniversitenin Öğrenci Bilgi Sistemi (OBS) için Python tabanlı modern bir otomasyon, veri çekme ve raporlama aracıdır.

## ⚠️ Yasal Uyarı

Bu proje **bağımsız bir öğrenci projesidir**. Herhangi bir üniversiteyle resmi bir bağlantısı veya ortaklığı yoktur. Yalnızca kendi hesabınızla kişisel amaçlarla eğitim/otomasyon amaçlı kullanılması hedeflenmiştir.

---

## ⚡ 3 Adımda Hızlı Başlangıç

```bash
# 1. Projeyi klonlayın ve klasöre girin
git clone https://github.com/efekrbas/obs-asistan.git
cd obs-asistan

# 2. Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# 3. Giriş yapın (Çerezleri kaydedin)
python scripts/tum_verileri_cek.py --login
```

---

## 📋 Sistem Gereksinimleri

- **Python 3.8+**
- **Google Chrome** (Selenium ile otomatik giriş için gereklidir)

---

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

---

## 📖 Kullanım ve Komutlar

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

# Belirli bir duyurunun tam metnini oku (Örn: 1. duyuru)
python scripts/tum_verileri_cek.py --duyuru-detay 1

# Akademik takvimi listele
python scripts/tum_verileri_cek.py --takvim

# Excel (.xlsx) raporu oluştur
python scripts/tum_verileri_cek.py --excel

# HTML (.html) web raporu oluştur
python scripts/tum_verileri_cek.py --html

# Yeni not takip modunu başlat (Varsayılan 30 dk aralıkla)
python scripts/tum_verileri_cek.py --takip
```

---

## ⚙️ Yapılandırma (Opsiyonel Telegram Bildirimi)

Yeni not açıklandığında doğrudan Telegram'dan bildirim almak isterseniz:
1. `config.example.json` dosyasını `config.json` olarak kopyalayın:
   ```bash
   cp config.example.json config.json
   ```
2. `@BotFather` üzerinden aldığınız bot token'ınızı ve Chat ID'nizi `config.json` dosyasına yazın.
> 🔒 **Gizlilik Notu:** `config.json`, çerez dosyaları ve oluşturulan tüm raporlar `.gitignore` ile korunmaktadır, asla GitHub'a gitmez.

---

## 📜 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
