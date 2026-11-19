<p align="center">
  <img src="assets/logo.png" alt="FileForm Logo" width="480">
</p>

# FileForm - Windows Local Batch File Converter

<p align="center">
  <a href="https://github.com/erenboga/FileForm/releases/latest">
    <img src="https://img.shields.io/github/v/release/erenboga/FileForm?style=for-the-badge&color=0078D4&label=Release" alt="Latest Release">
  </a>
  <a href="https://github.com/erenboga/FileForm/releases/download/v1.0.0/FileForm-v1.0.0-windows-x64.zip">
    <img src="https://img.shields.io/badge/Windows-x64%20Download%20(Portable)-2ea44f?style=for-the-badge&logo=windows" alt="Download Windows">
  </a>
  <img src="https://img.shields.io/badge/Vibe%20Coding-100%25%20AI%20Built-8A2BE2?style=for-the-badge&logo=openai&logoColor=white" alt="Vibe Coding / Built with AI">
  <img src="https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue?style=for-the-badge" alt="Platform Windows">
</p>

<p align="center">
  <b><a href="#türkçe">Türkçe</a></b> | <b><a href="#english">English</a></b>
</p>

---

> ### 🤖 100% Vibe Coding & Built with AI
> **TR:** Bu proje, baştan sona tek bir satır kod dahi elle yazılmadan; mimarisi, kodları, Windows kayıt defteri entegrasyonu, arayüzü, testleri ve derleme süreçleri tamamen yapay zeka ajanları ile **"Vibe Coding"** yaklaşımıyla hayata geçirilmiştir.
>
> **EN:** This project was architected, written, tested, and packaged 100% autonomously through AI agents following the **"Vibe Coding"** philosophy — zero lines of code written by hand.

---

<a name="türkçe"></a>
## 🇹🇷 Türkçe

**FileForm**, harici bir internet bağlantısına veya üçüncü taraf bulut hizmetine ihtiyaç duymadan, doğrudan **Windows sağ tık bağlam menüsü** ve **"Gönder" (SendTo)** menüsü üzerinden çalışan yüksek hızlı, yerel ve gizlilik odaklı bir toplu dosya dönüştürücüdür.

### ⚡ Hızlı İndir (Python Gerektirmez)

Başka bir bilgisayarda kullanmak veya hemen başlamak için kurulumsuz taşınabilir sürümü indirebilirsiniz:

