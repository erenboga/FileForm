"""
FileForm - Windows Kayıt Defteri (Registry) ve SendTo Menü Yöneticisi
Yönetici izni gerektirmeden HKCU düzeyinde sağ tık menüsü kurar ve kaldırır.
"""
import os
import sys
import winreg
import subprocess
from pathlib import Path
from typing import Tuple, List

REG_BASE = r"Software\Classes\*\shell\FileForm"
REG_DIR_BASE = r"Software\Classes\Directory\shell\FileForm"

PRESET_MENU_ITEMS = [
    ("01_gui", "FileForm ile Dönüştür...", "--gui"),
    ("02_png", "PNG'ye Dönüştür", "--preset png"),
    ("03_jpg", "JPG'ye Dönüştür", "--preset jpg"),
    ("04_webp", "WebP'ye Dönüştür", "--preset webp"),
    ("05_pdf", "PDF'e Dönüştür", "--preset pdf"),
    ("06_mp3", "MP3'e Dönüştür (Ses Ayıkla)", "--preset mp3"),
    ("07_mp4", "MP4'e Dönüştür (Video)", "--preset mp4"),
]

def get_icon_path() -> str:
    """Uygulama veya menü için .ico simge yolunu döner."""
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).parent
        ico = exe_dir / "assets" / "icon.ico"
        if ico.exists():
            return str(ico.resolve())
        return sys.executable
    else:
        project_dir = Path(__file__).parent.parent
        ico = project_dir / "assets" / "icon.ico"
        if ico.exists():
            return str(ico.resolve())
        return sys.executable

def get_launch_command(extra_args: str = "") -> str:
    """
    Çalışma ortamına göre doğru yürütme komutunu üretir.
    Eğer .exe ise doğrudan exe'yi, python ise pythonw.exe main.py'yi çağırır.
    """
    if getattr(sys, "frozen", False):
        # PyInstaller ile derlenmiş bağımsız .exe
        exe_path = sys.executable
        return f'"{exe_path}" {extra_args} "%1"'.strip()
    else:
        # Python kaynak kodu
        python_exe = sys.executable
        # Konsol penceresi açılmaması için pythonw tercih et
        pythonw_candidate = Path(python_exe).parent / "pythonw.exe"
        if pythonw_candidate.exists():
            runner = str(pythonw_candidate)
        else:
            runner = python_exe

        main_script = Path(__file__).parent.parent / "main.py"
        return f'"{runner}" "{main_script.resolve()}" {extra_args} "%1"'.strip()

def get_sendto_path() -> Path:
    """Windows SendTo (Gönder) klasörünü bulur."""
    appdata = os.environ.get("APPDATA")
    if appdata:
        sendto_dir = Path(appdata) / "Microsoft" / "Windows" / "SendTo"
        if sendto_dir.exists():
            return sendto_dir
    return Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "SendTo"

def create_sendto_shortcut() -> bool:
    """SendTo menüsüne FileForm kısayolu ekler."""
    try:
        sendto_dir = get_sendto_path()
        sendto_dir.mkdir(parents=True, exist_ok=True)
        shortcut_path = sendto_dir / "FileForm - Hızlı Dönüştür.lnk"

        if getattr(sys, "frozen", False):
            target_path = sys.executable
            args = "--gui"
        else:
            python_exe = sys.executable
            pythonw = Path(python_exe).parent / "pythonw.exe"
            target_path = str(pythonw if pythonw.exists() else python_exe)
            main_script = (Path(__file__).parent.parent / "main.py").resolve()
            args = f'"{main_script}" --gui'

        icon_path = get_icon_path()
        # PowerShell ile temiz .lnk kısayolu üret
        ps_cmd = f"""
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut('{str(shortcut_path)}')
        $Shortcut.TargetPath = '{target_path}'
        $Shortcut.Arguments = '{args}'
        $Shortcut.IconLocation = '{icon_path}'
        $Shortcut.Description = 'FileForm ile Toplu Dönüştür'
        $Shortcut.Save()
        """
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            timeout=5
        )
        return True
    except Exception as e:
        print(f"SendTo kısayol hatası: {e}")
        return False

