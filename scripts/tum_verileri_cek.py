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


def main():
    parser = argparse.ArgumentParser(description="OBS Asistan")
    parser.add_argument("--login", action="store_true", help="Giriş yap")
    parser.add_argument("--tumu", action="store_true", help="Tüm verileri çek")
    parser.add_argument("--notlar", action="store_true", help="Notları göster")
    parser.add_argument("--program", action="store_true", help="Ders programını göster")
    parser.add_argument("--mesajlar", action="store_true", help="Mesajları göster")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    if args.login:
        giris = OBSGiris()
        giris.interaktif_giris()
        return

    if not os.path.exists("obs_cookies.pkl"):
        print(f"{Fore.RED}❌ Çerez dosyası yok! Önce giriş yapın:{Style.RESET_ALL}")
        print(f"   python scripts/tum_verileri_cek.py --login")
        return

    api = OBSApi()

    if args.tumu:
        api.tum_verileri_cek()
        o = api.veri["ogrenci"]
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 ÖZET{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"  Ad Soyad     : {o.get('Ad')} {o.get('Soyad')}")
        print(f"  Öğrenci No   : {o.get('OgrenciNo')}")
        print(f"  Bölüm        : {o.get('BolumAd')}")
        print(f"  Sınıf        : {o.get('Sinif')}")
        print(f"  Ortalama     : {o.get('Ortalama')}")
        print(f"  Danışman     : {o.get('Danisman')}")
        print(f"  Aktif Dönem  : {o.get('AktifYilAd')} {o.get('AktifDonemAd')}")

    elif args.notlar:
        notlar = api.notlar()
        if isinstance(notlar, list):
            print(f"{Fore.YELLOW}📚 {len(notlar)} ders{Style.RESET_ALL}\n")
            for d in notlar:
                print(f"  {Fore.CYAN}{d['DersKodu']}{Style.RESET_ALL} - {d['DersAdi']}")
                print(f"  Hoca: {d['AkademikPersonelAd']}")
                print(f"  AKTS: {d['AKTS']} | Harf: {d['HarfNotu']}\n")

    elif args.program:
        prog = api.ders_programi()
        if isinstance(prog, dict):
            print(f"{Fore.YELLOW}📅 {prog.get('baslik', '')}{Style.RESET_ALL}\n")
            gunler = {}
            for s in prog.get("slotlar", []):
                gunler.setdefault(s["GunAdi"], []).append(s)

            for gun, slotlar in gunler.items():
                print(f"{Fore.CYAN}🔹 {gun}{Style.RESET_ALL}")
                for s in slotlar:
                    print(f"   {s['Baslangic'][:5]}-{s['Bitis'][:5]} | {s['Ders']} | {s['Derslik']}")
                print()

    elif args.mesajlar:
        m = api.mesajlar()
        if isinstance(m, dict):
            print(f"{Fore.YELLOW}💬 Mesajlar{Style.RESET_ALL}\n")
            print(f"  Gelen: {len(m.get('Gelen', []))}")
            print(f"  Giden: {len(m.get('Giden', []))}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ Durduruldu.{Style.RESET_ALL}")
