"""
OBS API istemcisi - Tüm verileri çeker
"""

import os
import pickle
import json
import requests
from datetime import datetime
from colorama import Fore, Style


class OBSApi:
    """OBS API'lerine istek atan sınıf"""

    BASE = "https://obs.bilecik.edu.tr/ogrenci/ogrencianasayfa.aspx"

    def __init__(self, cookie_file="obs_cookies.pkl"):
        self.cookie_file = cookie_file
        self.cookies = self._cerezleri_yukle()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*",
            "Content-Type": "application/json; charset=utf-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://obs.bilecik.edu.tr/ogrenci/ogrencianasayfa.aspx",
        }
        self.veri = {}

    def _cerezleri_yukle(self):
        if not os.path.exists(self.cookie_file):
            raise FileNotFoundError(
                f"Çerez dosyası bulunamadı: {self.cookie_file}\n"
                f"Önce giriş yapın: python scripts/tum_verileri_cek.py --login"
            )
        with open(self.cookie_file, "rb") as f:
            cookies_list = pickle.load(f)

        return {c["name"]: c["value"] for c in cookies_list if "bilecik.edu.tr" in c.get("domain", "")}

    def _api(self, api_adi, payload=None):
        try:
            r = requests.post(
                f"{self.BASE}/{api_adi}",
                cookies=self.cookies,
                headers=self.headers,
                json=payload or {},
                timeout=15
            )
            if r.status_code == 200:
                data = r.json()
                if "d" in data:
                    try:
                        return json.loads(data["d"])
                    except:
                        return data["d"]
                return data
        except Exception as e:
            return {"error": str(e)}
        return None

    # ============ VERİ ÇEKME ============

    def ogrenci_bilgileri(self):
        return self._api("OgrenciAnasayfaVeriGetir")

    def notlar(self):
        return self._api("SinavNotGoruntule", {"OgrenciBolumKayitUid": "", "DonemNo": -1})

    def ders_programi(self):
        o = self.ogrenci_bilgileri()
        return self._api("OgrenciDersProgramiGetir", {
            "OgrenciBolumKayitUid": o.get("OgrenciBolumKayitUid", ""),
            "DonemNo": o.get("AktifDonemNo", 0)
        })

    def yil_donem(self):
        o = self.ogrenci_bilgileri()
        return self._api("YilDonemListesi", {"OgrenciBolumKayitUid": o.get("OgrenciBolumKayitUid", "")})

    def mesajlar(self):
        return self._api("MesajKutulariGetir")

    def duyurular(self):
        return self._api("OgrenciDuyuru")

    def takvim(self):
        return self._api("AkademikTakvimOzetGetir")

    def telefon(self):
        o = self.ogrenci_bilgileri()
        return self._api("OgrenciTelefonGetir", {"OgrenciBolumKayitUid": o.get("OgrenciBolumKayitUid", "")})

    # ============ TOPLU ÇEKME ============

    def tum_verileri_cek(self, kaydet=True):
        print(f"\n{Fore.CYAN}📥 OBS verileri çekiliyor...{Style.RESET_ALL}\n")

        self.veri = {
            "cekilme_tarihi": datetime.now().isoformat(),
            "ogrenci": self.ogrenci_bilgileri(),
            "notlar": self.notlar(),
            "ders_programi": self.ders_programi(),
            "yil_donem": self.yil_donem(),
            "telefon": self.telefon(),
            "mesajlar": self.mesajlar(),
            "duyurular": self.duyurular(),
            "takvim": self.takvim(),
        }

        if kaydet:
            with open("obs_veri.json", "w", encoding="utf-8") as f:
                json.dump(self.veri, f, indent=2, ensure_ascii=False)
            print(f"{Fore.GREEN}✅ Tüm veriler 'obs_veri.json' dosyasına kaydedildi.{Style.RESET_ALL}")

        return self.veri