def remove_sendto_shortcut() -> bool:
    """SendTo menüsünden FileForm kısayolunu siler."""
    try:
        sendto_dir = get_sendto_path()
        shortcut_path = sendto_dir / "FileForm - Hızlı Dönüştür.lnk"
        if shortcut_path.exists():
            shortcut_path.unlink()
        return True
    except Exception:
        return False

def install_context_menu() -> Tuple[bool, str]:
    """
    Windows sağ tık menüsüne FileForm basamaklı (cascaded) alt menüsünü kurar.
    Yönetici yetkisi gerektirmez.
    """
    try:
        icon_path = get_icon_path()

        # 1. Ana Menü Anahtarı: HKCU\Software\Classes\*\shell\FileForm
        root_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_BASE)
        winreg.SetValueEx(root_key, "MUIVerb", 0, winreg.REG_SZ, "FileForm ile Dönüştür")
        winreg.SetValueEx(root_key, "SubCommands", 0, winreg.REG_SZ, "")
        winreg.SetValueEx(root_key, "Icon", 0, winreg.REG_SZ, f'"{icon_path}"')
        winreg.CloseKey(root_key)

        # 2. Alt Menüler: HKCU\Software\Classes\*\shell\FileForm\shell
        sub_shell_path = f"{REG_BASE}\\shell"
        for key_name, label, extra_args in PRESET_MENU_ITEMS:
            item_path = f"{sub_shell_path}\\{key_name}"
            item_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, item_path)
            winreg.SetValueEx(item_key, "MUIVerb", 0, winreg.REG_SZ, label)
            winreg.SetValueEx(item_key, "Icon", 0, winreg.REG_SZ, f'"{icon_path}"')
            winreg.CloseKey(item_key)

            # command anahtarı
            cmd_path = f"{item_path}\\command"
            cmd_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_path)
            cmd_string = get_launch_command(extra_args)
            winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, cmd_string)
            winreg.CloseKey(cmd_key)

        # 3. Klasör Sağ Tık Menüsü: HKCU\Software\Classes\Directory\shell\FileForm
        dir_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_DIR_BASE)
        winreg.SetValueEx(dir_key, "MUIVerb", 0, winreg.REG_SZ, "Klasördeki Dosyaları Dönüştür (FileForm)...")
        winreg.SetValueEx(dir_key, "Icon", 0, winreg.REG_SZ, f'"{icon_path}"')
        winreg.CloseKey(dir_key)

        dir_cmd_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{REG_DIR_BASE}\\command")
        dir_cmd_str = get_launch_command("--gui --dir")
        winreg.SetValueEx(dir_cmd_key, "", 0, winreg.REG_SZ, dir_cmd_str)
        winreg.CloseKey(dir_cmd_key)

        # 4. SendTo Kısayolu Ekle
        create_sendto_shortcut()

        return True, "FileForm sağ tık menüsü ve SendTo entegrasyonu başarıyla kuruldu!"
    except Exception as e:
        return False, f"Sağ tık menüsü kurulurken hata oluştu: {e}"

def _delete_reg_tree(root, subkey: str) -> None:
    """Kayıt defteri ağacını yinelemeli (recursive) olarak siler."""
    try:
        key = winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        return

    while True:
        try:
            sub = winreg.EnumKey(key, 0)
            _delete_reg_tree(root, f"{subkey}\\{sub}")
        except OSError:
            break

    winreg.CloseKey(key)
    try:
        winreg.DeleteKey(root, subkey)
    except OSError:
        pass

def uninstall_context_menu() -> Tuple[bool, str]:
    """
    FileForm sağ tık menüsünü ve SendTo kısayolunu tamamen kaldırır.
    """
    try:
        _delete_reg_tree(winreg.HKEY_CURRENT_USER, REG_BASE)
        _delete_reg_tree(winreg.HKEY_CURRENT_USER, REG_DIR_BASE)
        remove_sendto_shortcut()
        return True, "FileForm sağ tık menüsü ve kısayolları sistemden temizlendi."
    except Exception as e:
        return False, f"Menü kaldırılırken hata oluştu: {e}"

def is_context_menu_installed() -> bool:
    """Sağ tık menüsünün kurulu olup olmadığını kontrol eder."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_BASE, 0, winreg.KEY_READ)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
