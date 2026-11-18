"""
FileForm - Yapılandırma ve Yol Yönetim Modülü
"""
import os
import json
from pathlib import Path

APP_NAME = "FileForm"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Windows Sağ Tık Menüsü Entegrasyonlu Yerel Toplu Dosya Dönüştürücü"

DEFAULT_SETTINGS = {
    "output_mode": "subfolder",       # 'subfolder', 'same_folder', 'custom'
    "subfolder_name": "Dönüştürülenler",
    "custom_output_dir": "",
    "delete_originals": False,        # Orijinal dosyaları çöp kutusuna taşı
    "theme": "dark",                  # 'dark', 'light', 'system'
    "notify_on_complete": True,       # Windows Toast bildirimi
    "image_quality": 92,              # JPEG/WebP kalitesi (1-100)
    "pdf_dpi": 200,                   # PDF render çözünürlüğü (DPI)
    "video_crf": 23,                  # Video kalite katsayısı (18-28)
    "audio_bitrate": "192k"           # Ses bitrate'i
}

def get_app_data_dir() -> Path:
    """Uygulama ayarlarının tutulduğu AppData klasörünü döner."""
    base_dir = os.environ.get("APPDATA") or str(Path.home())
    app_dir = Path(base_dir) / APP_NAME
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir

def get_settings_file_path() -> Path:
    return get_app_data_dir() / "settings.json"

def load_settings() -> dict:
    """Kayıtlı ayarları yükler, yoksa varsayılanları kaydeder."""
    path = get_settings_file_path()
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                settings = DEFAULT_SETTINGS.copy()
                settings.update(data)
                return settings
        except Exception:
            pass
    save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS.copy()

def save_settings(settings: dict) -> None:
    """Ayarları JSON dosyasına kaydeder."""
    path = get_settings_file_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ayar kaydetme hatası: {e}")

def resolve_output_path(source_file: str, target_ext: str, settings: dict = None) -> str:
    """
    Kaynak dosya ve hedef uzantıya göre çıktı dosya yolunu belirler.
    Çakışma varsa _1, _2 şeklinde artırır.
    """
    if settings is None:
        settings = load_settings()

    src_path = Path(source_file)
    src_dir = src_path.parent
    base_name = src_path.stem

    # Uzantıyı temizle (örn: '.png' veya 'png' -> '.png')
    if not target_ext.startswith("."):
        target_ext = f".{target_ext.lower()}"
    else:
        target_ext = target_ext.lower()

    # Hedef dizini belirle
    output_mode = settings.get("output_mode", "subfolder")
    if output_mode == "subfolder":
        subfolder_name = settings.get("subfolder_name", "Dönüştürülenler")
        out_dir = src_dir / subfolder_name
    elif output_mode == "custom" and settings.get("custom_output_dir"):
        out_dir = Path(settings["custom_output_dir"])
    else:
        out_dir = src_dir

    out_dir.mkdir(parents=True, exist_ok=True)

    # İsim çakışması kontrolü
    candidate = out_dir / f"{base_name}{target_ext}"
    counter = 1
    while candidate.exists():
        candidate = out_dir / f"{base_name}_{counter}{target_ext}"
        counter += 1

    return str(candidate)
