"""
Rapor oluşturucu - Excel, HTML
"""

import os
import json
import re
import html as html_lib
from datetime import datetime
from colorama import Fore, Style
from obs_asistan.utils import tarih_formatla, saat_formatla

try:
    import pandas as pd
    PANDAS_VAR = True
except ImportError:
    PANDAS_VAR = False


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
                    degerlendirmeler = ders.get("DegerlendimeListe", [])
                    if degerlendirmeler:
                        for d in degerlendirmeler:
                            notlar_satirlar.append({
                                "Ders Kodu": ders.get("DersKodu"),
                                "Ders Adı": ders.get("DersAdi"),
                                "Hoca": ders.get("AkademikPersonelAd"),
                                "AKTS": ders.get("AKTS"),
                                "Sınav Türü": d.get("TurAd"),
                                "Yüzde": d.get("Yuzde"),
                                "Not": d.get("Not"),
                                "Sınıf Ort.": d.get("sinifOrtalamasi"),
                                "İlan Tarihi": tarih_formatla(d.get("IlanTarihi")),
                                "Harf Notu": ders.get("HarfNotu") or "—",
                            })
                    else:
                        notlar_satirlar.append({
                            "Ders Kodu": ders.get("DersKodu"),
                            "Ders Adı": ders.get("DersAdi"),
                            "Hoca": ders.get("AkademikPersonelAd"),
                            "AKTS": ders.get("AKTS"),
                            "Sınav Türü": "—",
                            "Yüzde": "—",
                            "Not": "—",
                            "Sınıf Ort.": "—",
                            "İlan Tarihi": "—",
                            "Harf Notu": ders.get("HarfNotu") or "—",
                        })
                if notlar_satirlar:
                    pd.DataFrame(notlar_satirlar).to_excel(writer, sheet_name="Notlar", index=False)
            
            # 3. Ders Programı
            prog = self.veri.get("ders_programi", {})
            if isinstance(prog, dict) and prog.get("slotlar"):
                prog_satirlar = []
                for s in prog["slotlar"]:
                    prog_satirlar.append({
                        "Gün": s.get("GunAdi", ""),
                        "Başlangıç": saat_formatla(s.get("Baslangic")),
                        "Bitiş": saat_formatla(s.get("Bitis")),
                        "Ders": s.get("Ders", ""),
                        "Derslik": s.get("Derslik", ""),
                        "Hoca": s.get("Hoca", ""),
                        "Tip": s.get("Tip", "")
                    })
                pd.DataFrame(prog_satirlar).to_excel(writer, sheet_name="Ders Programı", index=False)
            
            # 4. Mesajlar
            m = self.veri.get("mesajlar", {})
            if isinstance(m, dict):
                gelen = m.get("Gelen", [])
                if gelen:
                    mesaj_satirlar = []
                    for msg in gelen:
                        mesaj_satirlar.append({
                            "Gönderen": msg.get("Gonderen", ""),
                            "Konu": msg.get("Konu", ""),
                            "Tarih": tarih_formatla(msg.get("Tarih")),
                            "Durum": "Okundu" if msg.get("OkunduMu") else "YENİ",
                        })
                    pd.DataFrame(mesaj_satirlar).to_excel(writer, sheet_name="Mesajlar", index=False)
            
            # 5. Duyurular
            duyurular = self.veri.get("duyurular", [])
            if isinstance(duyurular, list) and duyurular:
                duyuru_satirlar = []
                for d in duyurular:
                    ozet = re.sub(r'<[^>]+>', '', d.get('Ozet', ''))
                    ozet = html_lib.unescape(ozet).strip()
                    duyuru_satirlar.append({
                        "Başlık": d.get("BaslikAd", ""),
                        "Tarih": tarih_formatla(d.get("SistemeEklenmeTarihi")),
                        "Özet": ozet
                    })
                pd.DataFrame(duyuru_satirlar).to_excel(writer, sheet_name="Duyurular", index=False)
            
            # 6. Akademik Takvim
            takvim = self.veri.get("takvim", {})
            if isinstance(takvim, dict):
                ozet = takvim.get("ozet", [])
                if ozet:
                    takvim_satirlar = []
                    for t in ozet:
                        takvim_satirlar.append({
                            "Tarih": t.get("Tarih", ""),
                            "Aktivite": t.get("Aktivite", ""),
                            "Durum": "Aktif" if t.get("Aktif") else "Tamamlandı"
                        })
                    pd.DataFrame(takvim_satirlar).to_excel(writer, sheet_name="Akademik Takvim", index=False)
        
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
        
        ad_soyad = f"{o.get('Ad', '')} {o.get('Soyad', '')}".strip()
        
        html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OBS Raporu - {ad_soyad}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f4f6f9; color: #2d3748; padding: 24px; line-height: 1.5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{ background: linear-gradient(135deg, #1a365d, #2b6cb0); color: white; padding: 32px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        header h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 8px; }}
        header p {{ opacity: 0.92; font-size: 15px; }}
        .card {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }}
        .card h2 {{ color: #1a365d; margin-bottom: 16px; border-bottom: 2px solid #edf2f7; padding-bottom: 12px; font-size: 20px; font-weight: 600; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th {{ background: #2b6cb0; color: white; padding: 12px 14px; text-align: left; font-size: 14px; font-weight: 600; }}
        td {{ padding: 10px 14px; border-bottom: 1px solid #edf2f7; font-size: 14px; vertical-align: top; }}
        tr:hover {{ background: #f7fafc; }}
        .info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }}
        .info-item {{ padding: 12px 16px; background: #f8fafc; border-radius: 8px; border: 1px solid #edf2f7; }}
        .info-item strong {{ color: #2b6cb0; display: inline-block; min-width: 105px; }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; text-align: center; }}
        .badge-ok {{ background: #c6f6d5; color: #22543d; }}
        .badge-no {{ background: #fed7d7; color: #742a2a; }}
        .badge-active {{ background: #feebc8; color: #7b341e; }}
        .announcement-item {{ padding: 14px; border-bottom: 1px solid #edf2f7; }}
        .announcement-item:last-child {{ border-bottom: none; }}
        .announcement-title {{ font-weight: 600; color: #2b6cb0; font-size: 15px; margin-bottom: 4px; }}
        .announcement-date {{ font-size: 12px; color: #718096; margin-bottom: 6px; }}
        .announcement-body {{ font-size: 13px; color: #4a5568; }}
        footer {{ text-align: center; padding: 24px; color: #718096; font-size: 13px; }}
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>📊 OBS Öğrenci Raporu</h1>
        <p>{ad_soyad} • {o.get('BolumAd', '')}</p>
        <p>Rapor Oluşturulma Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
    </header>
    
    <div class="card">
        <h2>👤 Öğrenci Bilgileri</h2>
        <div class="info-grid">
            <div class="info-item"><strong>Ad Soyad:</strong> {ad_soyad}</div>
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
                degerlendirmeler = ders.get("DegerlendimeListe", [])
                if degerlendirmeler:
                    sinavlar = ", ".join([f"{d['TurAd']}: {d['Not'] if d['Not'] is not None else '—'}" for d in degerlendirmeler])
                else:
                    sinavlar = "<span style='color:#a0aec0;'>Henüz sınav girilmedi</span>"
                harf = ders.get('HarfNotu') or '—'
                html += f"<tr><td><strong>{ders.get('DersKodu', '')}</strong></td><td>{ders.get('DersAdi', '')}</td><td>{ders.get('AkademikPersonelAd', '')}</td><td>{ders.get('AKTS', '')}</td><td><strong>{harf}</strong></td><td>{sinavlar}</td></tr>"
            html += '</tbody></table></div>'
        
        # Ders Programı
        if isinstance(prog, dict) and prog.get("slotlar"):
            gunler = {}
            for s in prog["slotlar"]:
                gunler.setdefault(s["GunAdi"], []).append(s)
            
            html += '<div class="card"><h2>📅 Ders Programı</h2>'
            for gun, slotlar in gunler.items():
                html += f'<h3 style="margin: 18px 0 8px 0; color: #2b6cb0;">🔹 {gun}</h3>'
                html += '<table><thead><tr><th>Saat</th><th>Ders</th><th>Derslik</th><th>Hoca</th></tr></thead><tbody>'
                for s in slotlar:
                    saat_bas = saat_formatla(s.get('Baslangic'))
                    saat_bit = saat_formatla(s.get('Bitis'))
                    html += f"<tr><td><strong>{saat_bas} - {saat_bit}</strong></td><td>{s.get('Ders', '')}</td><td>{s.get('Derslik', '')}</td><td>{s.get('Hoca', '')}</td></tr>"
                html += '</tbody></table>'
            html += '</div>'
        
        # Mesajlar
        if isinstance(mesajlar, dict) and mesajlar.get("Gelen"):
            html += '<div class="card"><h2>💬 Gelen Mesajlar</h2><table><thead><tr><th>Gönderen</th><th>Konu</th><th>Tarih</th><th>Durum</th></tr></thead><tbody>'
            for m in mesajlar["Gelen"][:30]:
                okundu = "Okundu" if m.get("OkunduMu") else "YENİ"
                badge = "badge-ok" if m.get("OkunduMu") else "badge-no"
                tarih_str = tarih_formatla(m.get('Tarih', ''))
                html += f"<tr><td><strong>{m.get('Gonderen', '')}</strong></td><td>{m.get('Konu', '')}</td><td>{tarih_str}</td><td><span class='badge {badge}'>{okundu}</span></td></tr>"
            html += '</tbody></table></div>'
        
        # Duyurular
        if isinstance(duyurular, list) and duyurular:
            html += '<div class="card"><h2>📢 Son Duyurular</h2>'
            for d in duyurular[:10]:
                tarih_d = tarih_formatla(d.get('SistemeEklenmeTarihi', ''))
                ozet = re.sub(r'<[^>]+>', '', d.get('Ozet', ''))
                ozet = html_lib.unescape(ozet).strip()
                if len(ozet) > 280:
                    ozet = ozet[:280] + "..."
                html += f"""<div class="announcement-item">
                    <div class="announcement-title">{d.get('BaslikAd', '')}</div>
                    <div class="announcement-date">📅 {tarih_d}</div>
                    <div class="announcement-body">{ozet}</div>
                </div>"""
            html += '</div>'
        
        # Akademik Takvim
        if isinstance(takvim, dict) and takvim.get("ozet"):
            html += '<div class="card"><h2>📆 Akademik Takvim</h2><table><thead><tr><th>Tarih</th><th>Aktivite</th><th>Durum</th></tr></thead><tbody>'
            for t in takvim["ozet"]:
                durum_badge = "<span class='badge badge-active'>Devam Ediyor</span>" if t.get("Aktif") else "<span class='badge badge-ok'>Tamamlandı</span>"
                html += f"<tr><td><strong>{t.get('Tarih', '')}</strong></td><td>{t.get('Aktivite', '')}</td><td>{durum_badge}</td></tr>"
            html += '</tbody></table></div>'
        
        html += f"""
    <footer>
        <p>OBS Asistan v1.0 ile üretilmiştir.</p>
        <p>Bu rapor bağımsız bir öğrenci projesi tarafından kişisel kullanım amacıyla oluşturulmuştur.</p>
    </footer>
</div>
</body>
</html>"""
        
        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"{Fore.GREEN}✅ HTML raporu oluşturuldu: {dosya_adi}{Style.RESET_ALL}")
        return dosya_adi
