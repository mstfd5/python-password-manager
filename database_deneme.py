import sqlite3

# 1. BAĞLANTI: 'sirket.db' adında bir dosya oluşturur ve bağlanır.
# (Eğer dosya varsa sadece bağlanır)
baglanti = sqlite3.connect('sirket.db')

# 2. İMLEÇ (Cursor): Veritabanı üzerinde işlem yapacak "elimiz".
imlec = baglanti.cursor()

# 3. TABLO OLUŞTURMA: SQL komutu ile tablo yaratıyoruz.
# IF NOT EXISTS: Hata almamak için "yoksa oluştur" diyoruz.
imlec.execute('''
    CREATE TABLE IF NOT EXISTS personel (
        id INTEGER PRIMARY KEY,
        isim TEXT,
        departman TEXT,
        maas INTEGER
    )
''')

# 4. VERİ EKLEME (INSERT): İçeriye biraz veri gömelim.
# Daha önce eklediysek tekrar eklemesin diye try-except falan koymadım, 
# her çalıştırdığında ekler, şimdilik sorun değil.
imlec.execute("INSERT INTO personel (isim, departman, maas) VALUES ('Ahmet', 'IT', 25000)")
imlec.execute("INSERT INTO personel (isim, departman, maas) VALUES ('Zeynep', 'İK', 18000)")
imlec.execute("INSERT INTO personel (isim, departman, maas) VALUES ('Mehmet', 'Siber Güvenlik', 35000)")

# Değişiklikleri kaydet (Commit etmezsen veriler uçucu olur)
baglanti.commit()

print("--- Veriler Eklendi ---\n")

# 5. VERİ ÇEKME (SELECT): İşte o meşhur sorgu anı.
# IT departmanında çalışanları seçelim.
imlec.execute("SELECT * FROM personel WHERE departman = 'IT' OR departman = 'Siber Güvenlik'")

# Gelen verileri al
gelen_veriler = imlec.fetchall()

print("--- Sorgu Sonucu ---")
for satir in gelen_veriler:
    print(f"ID: {satir[0]} | İsim: {satir[1]} | Bölüm: {satir[2]} | Maaş: {satir[3]}")

# 6. KAPANIŞ: Bağlantıyı kapat.
baglanti.close()