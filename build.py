"""
FileForm - Bağımsız Taşınabilir (.exe) Derleme Betiği
PyInstaller kullanarak Python veya kütüphane gerektirmeyen tek bir FileForm.exe üretir.
"""
import sys
import subprocess
from pathlib import Path

def build_executable():
    print("=" * 60)
    print("      FileForm Standalone .exe Derleme İşlemi Başlatılıyor")
    print("=" * 60)

    project_dir = Path(__file__).parent.resolve()
    main_py = project_dir / "main.py"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",                       # Hızlı başlatma ve ffmpeg performansı için onedir veya onefile
        "--windowed",                     # Konsol penceresi açılmasın
        "--name", "FileForm",
        "--icon", str(project_dir / "assets" / "icon.ico"),
        "--add-data", f"{project_dir / 'assets'};assets",
        "--collect-all", "imageio_ffmpeg",
        "--collect-all", "pypdfium2",
        "--hidden-import", "win32com.client",
        "--hidden-import", "win10toast",
        "--hidden-import", "send2trash",
        str(main_py)
    ]

    print("Çalıştırılan komut:", " ".join(cmd))
    res = subprocess.run(cmd, cwd=str(project_dir))

    if res.returncode == 0:
        print("\n" + "=" * 60)
        print("✓ Derleme başarıyla tamamlandı!")
        print(f"Çıktı klasörü: {project_dir / 'dist' / 'FileForm'}")
        print("=" * 60)
    else:
        print("\n✗ Derleme sırasında hata oluştu!")

if __name__ == "__main__":
    build_executable()
