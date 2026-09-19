"""
Bildirim sistemi - Not takip
"""

import os
import json
import time
import requests
from datetime import datetime
from colorama import Fore, Style


class Notifier:
    """Bildirim gönderen sınıf"""
    
    def __init__(self, config_file="config.json"):
        self.config = self._config_yukle(config_file)
    
    def _config_yukle(self, dosya):
        if os.path.exists(dosya):
            with open(dosya, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    # ============ TELEGRAM ============
    
    def telegram_gonder(self, mesaj):
        """Telegram'a mesaj gönderir"""
        token = self.config.get("telegram_token")
        chat_id = self.config.get("telegram_chat_id")
        
        if not token or not chat_id:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            r = requests.post(url, json={
                "chat_id": chat_id,
                "text": mesaj,
                "parse_mode": "HTML"
            }, timeout=10)
            return r.status_code == 200
        except:
            return False
    
    # ============ NOT TAKİP ============
    
    def not_takip_baslat(self, api, aralik_dakika=30):
        """Notları belirli aralıklarla kontrol eder"""
        print(f"{Fore.CYAN}🔔 Not Takip Modu{Style.RESET_ALL}")
        print(f"   Kontrol aralığı: {aralik_dakika} dakika")
        print(f"   Durdurmak için: Ctrl+C\n")
        
        onceki_notlar = self._son_notlari_yukle()
        
        while True:
            try:
                print(f"{Fore.YELLOW}⏰ {datetime.now().strftime('%H:%M:%S')} - Kontrol ediliyor...{Style.RESET_ALL}")
                
                notlar = api.notlar()
                if not isinstance(notlar, list):
                    print(f"{Fore.RED}   ❌ Notlar alınamadı{Style.RESET_ALL}")
                    time.sleep(aralik_dakika * 60)
                    continue
                
                # Yeni açıklanan notları bul
                yeni_notlar = []
                for ders in notlar:
                    ders_kodu = ders.get("DersKodu")
                    for d in ders.get("DegerlendimeListe", []):
                        if d.get("Not") is not None:
                            anahtar = f"{ders_kodu}_{d.get('TurAd')}"
                            if anahtar not in onceki_notlar:
                                yeni_notlar.append({
                                    "ders": f"{ders_kodu} - {ders.get('DersAdi')}",
                                    "sinav": d.get("TurAd"),
                                    "not": d.get("Not"),
                                })
                                onceki_notlar[anahtar] = d.get("Not")
                
                if yeni_notlar:
                    print(f"{Fore.GREEN}   🎉 {len(yeni_notlar)} yeni not açıklandı!{Style.RESET_ALL}")
                    
                    mesaj = "🎉 <b>Yeni Not Açıklandı!</b>\n\n"
                    for n in yeni_notlar:
                        print(f"      • {n['ders']} | {n['sinav']}: {n['not']}")
                        mesaj += f"📚 <b>{n['ders']}</b>\n   {n['sinav']}: <b>{n['not']}</b>\n\n"
                    
                    self.telegram_gonder(mesaj)
                    self._son_notlari_kaydet(onceki_notlar)
                else:
                    print(f"{Fore.CYAN}   ℹ️  Yeni not yok{Style.RESET_ALL}")
                
                time.sleep(aralik_dakika * 60)
            
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}⚠️  Takip durduruldu.{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}   ❌ Hata: {e}{Style.RESET_ALL}")
                time.sleep(60)
    
    def _son_notlari_yukle(self):
        if os.path.exists("son_notlar.json"):
            with open("son_notlar.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _son_notlari_kaydet(self, notlar):
        with open("son_notlar.json", "w", encoding="utf-8") as f:
            json.dump(notlar, f, ensure_ascii=False, indent=2)
