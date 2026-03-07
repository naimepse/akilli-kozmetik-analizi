import sqlite3

# Veritabanına aktaracağımız genişletilmiş yeni veriler
kimyasallar = [
    # ⚠️ Riskli / Zararlı İçerikler
    ("parfum", -15, "Alerjen riski taşıyor. Hassas ciltler dikkat etmeli!"),
    ("fragrance", -15, "Yapay parfüm, alerji ve hassasiyet riski taşır."),
    ("paraben", -20, "Koruyucu maddedir. Bazı türlerinin hormon bozucu olabileceği tartışılmaktadır."),
    ("sulfate", -15, "Sert temizleyicidir, cildin doğal yağını sökerek kurutabilir."),
    ("sls", -15, "Sodyum Lauryl Sülfat. Cilt bariyerini zayıflatabilir ve tahriş edebilir."),
    ("sles", -10, "SLS'ye göre daha yumuşak olsa da hassas ciltleri kurutabilir."),
    ("alcohol denat", -15, "Cildi ciddi şekilde kurutabilir ve bariyerine zarar verebilir."),
    ("dimethicone", -5, "Silikon içerir. Akneye meyilli ciltlerde gözenek tıkayabilir (Komedojenik)."),
    ("mineral oil", -10, "Petrol türevidir. Gözenekleri tıkayıp sivilceye yol açabilir."),
    
    # 💚 Faydalı / İyileştirici İçerikler
    ("glycerin", 0, "Harika bir nem tutucudur. Cilt bariyerini korur."),
    ("niacinamide", 0, "B3 Vitaminidir. Lekeleri açar, sebum dengeler ve sivilce izlerine iyi gelir."),
    ("ceramide", 0, "Cilt bariyerini onaran mükemmel bir içerik."),
    ("hyaluronic acid", 0, "Kendi ağırlığının çok ötesinde su tutarak cildi derinlemesine nemlendirir."),
    ("panthenol", 0, "Pro-Vitamin B5. Cildi yatıştırır, onarır ve nemlendirir."),
    ("salicylic acid", 0, "BHA (Beta Hidroksi Asit). Gözenek içini temizler, siyah nokta ve akneyle savaşır."),
    ("glycolic acid", 0, "AHA'dır. Cilt yüzeyindeki ölü deriyi uzaklaştırır, cilde aydınlık verir."),
    ("peptide", 0, "Kolajen üretimini destekler, ince çizgi ve yaşlanma karşıtı bakım yapar."),
    ("centella asiatica", 0, "Cilt bariyerini onarır, kızarıklığı ve tahrişi anında yatıştırır (Cica)."),
    ("allantoin", 0, "Hücre yenilenmesini destekler ve tahriş olmuş cildi sakinleştirir.")
]

def veritabani_hazirla():
    print("Veritabanı güncelleniyor...")
    try:
        conn = sqlite3.connect("kozmetik.db")
        cur = conn.cursor()

        # Eski tabloyu temizleyip yepyeni bir başlangıç yapıyoruz ki yeni listemiz sorunsuz eklensin
        cur.execute("DROP TABLE IF EXISTS icerikler")
        
        print("Yeni tablo kuruluyor...")
        cur.execute("""
            CREATE TABLE icerikler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                madde_adi TEXT UNIQUE NOT NULL,
                puan_etkisi INTEGER NOT NULL,
                mesaj TEXT
            )
        """)

        print("Zenginleştirilmiş veriler ekleniyor...")
        for madde in kimyasallar:
            cur.execute("""
                INSERT INTO icerikler (madde_adi, puan_etkisi, mesaj)
                VALUES (?, ?, ?)
            """, madde)

        conn.commit()
        conn.close()
        print("\n✅ MÜKEMMEL! Veritabanı başarıyla güncellendi ve yeni kozmetik içerikleri eklendi.")

    except Exception as e:
        print("\n❌ Veritabanı hatası:", e)

# Fonksiyonu çalıştır
veritabani_hazirla()