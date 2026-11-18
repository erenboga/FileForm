"""
FileForm - Ana Giriş Noktası (CLI, IPC ve GUI Yönlendirici)
"""
import os
import sys
import argparse
from pathlib import Path
from typing import List

from core.config import load_settings
from core.notification import send_toast
from core.ipc import send_to_primary_instance, IPCServer
from core.registry import install_context_menu, uninstall_context_menu
from converters.manager import ConversionManager

def parse_args():
    parser = argparse.ArgumentParser(description="FileForm - Yerel Toplu Dosya Dönüştürücü")
    parser.add_argument("files", nargs="*", help="Dönüştürülecek dosya veya klasörler")
    parser.add_argument("--gui", action="store_true", help="Toplu dönüştürme grafik arayüzünü aç")
    parser.add_argument("--preset", type=str, help="Hızlı dönüştürme hedef formatı (örn: png, jpg, pdf, mp3)")
    parser.add_argument("--dir", action="store_true", help="Girdi olarak klasör verildiğini belirtir")
    parser.add_argument("--install-menu", action="store_true", help="Windows sağ tık menüsünü kur")
    parser.add_argument("--uninstall-menu", action="store_true", help="Windows sağ tık menüsünü kaldır")
    parser.add_argument("--settings", action="store_true", help="Ayarlar penceresini aç")
    return parser.parse_args()

def run_preset_batch(files: List[str], target_preset: str):
    """Preset modunda dosyaları arka planda dönüştürür ve bildirim verir."""
    settings = load_settings()
    manager = ConversionManager()
    target_ext = target_preset.lower().lstrip(".")

    results = manager.convert_batch(files, target_ext, settings)
    success_count = sum(1 for _, ok, _, _ in results if ok)
    total_count = len(results)

    if settings.get("notify_on_complete", True):
        fmt_upper = target_ext.upper()
        if success_count == total_count:
            send_toast(
                "FileForm - Dönüştürme Başarılı",
                f"{success_count} dosya başarıyla {fmt_upper} formatına dönüştürüldü."
            )
        else:
            send_toast(
                "FileForm - Dönüştürme Tamamlandı",
                f"{success_count}/{total_count} dosya {fmt_upper} yapıldı ({total_count - success_count} hata)."
            )

def run_gui(files: List[str], open_settings: bool = False):
    """PyQt6 Grafik Arayüzünü Başlatır."""
    from PyQt6.QtWidgets import QApplication
    from ui.batch_dialog import BatchDialog
    from ui.settings_dialog import SettingsDialog

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    if open_settings:
        dlg = SettingsDialog()
        dlg.exec()
    else:
        dlg = BatchDialog(files)
        dlg.show()
        app.exec()

def expand_directory_files(paths: List[str]) -> List[str]:
    """Eğer klasör yolu verilmişse içindeki dosyaları listeler."""
    expanded = []
    for p_str in paths:
        p = Path(p_str)
        if p.is_dir():
            for child in p.iterdir():
                if child.is_file():
                    expanded.append(str(child.resolve()))
        elif p.is_file():
            expanded.append(str(p.resolve()))
    return expanded

def main():
    args = parse_args()

    # 1. Menü Kurulum / Kaldırma Komutları
    if args.install_menu:
        ok, msg = install_context_menu()
        print(msg)
        sys.exit(0 if ok else 1)

    if args.uninstall_menu:
        ok, msg = uninstall_context_menu()
        print(msg)
        sys.exit(0 if ok else 1)

    # 2. Doğrudan Ayarlar Penceresi
    if args.settings:
        run_gui([], open_settings=True)
        return

    # Dosya yollarını hazırla
    raw_files = args.files or []
    if args.dir:
        raw_files = expand_directory_files(raw_files)
    else:
        raw_files = [str(Path(f).resolve()) for f in raw_files if Path(f).exists()]

    # Eğer hiçbir argüman verilmemişse doğrudan boş GUI aç
    if not raw_files and not args.preset:
        run_gui([])
        return

    # 3. IPC Coordinator İstemci Kontrolü
    # Eğer arka planda başka bir instance varsa (Windows Gezgini çoklu çağrısı),
    # bu instance dosyasını ona aktarıp anında kapanmalıdır.
    payload = {
        "files": raw_files,
        "preset": args.preset,
        "gui": args.gui
    }

    if send_to_primary_instance(payload):
        # Başarıyla ana sunucuya iletildi, bu proses sonlanabilir
        sys.exit(0)

    # 4. Bu proses Ana Sunucu (Primary) oluyor!
    # Debounce süresince (250ms) diğer gelebilecek çağrıları toplar.
    server = IPCServer(payload)
    collected_files, final_preset, is_gui = server.run()

    if not collected_files:
        run_gui([])
        return

    # 5. Çalıştırma Kararı
    # Eğer preset belirtilmişse ve GUI istenmemişse arka planda dönüştür
    if final_preset and not is_gui:
        run_preset_batch(collected_files, final_preset)
    else:
        run_gui(collected_files)

if __name__ == "__main__":
    main()