👉 **[FileForm-v1.0.0-windows-x64.zip İndir](https://github.com/erenboga/FileForm/releases/download/v1.0.0/FileForm-v1.0.0-windows-x64.zip)**

1. İndirdiğiniz `.zip` dosyasını istediğiniz bir klasöre çıkartın.
2. Klasör içindeki **`kur_menu.bat`** dosyasına çift tıklayın (yönetici izni gerektirmez).
3. Artık herhangi bir dosyayı seçip sağ tıklayarak saniyeler içinde dönüştürebilirsiniz!

### 🚀 Öne Çıkan Özellikler

- **Windows Sağ Tık Menüsü Entegrasyonu:** Tek tıkla açılan basamaklı menü (*PNG Yap, JPG Yap, WebP Yap, PDF Yap, MP3 Ses Ayıkla, MP4 Yap*) ve detaylı kontrol için *"FileForm ile Dönüştür..."* seçeneği.
- **Toplu İşlem ve Akıllı IPC Debounce:** Windows Gezgini'nde aynı anda 50 dosya seçildiğinde 50 ayrı pencere açılmaz; hafif soket toplayıcı tüm çağrıları tek bir ana işlemde birleştirir.
- **Güvenli Dosya Yönetimi:** Orijinal dosyalarınız asla kaybolmaz veya üzerine yazılmaz; dönüştürülen dosyalar kaynak klasörün içindeki `Dönüştürülenler` alt klasörüne düzenli biçimde aktarılır.
- **Çoklu Görseli Tek PDF Yapma:** Seçilen birden fazla resmi tek bir birleşik PDF belgesine dönüştürebilme imkanı.
- **Sıfır Bulut Bağımlılığı:** Tüm dönüşüm işlemleri tamamen yerel işlemci ve belleğinizde gerçekleşir; dosyalarınız cihazınızdan dışarı çıkmaz.
- **Modern Fluent Arayüz:** PyQt6 ile tasarlanmış, koyu ve açık tema destekli modern masaüstü görünümü.

### 📁 Desteklenen Formatlar

| Kategori | Kaynak Formatlar | Hedef Formatlar |
| :--- | :--- | :--- |
| **Görsel** | PNG, JPG, JPEG, WEBP, BMP, ICO, TIFF, GIF | PNG, JPG, WEBP, PDF, ICO (çoklu boyut), BMP, TIFF |
| **PDF** | PDF (Tek veya Çok Sayfalı) | PNG, JPG, WEBP, TXT (Yüksek DPI Sayfa Render) |
| **Ofis Belgeleri** | DOCX, DOC, XLSX, XLS, PPTX, PPT | PDF, TXT, CSV (Orijinal MS Office COM Motoru) |
| **Multimedya** | MP4, MKV, AVI, MOV, WEBM, FLV | MP4, WEBM, GIF (Yüksek Kalite Palet), MP3, WAV |
| **Veri / Tablo** | CSV, XLSX, JSON | CSV, XLSX, JSON |

### 🛠️ Geliştiriciler İçin Kaynak Koddan Çalıştırma

```bash
# Depoyu klonlayın
git clone https://github.com/erenboga/FileForm.git
cd FileForm

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
python main.py

# Sağ tık menüsünü kurun / kaldırın
python main.py --install-menu
python main.py --uninstall-menu

# Bağımsız .exe paketini derleyin
python build.py
```

---

<a name="english"></a>
## 🇬🇧 English

**FileForm** is a blazing-fast, 100% offline and privacy-first local batch file converter for Windows that operates directly from your **Windows File Explorer right-click context menu** and the **"Send to"** menu.

### ⚡ Quick Download (No Python Required)

You can download the pre-compiled, portable release ready for any Windows machine:

👉 **[Download FileForm-v1.0.0-windows-x64.zip](https://github.com/erenboga/FileForm/releases/download/v1.0.0/FileForm-v1.0.0-windows-x64.zip)**

1. Extract the `.zip` archive to any directory.
2. Double-click **`kur_menu.bat`** (or `FileForm.exe --install-menu`) — *no Administrator privileges required!*
3. Select any file or batch of files in Windows Explorer, right-click, and convert instantly.

### 🚀 Key Features

- **Native Windows Context Menu & SendTo Integration:** Access quick conversion presets directly (*Convert to PNG, JPG, WebP, PDF, Extract MP3 Audio, MP4*) or open the full batch manager window.
- **Batch Processing with IPC Debounce:** Selecting 50 files in Explorer won't spawn 50 popup windows. A lightweight local socket coordinator automatically collects all selected paths within a 250ms debounce window into a single batch queue.
- **Safe & Organized Output:** Originals are left 100% intact. Converted files are automatically saved into a clean `Dönüştürülenler` (Converted) subfolder with smart incremental naming (`_1`, `_2`) if duplicates exist.
- **Merge Images to PDF:** Select multiple photos or scanned documents and combine them into a single multi-page PDF document with one click.
- **100% Offline & Private:** Zero cloud dependencies, zero telemetry. Every byte is converted locally on your CPU and RAM.
- **Modern Fluent UI:** Built with PyQt6 supporting sleek Dark & Light modes, real-time progress bars, and drag-and-drop file additions.

### 📁 Supported Formats

| Category | Input Formats | Output Formats |
| :--- | :--- | :--- |
| **Images** | PNG, JPG, JPEG, WEBP, BMP, ICO, TIFF, GIF | PNG, JPG, WEBP, PDF, ICO (multi-resolution 16-256px), BMP, TIFF |
| **PDF** | PDF (Single or Multi-Page) | High-DPI PNG, JPG, WEBP, TXT |
| **Office Documents** | DOCX, DOC, XLSX, XLS, PPTX, PPT | PDF, TXT, CSV (via native Microsoft Office COM engine) |
| **Multimedia** | MP4, MKV, AVI, MOV, WEBM, FLV | MP4, WEBM, High-Quality GIF, MP3, WAV (via embedded FFmpeg) |
| **Data & Tables** | CSV, XLSX, JSON | CSV, XLSX, JSON |

### 🛠️ Developer Setup (Run from Source)

```bash
# Clone the repository
git clone https://github.com/erenboga/FileForm.git
cd FileForm

# Install requirements
pip install -r requirements.txt

# Run GUI
python main.py

# Install or uninstall Windows Explorer context menu
python main.py --install-menu
python main.py --uninstall-menu

# Run automated test suite
python -m unittest discover tests

# Build standalone portable executable
python build.py
```

---

## 🏗️ Architecture

- `core/ipc.py`: Socket-based single-instance coordinator handling Windows Explorer batch multi-invokes.
- `core/registry.py`: Dynamic `HKEY_CURRENT_USER` context menu and SendTo shortcut manager.
- `converters/`: Modular conversion drivers powered by Pillow, pypdfium2, win32com, and FFmpeg.
- `ui/`: Modern PyQt6 interface featuring responsive multithreading and Fluent themes.

---

## 📄 License

MIT License — Feel free to use, modify, and distribute.
