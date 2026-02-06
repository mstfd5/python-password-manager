# CLASS TANIMI (OOP - Taslak)
class HedefSistem:
    
    # __init__ METODU (Dunder - Başlangıç Ayarları)
    # Bu sınıf çağrıldığında İLK burası çalışır.
    def __init__(self, ip_adresi, port):
        self.ip = ip_adresi  # Syntax: Değişken atama
        self.port = port
        self.durum = "Bilinmiyor"
        
    # METOD (Fonksiyon - Yetenek)
    def tarama_yap(self):
        # Syntax: if bloğu ve girinti
        if self.port == 80:
            self.durum = "Açık (Web)"
        else:
            self.durum = "Kapalı"
    
    # __str__ METODU (Dunder - Kimlik Kartı)
    # print(hedef1) dediğimizde burası çalışır.
    def __str__(self):
        return f"Hedef: {self.ip} | Port: {self.port} | Durum: {self.durum}"

# --- KULLANIM (Nesne Oluşturma) ---

# Syntax: Class'tan bir Object türetmek
hedef1 = HedefSistem("192.168.1.1", 80) 
# (Yukarıdaki satır çalıştığı an __init__ devreye girdi ve IP'yi kaydetti)

hedef1.tarama_yap() # Nesnenin yeteneğini kullandık

print(hedef1) 
# (Yukarıdaki satır çalıştığı an __str__ devreye girdi ve düzgün çıktı verdi)