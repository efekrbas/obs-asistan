# OBS Asistan

Herhangi bir üniversitenin Öğrenci Bilgi Sistemi (OBS) için Python tabanlı bir otomasyon aracıdır.

## ⚠️ Yasal Uyarı

Bu proje **bağımsız bir öğrenci projesidir**. Herhangi bir üniversiteyle resmi bağlantısı yoktur. Sadece kendi hesabınızla kullanmanız amaçlanmıştır.

## ✨ Özellikler

- 🔐 Selenium ile otomatik giriş
- 📚 Notları çekme
- 📅 Ders programını çekme
- 💬 Mesajları listeleme
- 📢 Duyuruları takip etme
- 📆 Akademik takvim

## 🚀 Kurulum

```bash
pip install -r requirements.txt
```

## 📖 Kullanım

```bash
# Giriş yap
python scripts/tum_verileri_cek.py --login

# Tüm verileri çek
python scripts/tum_verileri_cek.py --tumu

# Notları göster
python scripts/tum_verileri_cek.py --notlar

# Ders programını göster
python scripts/tum_verileri_cek.py --program

# Mesajları göster
python scripts/tum_verileri_cek.py --mesajlar
```

## 📜 Lisans

MIT License
