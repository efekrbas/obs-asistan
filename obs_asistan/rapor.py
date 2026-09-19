"""
Rapor oluşturucu - Excel, HTML
"""

import os
import json
from datetime import datetime
from colorama import Fore, Style

try:
    import pandas as pd
    PANDAS_VAR = True
except ImportError:
    PANDAS_VAR = False

try:
    from jinja2 import Template
    JINJA_VAR = True
except ImportError:
    JINJA_VAR = False


class OBSRapor:
    """OBS verilerinden rapor oluşturan sınıf"""
    
    def __init__(self, veri):
        self.veri = veri
        self.tarih = datetime.now().strftime("%Y%m%d_%H%M")
    
    # ============ EXCEL RAPORU ============
    
    def excel_olustur(self, dosya_adi=None):
        """Tüm verileri Excel dosyasına aktarır"""
        if not PANDAS_VAR:
            print(f"{Fore.RED}❌ pandas kütüphanesi yok!{Style.RESET_ALL}")
            print(f"   pip install pandas openpyxl")
            return None
        
        dosya_adi = dosya_adi or f"obs_rapor_{self.tarih}.xlsx"
        
        print(f"{Fore.YELLOW}📊 Excel raporu oluşturuluyor...{Style.RESET_ALL}")
        
        with pd.ExcelWriter(dosya_adi, engine="openpyxl") as writer:
            
            # 1. Öğrenci Bilgileri
            o = self.veri.get("ogrenci", {})
            ogrenci_df = pd.DataFrame([{
                "Ad Soyad": f"{o.get('Ad', '')} {o.get('Soyad', '')}",
                "Öğrenci No": o.get("OgrenciNo"),
                "Bölüm": o.get("BolumAd"),
                "Fakülte/MYO": o.get("AkademikBirimAd"),
                "Sınıf": o.get("Sinif"),
                "Dönem": o.get("Donem"),
                "Ortalama": o.get("Ortalama"),
                "Danışman": o.get("Danisman"),
                "Aktif Yıl": o.get("AktifYilAd"),
                "Aktif Dönem": o.get("AktifDonemAd"),
            }])
            ogrenci_df.to_excel(writer, sheet_name="Öğrenci", index=False)
            
            # 2. Notlar
            notlar = self.veri.get("notlar", [])
            if isinstance(notlar, list):
                notlar_satirlar = []
                for ders in notlar:
                    for d in ders.get("DegerlendimeListe", []):
                        notlar_satirlar.append({
                            "Ders Kodu": ders.get("DersKodu"),
                            "Ders Adı": ders.get("DersAdi"),
                            "Hoca": ders.get("AkademikPersonelAd"),
                            "AKTS": ders.get("AKTS"),
                            "Sınav Türü": d.get("TurAd"),
                            "Yüzde": d.get("Yuzde"),
                            "Not": d.get("Not"),
                            "Sınıf Ort.": d.get("sinifOrtalamasi"),
                            "İlan Tarihi": d.get("IlanTarihi"),
                            "Harf Notu": ders.get("HarfNotu"),
                        })
                if notlar_satirlar:
                    pd.DataFrame(notlar_satirlar).to_excel(writer, sheet_name="Notlar", index=False)
            
            # 3. Ders Programı
            prog = self.veri.get("ders_programi", {})
            if isinstance(prog, dict) and prog.get("slotlar"):
                prog_df = pd.DataFrame(prog["slotlar"])[
                    ["GunAdi", "Baslangic", "Bitis", "Ders", "Derslik", "Hoca", "Tip"]
                ]
                prog_df.columns = ["Gün", "Başlangıç", "Bitiş", "Ders", "Derslik", "Hoca", "Tip"]
                prog_df.to_excel(writer, sheet_name="Ders Programı", index=False)
            
            # 4. Mesajlar
            m = self.veri.get("mesajlar", {})
            if isinstance(m, dict):
                gelen = m.get("Gelen", [])
                if gelen:
                    pd.DataFrame(gelen).to_excel(writer, sheet_name="Mesajlar", index=False)
            
            # 5. Duyurular
            duyurular = self.veri.get("duyurular", [])
            if isinstance(duyurular, list) and duyurular:
                pd.DataFrame(duyurular).to_excel(writer, sheet_name="Duyurular", index=False)
        
        print(f"{Fore.GREEN}✅ Excel raporu oluşturuldu: {dosya_adi}{Style.RESET_ALL}")
        return dosya_adi
    
    # ============ HTML RAPORU ============
    
    def html_olustur(self, dosya_adi=None):
        """Tüm verileri HTML dosyasına aktarır"""
        dosya_adi = dosya_adi or f"obs_rapor_{self.tarih}.html"
        
        print(f"{Fore.YELLOW}🌐 HTML raporu oluşturuluyor...{Style.RESET_ALL}")
        
        o = self.veri.get("ogrenci", {})
        notlar = self.veri.get("notlar", [])
        prog = self.veri.get("ders_programi", {})
        mesajlar = self.veri.get("mesajlar", {})
        duyurular = self.veri.get("duyurular", [])
        takvim = self.veri.get("takvim", {})
        
        html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>OBS Raporu - {o.get('Ad', '')} {o.get('Soyad', '')}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; color: #333; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{ background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        header p {{ opacity: 0.9; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .card h2 {{ color: #1e3c72; margin-bottom: 15px; border-bottom: 2px solid #eee; padding-bottom: 10px; font-size: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th {{ background: #1e3c72; color: white; padding: 10px; text-align: left; font-size: 14px; }}
        td {{ padding: 8px 10px; border-bottom: 1px solid #eee; font-size: 14px; }}
        tr:hover {{ background: #f8f9fa; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
        .info-item {{ padding: 10px; background: #f8f9fa; border-radius: 5px; }}
        .info-item strong {{ color: #1e3c72; }}
        .badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
        .badge-ok {{ background: #d4edda; color: #155724; }}
        .badge-no {{ background: #f8d7da; color: #721c24; }}
        footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>📊 OBS Raporu</h1>
        <p>{o.get('Ad', '')} {o.get('Soyad', '')} - {o.get('BolumAd', '')}</p>
        <p>Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
    </header>
    
    <div class="card">
        <h2>👤 Öğrenci Bilgileri</h2>
        <div class="info-grid">
            <div class="info-item"><strong>Ad Soyad:</strong> {o.get('Ad', '')} {o.get('Soyad', '')}</div>
            <div class="info-item"><strong>Öğrenci No:</strong> {o.get('OgrenciNo', '')}</div>
            <div class="info-item"><strong>Bölüm:</strong> {o.get('BolumAd', '')}</div>
            <div class="info-item"><strong>MYO/Fakülte:</strong> {o.get('AkademikBirimAd', '')}</div>
            <div class="info-item"><strong>Sınıf:</strong> {o.get('Sinif', '')}</div>
            <div class="info-item"><strong>Ortalama:</strong> {o.get('Ortalama', '')}</div>
            <div class="info-item"><strong>Danışman:</strong> {o.get('Danisman', '')}</div>
            <div class="info-item"><strong>Aktif Dönem:</strong> {o.get('AktifYilAd', '')} {o.get('AktifDonemAd', '')}</div>
        </div>
    </div>
"""
        
        # Notlar
        if isinstance(notlar, list):
            html += '<div class="card"><h2>📚 Notlar</h2><table><thead><tr><th>Ders Kodu</th><th>Ders Adı</th><th>Hoca</th><th>AKTS</th><th>Harf</th><th>Sınavlar</th></tr></thead><tbody>'
            for ders in notlar:
                sinavlar = ", ".join([f"{d['TurAd']}: {d['Not'] if d['Not'] is not None else '—'}" for d in ders.get("DegerlendimeListe", [])])
                html += f"<tr><td><strong>{ders.get('DersKodu', '')}</strong></td><td>{ders.get('DersAdi', '')}</td><td>{ders.get('AkademikPersonelAd', '')}</td><td>{ders.get('AKTS', '')}</td><td>{ders.get('HarfNotu', '-')}</td><td>{sinavlar}</td></tr>"
            html += '</tbody></table></div>'
        
        # Ders Programı
        if isinstance(prog, dict) and prog.get("slotlar"):
            gunler = {}
            for s in prog["slotlar"]:
                gunler.setdefault(s["GunAdi"], []).append(s)
            
            html += '<div class="card"><h2>📅 Ders Programı</h2>'
            for gun, slotlar in gunler.items():
                html += f'<h3 style="margin: 15px 0 5px 0; color: #2a5298;">{gun}</h3>'
                html += '<table><thead><tr><th>Saat</th><th>Ders</th><th>Derslik</th><th>Hoca</th></tr></thead><tbody>'
                for s in slotlar:
                    html += f"<tr><td>{s['Baslangic'][:5]}-{s['Bitis'][:5]}</td><td>{s.get('Ders', '')}</td><td>{s.get('Derslik', '')}</td><td>{s.get('Hoca', '')}</td></tr>"
                html += '</tbody></table>'
            html += '</div>'
        
        # Mesajlar
        if isinstance(mesajlar, dict) and mesajlar.get("Gelen"):
            html += '<div class="card"><h2>💬 Mesajlar</h2><table><thead><tr><th>Gönderen</th><th>Konu</th><th>Tarih</th><th>Durum</th></tr></thead><tbody>'
            for m in mesajlar["Gelen"][:30]:
                okundu = "Okundu" if m.get("OkunduMu") else "YENİ"
                badge = "badge-ok" if m.get("OkunduMu") else "badge-no"
                html += f"<tr><td>{m.get('Gonderen', '')}</td><td>{m.get('Konu', '')}</td><td>{m.get('Tarih', '')}</td><td><span class='badge {badge}'>{okundu}</span></td></tr>"
            html += '</tbody></table></div>'
        
        html += f"""
    <footer>
        <p>OBS Asistan v1.0 tarafından oluşturuldu</p>
        <p>Bu rapor bağımsız bir öğrenci projesi tarafından hazırlanmıştır.</p>
    </footer>
</div>
</body>
</html>"""
        
        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"{Fore.GREEN}✅ HTML raporu oluşturuldu: {dosya_adi}{Style.RESET_ALL}")
        return dosya_adi
