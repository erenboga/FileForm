"""
FileForm - IPC (Inter-Process Communication) ve Debounce Modülü
Windows Gezgini'nde toplu dosya seçildiğinde çoklu açılan prosesleri tek çatıda toplar.
"""
import socket
import json
import time
import threading
from typing import List, Dict, Any, Tuple, Optional

IPC_HOST = "127.0.0.1"
IPC_PORT = 49218
DEBOUNCE_SECONDS = 0.25  # 250 milisaniye bekleme penceresi

def send_to_primary_instance(payload: Dict[str, Any], timeout: float = 0.3) -> bool:
    """
    Çalışan bir ana sunucu varsa argümanları ona gönderir.
    Başarılı olursa True döner, sunucu yoksa False döner.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((IPC_HOST, IPC_PORT))
            msg = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")
            s.sendall(msg)
            # Cevap bekle
            resp = s.recv(1024)
            if resp:
                data = json.loads(resp.decode("utf-8").strip())
                if data.get("status") == "ok":
                    return True
    except Exception:
        pass
    return False

class IPCServer:
    """
    İlk başlayan proses için yerel IPC sunucusu.
    Gelen tüm dosya çağrılarını debounce süresince toplar.
    """
    def __init__(self, initial_payload: Dict[str, Any]):
        self.initial_payload = initial_payload
        self.collected_files: List[str] = list(initial_payload.get("files", []))
        self.preset: Optional[str] = initial_payload.get("preset")
        self.is_gui: bool = initial_payload.get("gui", False)
        self.last_arrival = time.time()
        self.running = True
        self.server_socket: Optional[socket.socket] = None
        self.lock = threading.Lock()

    def run(self) -> Tuple[List[str], Optional[str], bool]:
        """
        Sunucuyu başlatır, gelen dosyaları toplar ve debounce süresi dolunca sonuçları döner.
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((IPC_HOST, IPC_PORT))
            self.server_socket.listen(50)
            self.server_socket.settimeout(0.05)  # 50ms polling
        except Exception as e:
            # Port meşgulse sadece ilk gelen dosyaları döner
            return self.collected_files, self.preset, self.is_gui

        # Dinleme döngüsü
        while self.running:
            try:
                conn, _ = self.server_socket.accept()
                threading.Thread(target=self._handle_client, args=(conn,), daemon=True).start()
            except socket.timeout:
                pass
            except Exception:
                break

            with self.lock:
                elapsed = time.time() - self.last_arrival
                # Debounce süresi dolduysa ve artık yeni çağrı gelmiyorsa döngüyü bitir
                if elapsed >= DEBOUNCE_SECONDS:
                    self.running = False

        try:
            self.server_socket.close()
        except Exception:
            pass

        # Tekrarlayan dosyaları ayıkla ama sırayı koru
        seen = set()
        unique_files = []
        for f in self.collected_files:
            if f not in seen:
                seen.add(f)
                unique_files.append(f)

        return unique_files, self.preset, self.is_gui

    def _handle_client(self, conn: socket.socket):
        try:
            conn.settimeout(1.0)
            data = b""
            while not data.endswith(b"\n"):
                chunk = conn.recv(1024)
                if not chunk:
                    break
                data += chunk
            if data:
                payload = json.loads(data.decode("utf-8").strip())
                new_files = payload.get("files", [])
                new_preset = payload.get("preset")
                new_gui = payload.get("gui", False)

                with self.lock:
                    self.collected_files.extend(new_files)
                    if new_preset and not self.preset:
                        self.preset = new_preset
                    if new_gui:
                        self.is_gui = True
                    self.last_arrival = time.time()

                conn.sendall(json.dumps({"status": "ok"}).encode("utf-8") + b"\n")
        except Exception:
            pass
        finally:
            try:
                conn.close()
            except Exception:
                pass
