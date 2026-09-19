#!/usr/bin/env python3
"""
OBS Asistan - Ana Script
"""

import sys
import os
import argparse

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colorama import Fore, Style, init
init(autoreset=True)

from obs_asistan.giris import OBSGiris
from obs_asistan.api import OBSApi
from obs_asistan.rapor import OBSRapor
from obs_asistan.notifications import Notifier
from obs_asistan.utils import cerez_kontrol, cerez_yasi, tarih_formatla, saat_formatla


BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   {Fore.YELLOW}OBS ASISTAN{Fore.CYAN} v1.0                                      ║
║   {Fore.GREEN}Öğrenci Bilgi Sistemi Otomasyonu{Fore.CYAN}                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""


def main():
    parser = argparse.ArgumentParser(
        description="OBS Asistan - Öğrenci Bilgi Sistemi Otomasyonu",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python scripts/tum_verileri_cek.py --login     # Giriş yap
  python scripts/tum_verileri_cek.py --tumu      # Tüm verileri çek
  python scripts/tum_verileri_cek.py --notlar    # Notları göster
  python scripts/tum_verileri_cek.py --program   # Ders programını göster
  python scripts/tum_verileri_cek.py --excel     # Excel raporu oluştur
  python scripts/tum_verileri_cek.py --html      # HTML raporu oluştur
  python scripts/tum_verileri_cek.py --takip     # Not takip modu
        """
    )
    parser.add_argument("--login", action="store_true", help="Giriş yap")
    parser.add_argument("--yenile", action="store_true", help="Çerezleri yenile")
    parser.add_argument("--tumu", action="store_true", help="Tüm verileri çek")
    parser.add_argument("--notlar", action="store_true", help="Notları göster")
    parser.add_argument("--program", action="store_true", help="Ders programını göster")
    parser.add_argument("--mesajlar", action="store_true", help="Mesajları göster")
    parser.add_argument("--duyurular", action="store_true", help="Duyuruları göster")
    parser.add_argument("--takvim", action="store_true", help="Akademik takvimi göster")
    parser.add_argument("--excel", action="store_true", help="Excel raporu oluştur")
    parser.add_argument("--html", action="store_true", help="HTML raporu oluştur")
    parser.add_argument("--takip", action="store_true", help="Not takip modu")
    
    args = parser.parse_args()
    print(BANNER)
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # Giriş / Yenile
    if args.login or args.yenile:
        # Eski çerezi sil
        if os.path.exists("obs_cookies.pkl"):
            os.remove("obs_cookies.pkl")
            print(f"{Fore.YELLOW}🗑️  Eski çerez silindi.{Style.RESET_ALL}")
        
        giris = OBSGiris()
        giris.interaktif_giris()
        return
    
    # Çerez kontrolü
    if not cerez_kontrol():
        return
    
    yas = cerez_yasi()
    if yas is not None:
        print(f"{Fore.CYAN}ℹ️  Çerez yaşı: {yas} saat{Style.RESET_ALL}\n")
    
    api = OBSApi()
    
    # ============ TÜM VERİLER ============
    if args.tumu:
        api.tum_verileri_cek()
        o = api.veri["ogrenci"]
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 ÖZET{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"  Ad Soyad    : {o.get('Ad')} {o.get('Soyad')}")
        print(f"  Öğrenci No  : {o.get('OgrenciNo')}")
        print(f"  Bölüm       : {o.get('BolumAd')}")
        print(f"  Sınıf       : {o.get('Sinif')}")
        print(f"  Ortalama    : {o.get('Ortalama')}")
        print(f"  Danışman    : {o.get('Danisman')}")
        print(f"  Aktif Dönem : {o.get('AktifYilAd')} {o.get('AktifDonemAd')}")
        print(f"  Mesaj       : {o.get('OkunmamisYeniMesajSayisi')} okunmamış")
    
    # ============ NOTLAR ============
    elif args.notlar:
        notlar = api.notlar()
        if isinstance(notlar, list):
            print(f"{Fore.YELLOW}📚 {len(notlar)} ders{Style.RESET_ALL}\n")
            for d in notlar:
                print(f"  {Fore.CYAN}{d['DersKodu']}{Style.RESET_ALL} - {d['DersAdi']}")
                print(f"     Hoca: {d['AkademikPersonelAd']}")
                print(f"     AKTS: {d['AKTS']} | Harf: {d['HarfNotu']}")
                for s in d.get("DegerlendimeListe", []):
                    not_d = s["Not"] if s["Not"] is not None else "—"
                    print(f"       • {s['TurAd']} (%{s['Yuzde']}): {not_d}")
                print()
    
    # ============ DERS PROGRAMI ============
    elif args.program:
        prog = api.ders_programi()
        if isinstance(prog, dict):
            print(f"{Fore.YELLOW}📅 {prog.get('baslik', '')}{Style.RESET_ALL}")
            print(f"   {prog.get('ogrenci', '')}\n")
            gunler = {}
            for s in prog.get("slotlar", []):
                gunler.setdefault(s["GunAdi"], []).append(s)
            for gun, slotlar in gunler.items():
                print(f"{Fore.CYAN}🔹 {gun}{Style.RESET_ALL}")
                for s in slotlar:
                    print(f"   {saat_formatla(s['Baslangic'])}-{saat_formatla(s['Bitis'])} | {s['Ders']} | {s['Derslik']}")
                print()
    
    # ============ MESAJLAR ============
    elif args.mesajlar:
        m = api.mesajlar()
        if isinstance(m, dict):
            gelen = m.get("Gelen", [])
            print(f"{Fore.YELLOW}💬 Mesajlar ({len(gelen)} gelen){Style.RESET_ALL}\n")
            for msg in gelen[:20]:
                okundu = "✅" if msg.get("OkunduMu") else "🔴"
                print(f"  {okundu} {msg.get('Gonderen', '')}: {msg.get('Konu', '')}")
            if len(gelen) > 20:
                print(f"\n  ... ve {len(gelen) - 20} mesaj daha")
    
    # ============ DUYURULAR ============
    elif args.duyurular:
        duyurular = api.duyurular()
        if isinstance(duyurular, list):
            print(f"{Fore.YELLOW}📢 Duyurular ({len(duyurular)}){Style.RESET_ALL}\n")
            for i, d in enumerate(duyurular[:15], 1):
                print(f"  {i}. {d.get('BaslikAd', '')}")
                print(f"     {tarih_formatla(d.get('SistemeEklenmeTarihi'))}")
                print()
    
    # ============ TAKVİM ============
    elif args.takvim:
        takvim = api.takvim()
        if isinstance(takvim, dict):
            ozet = takvim.get("ozet", [])
            print(f"{Fore.YELLOW}📅 Akademik Takvim ({len(ozet)} etkinlik){Style.RESET_ALL}\n")
            for t in ozet:
                aktif = "🔴" if t.get("Aktif") else "⚪"
                print(f"  {aktif} {t.get('Tarih', '')}")
                print(f"     {t.get('Aktivite', '')}")
                print()
    
    # ============ EXCEL ============
    elif args.excel:
        api.tum_verileri_cek(kaydet=False)
        rapor = OBSRapor(api.veri)
        rapor.excel_olustur()
    
    # ============ HTML ============
    elif args.html:
        api.tum_verileri_cek(kaydet=False)
        rapor = OBSRapor(api.veri)
        rapor.html_olustur()
    
    # ============ TAKİP ============
    elif args.takip:
        notifier = Notifier()
        notifier.not_takip_baslat(api, aralik_dakika=30)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Durduruldu.{Style.RESET_ALL}")
