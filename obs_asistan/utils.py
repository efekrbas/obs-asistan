"""
Yardımcı fonksiyonlar
"""

import os
import pickle
from datetime import datetime
from colorama import Fore, Style


def cerez_kontrol(cookie_file="obs_cookies.pkl"):
    """Çerez dosyasının var olup olmadığını kontrol eder"""
    if not os.path.exists(cookie_file):
        print(f"{Fore.RED}❌ Çerez dosyası bulunamadı: {cookie_file}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Önce giriş yapın:{Style.RESET_ALL}")
        print(f"   python scripts/tum_verileri_cek.py --login")
        return False
    return True


def cerez_yasi(cookie_file="obs_cookies.pkl"):
    """Çerez dosyasının yaşını saat cinsinden döndürür"""
    if not os.path.exists(cookie_file):
        return None
    mtime = os.path.getmtime(cookie_file)
    yas_saat = (datetime.now().timestamp() - mtime) / 3600
    return round(yas_saat, 1)


def tarih_formatla(tarih_str):
    """ASP.NET tarih formatını okunabilir hale getirir"""
    if not tarih_str:
        return "—"
    try:
        # /Date(1756676100000)/ formatını parse et
        if "/Date(" in str(tarih_str):
            ms = int(str(tarih_str).split("(")[1].split(")")[0])
            return datetime.fromtimestamp(ms / 1000).strftime("%d.%m.%Y")
    except:
        pass
    return str(tarih_str)


def saat_formatla(saat_str):
    """08:00:00 -> 08:00"""
    if not saat_str:
        return "—"
    return str(saat_str)[:5]


def baslik_yazdir(baslik, karakter="=", uzunluk=60):
    """Renkli başlık yazdırır"""
    print(f"\n{Fore.CYAN}{karakter * uzunluk}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{baslik}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{karakter * uzunluk}{Style.RESET_ALL}")


def dosya_boyutu(dosya):
    """Dosya boyutunu okunabilir formatta döndürür"""
    if not os.path.exists(dosya):
        return "0 B"
    boyut = os.path.getsize(dosya)
    for birim in ["B", "KB", "MB", "GB"]:
        if boyut < 1024:
            return f"{boyut:.1f} {birim}"
        boyut /= 1024
    return f"{boyut:.1f} TB"
