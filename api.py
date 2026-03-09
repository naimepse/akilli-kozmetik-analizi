from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
import sqlite3

app = FastAPI(
    title="Akıllı Kozmetik Analiz API",
    version="5.0.0" # Çoklu Site Güncellemesi!
)

class LinkIstegi(BaseModel):
    url: str

@app.get("/")
def ana_sayfayi_goster():
    return FileResponse("index.html")

@app.post("/analiz-et")
def urun_analiz_et_api(istek: LinkIstegi):
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        
        try:
            conn = sqlite3.connect("kozmetik.db")
            cur = conn.cursor()
            cur.execute("SELECT madde_adi, puan_etkisi, mesaj FROM icerikler")
            db_icerikler = cur.fetchall() 
            conn.close() 
            
            page.goto(istek.url, timeout=60000)
            page.wait_for_timeout(4000)
            
            temiz_liste = [] # Başlangıçta boş bir liste oluşturuyoruz
            
            # 🚦 TRAFİK POLİSİ: Gelen link hangi siteye ait?
            if "watsons.com.tr" in istek.url:
                hedef_kutu = page.locator("e2-product-legal-info")
                if hedef_kutu.count() > 0:
                    icerik_metni = hedef_kutu.inner_text()
                    sadece_icerik = icerik_metni.split("İmalatçı Bilgisi")[0].replace("Ürün İçerik Bilgisi", "").strip()
                    temiz_liste = [madde.strip().capitalize() for madde in sadece_icerik.split(",") if madde.strip()]
            
            elif "gratis.com" in istek.url:
                # 🕵️‍♀️ GRATIS İÇİN DETEKTİFLİK KISMI (Burayı seninle bulacağız!)
                hedef_kutu = page.locator(".text-primary-900.text-base.font-normal")
                if hedef_kutu.count() > 0:
                    icerik_metni = hedef_kutu.inner_text()
                    temiz_liste = [madde.strip().capitalize() for madde in icerik_metni.split(",") if madde.strip()]
            
            else:
                browser.close()
                raise HTTPException(status_code=400, detail="Sistem şu an sadece Watsons ve Gratis linklerini desteklemektedir!")

            # Eğer kutu bulundu ama içi boşsa:
            if len(temiz_liste) == 0:
                browser.close()
                raise HTTPException(status_code=404, detail="Bu ürünün içerik listesi sitede bulunamadı veya format uygun değil.")
            
            # --- STANDART ANALİZ ALGORİTMASI ---
            urun_skoru = 100
            zararli_bulunanlar = []
            faydali_bulunanlar = []
            
            for madde in temiz_liste:
                madde_kucuk = madde.lower()
                
                for db_madde, puan_etkisi, mesaj in db_icerikler:
                    if db_madde in madde_kucuk:
                        if puan_etkisi < 0:
                            urun_skoru += puan_etkisi
                            zararli_bulunanlar.append({"madde": madde, "uyari": mesaj})
                        else:
                            faydali_bulunanlar.append({"madde": madde, "fayda": mesaj})
            
            if urun_skoru < 0: urun_skoru = 0
            
            browser.close()
            
            return {
                "durum": "Başarılı",
                "veri_kaynagi": "SQLite Veritabanı",
                "toplam_icerik_sayisi": len(temiz_liste),
                "cilt_uyumluluk_skoru": urun_skoru,
                "faydali_icerikler": faydali_bulunanlar,
                "riskli_icerikler": zararli_bulunanlar,
                "tam_liste": temiz_liste
            }
                
        except Exception as e:
            browser.close()
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Siteye bağlanırken bir sorun oluştu: {str(e)}")