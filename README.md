<p align="center">
  <img src="assets/logo.png" alt="FileForm Logo" width="500">
</p>

# FileForm - Windows Yerel Toplu Dosya Dönüştürücü

FileForm, herhangi bir internet bağlantısına veya üçüncü taraf bulut hizmetine ihtiyaç duymadan, doğrudan Windows sağ tık bağlam menüsü üzerinden çalışan yüksek hızlı ve yerel bir toplu dosya dönüştürücüdür.

---

## 🚀 Öne Çıkan Özellikler

- **Windows Sağ Tık ve SendTo Entegrasyonu:** Dosyaları seçip sağ tıklayarak saniyeler içinde dönüştürün.
- **Toplu İşlem ve Akıllı IPC Debounce:** Windows Gezgini'nde aynı anda 50 dosya seçildiğinde 50 ayrı pencere açılmaz; hafif soket toplayıcı tüm dosyaları tek bir işlemde birleştirir.
- **Güvenli Dosya Yönetimi:** Orijinal dosyalarınız korunur; dönüştürülen dosyalar kaynak klasörün içindeki `Dönüştürülenler` alt klasörüne düzenli biçimde aktarılır.
- **Çoklu Görseli Tek PDF Yapma:** Seçilen birden fazla resmi tek bir birleşik PDF belgesine dönüştürebilme imkanı.
- **Sıfır Bulut Bağımlılığı:** Tüm dönüşüm işlemleri tamamen yerel işlemci ve belleğinizde gerçekleşir.
- **Modern Fluent Arayüz:** PyQt6 ile tasarlanmış, koyu ve açık tema destekli modern masaüstü görünümü.

---

## 📁 Desteklenen Formatlar

| Kategori | Kaynak Formatlar | Hedef Formatlar |
| :--- | :--- | :--- |
| **Görsel** | PNG, JPG, JPEG, WEBP, BMP, ICO, TIFF, GIF | PNG, JPG, WEBP, PDF, ICO, BMP, TIFF |
| **PDF** | PDF (Tek veya Çok Sayfalı) | PNG, JPG, WEBP, TXT |
| **Ofis Belgeleri** | DOCX, DOC, XLSX, XLS, PPTX, PPT | PDF, TXT, CSV |
| **Multimedya** | MP4, MKV, AVI, MOV, WEBM, FLV | MP4, WEBM, GIF, MP3, WAV |
| **Veri / Tablo** | CSV, XLSX, JSON | CSV, XLSX, JSON |

---

## 🛠️ Kurulum ve Kullanım

### 1. Hızlı Kurulum (Sağ Tık Menüsüne Ekleme)
Klasör içindeki `kur_menu.bat` dosyasına çift tıklayarak yönetici izni gerekmeden menüyü kurabilirsiniz.

### 2. Kaldırma (Temizleme)
Menüyü kaldırmak için `kaldir_menu.bat` dosyasına çift tıklamanız yeterlidir.

### 3. Kaynak Koddan Çalıştırma
Gerekli Python paketlerini yüklemek için:
```bash
pip install -r requirements.txt
python main.py
```

### 4. Bağımsız (.exe) Derleme
Python kurulu olmayan bilgisayarlarda çalıştırmak üzere tek dosya paket oluşturmak için:
```bash
python build.py
```

---

## 🏗️ Mimari Yapı

- `core/ipc.py`: Windows Gezgini çoklu çalıştırmalarını tekilleştiren soket tabanlı toplayıcı.
- `core/registry.py`: `HKEY_CURRENT_USER` tabanlı basamaklı menü yöneticisi.
- `converters/`: Pillow, pypdfium2, win32com ve FFmpeg motorlarını barındıran modüller.
- `ui/`: PyQt6 tabanlı sürükle-bırak destekli modern kullanıcı arayüzü.
