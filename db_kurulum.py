import sqlite3

# Veritabanına aktaracağımız veriler
kimyasallar = [
    ("parfum", -15, "Alerjen riski taşıyor. Hassas ciltler dikkat etmeli!"),
    ("dimethicone", -5, "Silikon içerir. Akneye meyilli ciltlerde gözenek tıkayabilir (Komedojenik)."),
    ("glycerin", 0, "Harika bir nem tutucudur. Cilt bariyerini korur."),
    ("niacinamide", 0, "B3 Vitaminidir. Lekeleri açar ve sivilce izlerine iyi gelir."),
    ("ceramide", 0, "Cilt bariyerini onaran mükemmel bir içerik.")
]

def veritabani_hazirla():
    print("Sanal Veritabanı (SQLite) oluşturuluyor...")
    try:
        # Bu sihirli satır, klasöründe otomatik olarak bir veritabanı dosyası oluşturur!
        conn = sqlite3.connect("kozmetik.db")
        cur = conn.cursor()

        print("Tablo kuruluyor...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS icerikler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                madde_adi TEXT UNIQUE NOT NULL,
                puan_etkisi INTEGER NOT NULL,
                mesaj TEXT
            )
        """)

        print("Veriler ekleniyor...")
        for madde in kimyasallar:
            # INSERT OR IGNORE, veriler zaten varsa hata vermesini engeller
            cur.execute("""
                INSERT OR IGNORE INTO icerikler (madde_adi, puan_etkisi, mesaj)
                VALUES (?, ?, ?)
            """, madde)

        conn.commit()
        conn.close()
        print("\n✅ MÜKEMMEL! SQLite veritabanı başarıyla oluşturuldu ve veriler eklendi.")

    except Exception as e:
        print("\n❌ Veritabanı hatası:", e)

# Fonksiyonu çalıştır
veritabani_hazirla()