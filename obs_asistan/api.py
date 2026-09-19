"""
OBS API istemcisi - Tüm verileri çeker
Çerez süresi dolduğunda otomatik yeniden giriş yapar
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
    
    def __init__(self, cookie_file="obs_cookies.pkl", otomatik_yenile=True):
        self.cookie_file = cookie_file
        self.otomatik_yenile = otomatik_yenile
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
        """Çerezleri yükler, yoksa otomatik giriş yapar"""
        if not os.path.exists(self.cookie_file):
            if self.otomatik_yenile:
                print(f"{Fore.YELLOW}⚠️  Çerez dosyası bulunamadı, giriş yapılıyor...{Style.RESET_ALL}")
                self._yeniden_giris_yap()
            else:
                raise FileNotFoundError(f"Çerez dosyası yok: {self.cookie_file}")
        
        with open(self.cookie_file, "rb") as f:
            cookies_list = pickle.load(f)
        
        return {c["name"]: c["value"] for c in cookies_list 
                if "bilecik.edu.tr" in c.get("domain", "")}
    
    def _yeniden_giris_yap(self):
        """Selenium ile yeniden giriş yapar ve çerezleri günceller"""
        from obs_asistan.giris import OBSGiris
        giris = OBSGiris(cookie_file=self.cookie_file)
        giris.interaktif_giris()
    
    def _api(self, api_adi, payload=None, _deneme=0):
        """API çağrısı yapar, 401 alırsa otomatik yeniden giriş yapar"""
        if _deneme > 1:
            return {"error": "Çerez yenileme başarısız"}
        
        try:
            r = requests.post(
                f"{self.BASE}/{api_adi}",
                cookies=self.cookies,
                headers=self.headers,
                json=payload or {},
                timeout=15
            )
            
            # 401 = çerez süresi dolmuş
            if r.status_code == 401:
                if self.otomatik_yenile:
                    print(f"\n{Fore.YELLOW}⚠️  Çerez süresi dolmuş! Yeniden giriş yapılıyor...{Style.RESET_ALL}")
                    self._yeniden_giris_yap()
                    self.cookies = self._cerezleri_yukle()
                    # Tekrar dene
                    return self._api(api_adi, payload, _deneme=_deneme + 1)
                else:
                    return {"error": "HTTP 401 - Çerez süresi dolmuş"}
            
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
