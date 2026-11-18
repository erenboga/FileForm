"""
FileForm - IPC Debounce ve Çoklu Çağrı Testi
"""
import time
import threading
import unittest
from core.ipc import IPCServer, send_to_primary_instance

class TestIPC(unittest.TestCase):
    def test_concurrent_clients_debounced(self):
        initial = {"files": ["C:\\test\\file1.png"], "preset": "png", "gui": False}
        server = IPCServer(initial)

        results_holder = []
        def run_server():
            files, preset, is_gui = server.run()
            results_holder.append((files, preset, is_gui))

        server_thread = threading.Thread(target=run_server)
        server_thread.start()

        # Sunucunun soketi dinlemeye başlaması için kısa bekleme
        time.sleep(0.05)

        # 4 farklı istemcinin Gezgin gibi peş peşe dosya göndermesi
        for i in range(2, 6):
            payload = {"files": [f"C:\\test\\file{i}.png"], "preset": "png", "gui": False}
            ok = send_to_primary_instance(payload)
            self.assertTrue(ok, f"İstemci {i} sunucuya bağlanamadı")
            time.sleep(0.03)

        server_thread.join(timeout=3.0)
        self.assertEqual(len(results_holder), 1)

        files, preset, is_gui = results_holder[0]
        self.assertEqual(len(files), 5, f"Toplanan dosya sayısı 5 olmalı, alınan: {len(files)}")
        self.assertEqual(preset, "png")
        self.assertFalse(is_gui)

if __name__ == "__main__":
    unittest.main()
