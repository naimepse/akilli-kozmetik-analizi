from playwright.sync_api import sync_playwright

# --- MİNİ VERİTABANIMIZ (SİSTEMİN BEYNİ) ---
# Gerçek projede bu veriler PostgreSQL'den gelecek, şimdilik burada tutuyoruz.
KIMYASAL_SOZLUK = {
    "parfum": {"puan_etkisi": -15, "mesaj": "Alerjen riski taşıyor. Hassas ciltler dikkat etmeli!"},
    "dimethicone": {"puan_etkisi": -5, "mesaj": "Silikon içerir. Akneye meyilli ciltlerde gözenek tıkayabilir (Komedojenik)."},
    "glycerin": {"puan_etkisi": +5, "mesaj": "Harika bir nem tutucudur. Cilt bariyerini korur."},
    "niacinamide": {"puan_etkisi": +10, "mesaj": "B3 Vitaminidir. Lekeleri açar ve sivilce izlerine iyi gelir."},
    "ceramide": {"puan_etkisi": +10, "mesaj": "Cilt bariyerini onaran mükemmel bir içerik."}
}

def urun_analiz_et(url):
    print("🤖 Akıllı Asistan Başlatılıyor ve Siteye Gidiliyor...\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(4000)
        
        hedef_kutu = page.locator("e2-product-legal-info")
        
        if hedef_kutu.count() > 0:
            icerik_metni = hedef_kutu.inner_text()
            
            # 1. Veri Temizleme (Bir önceki adımda yaptığımız yer)
            try:
                sadece_icerik = icerik_metni.split("İmalatçı Bilgisi")[0].replace("Ürün İçerik Bilgisi", "").strip()
                temiz_liste = [madde.strip().capitalize() for madde in sadece_icerik.split(",") if madde.strip()]
                
                print(f"✅ {len(temiz_liste)} adet içerik başarıyla ayrıştırıldı. Analiz Başlıyor...\n")
                print("="*50)
                
                # 2. KARAR DESTEK ALGORİTMASI (Puanlama Sistemi)
                urun_skoru = 100
                zararli_bulunanlar = []
                faydali_bulunanlar = []
                
                for madde in temiz_liste:
                    madde_kucuk = madde.lower()
                    
                    # Veritabanımızdaki riskli/faydalı kelimeleri kontrol ediyoruz
                    for sozluk_kelimesi, ozellikler in KIMYASAL_SOZLUK.items():
                        if sozluk_kelimesi in madde_kucuk:
                            urun_skoru += ozellikler["puan_etkisi"]
                            
                            if ozellikler["puan_etkisi"] < 0:
                                zararli_bulunanlar.append(f"❌ {madde}: {ozellikler['mesaj']}")
                            else:
                                faydali_bulunanlar.append(f"🌟 {madde}: {ozellikler['mesaj']}")
                
                # Maksimum puanı 100'de sınırlayalım
                if urun_skoru > 100: urun_skoru = 100
                
                # 3. KULLANICIYA RAPOR SUNUMU
                print(f"🎯 ÜRÜN CİLT UYUMLULUK SKORU: {urun_skoru} / 100")
                print("="*50)
                
                if zararli_bulunanlar:
                    print("\n⚠️ DİKKAT EDİLMESİ GEREKENLER:")
                    for z in zararli_bulunanlar: print(z)
                
                if faydali_bulunanlar:
                    print("\n💚 ÖNE ÇIKAN FAYDALI İÇERİKLER:")
                    for f in faydali_bulunanlar: print(f)
                    
                print("\n" + "="*50)
                
            except Exception as e:
                print("[HATA] Analiz sırasında sorun çıktı:", e)
        else:
            print("[HATA] Ürün içeriği sitede bulunamadı.")
            
        browser.close()

# Aynı link üzerinden test ediyoruz
yeni_link = "https://www.watsons.com.tr/the-purest-solutions-gunluk-nemlendirici-bakim-kremi-50-ml/p/BP_1313396"
urun_analiz_et(yeni_link)