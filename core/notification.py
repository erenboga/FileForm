"""
FileForm - Windows Toast Bildirim Modülü
"""
import threading
import subprocess
import sys

def send_toast(title: str, message: str) -> None:
    """Windows bildirimini arka planda asenkron gönderir (UI'ı bloklamaz)."""
    def _worker():
        try:
            # PowerShell tabanlı modern Windows 10/11 toast bildirimi
            ps_script = f"""
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
            $template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02
            $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template)
            $textNodes = $xml.GetElementsByTagName("text")
            $textNodes.Item(0).AppendChild($xml.CreateTextNode('{title}')) > $null
            $textNodes.Item(1).AppendChild($xml.CreateTextNode('{message}')) > $null
            $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('FileForm').Show($toast)
            """
            subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                timeout=5
            )
        except Exception:
            # Fallback to win10toast if available
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=4, threaded=True)
            except Exception:
                pass

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
