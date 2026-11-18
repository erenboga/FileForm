"""
FileForm - Modern Toplu Dönüştürme Arayüzü (Batch Conversion Dialog)
"""
import os
import subprocess
from pathlib import Path
from typing import List, Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QCheckBox, QProgressBar, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

from core.config import load_settings, save_settings
from core.notification import send_toast
from converters.manager import ConversionManager
from ui.settings_dialog import SettingsDialog
from ui.modern_theme import DARK_THEME, LIGHT_THEME

class ConversionWorker(QThread):
    progress_signal = pyqtSignal(int, int, str, bool)
    finished_signal = pyqtSignal(list)

    def __init__(self, manager: ConversionManager, files: List[str], target_ext: str, merge_pdf: bool, options: dict):
        super().__init__()
        self.manager = manager
        self.files = files
        self.target_ext = target_ext
        self.merge_pdf = merge_pdf
        self.options = options
        self._is_cancelled = False

    def run(self):
        def _cb(curr, tot, fname, ok):
            self.progress_signal.emit(curr, tot, fname, ok)

        results = self.manager.convert_batch(
            self.files,
            self.target_ext,
            self.options,
            merge_images_to_pdf=self.merge_pdf,
            progress_callback=_cb
        )
        self.finished_signal.emit(results)


class BatchDialog(QDialog):
    def __init__(self, files: Optional[List[str]] = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FileForm - Yerel Toplu Dosya Dönüştürücü")
        self.resize(760, 520)
        self.setAcceptDrops(True)

        self.manager = ConversionManager()
        self.settings = load_settings()
        self.files: List[str] = list(files or [])
        self.worker: Optional[ConversionWorker] = None
        self.last_output_dir: Optional[str] = None

        self._apply_theme()
        self._init_ui()
        self._populate_files()

    def _apply_theme(self):
        theme_name = self.settings.get("theme", "dark")
        self.setStyleSheet(DARK_THEME if theme_name == "dark" else LIGHT_THEME)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Üst Başlık ve Bilgi Çubuğu
        header_row = QHBoxLayout()
        title_box = QVBoxLayout()
        self.lbl_title = QLabel("Toplu Dosya Dönüştürücü")
        self.lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #89b4fa;")
        self.lbl_sub = QLabel("Dosyaları sürükleyip bırakabilir veya listeden yönetebilirsiniz.")
        self.lbl_sub.setStyleSheet("color: #a6adc8; font-size: 12px;")
        title_box.addWidget(self.lbl_title)
        title_box.addWidget(self.lbl_sub)
        header_row.addLayout(title_box)
        header_row.addStretch()

        self.btn_settings = QPushButton("⚙ Ayarlar")
        self.btn_settings.clicked.connect(self._open_settings)
        header_row.addWidget(self.btn_settings)

        layout.addLayout(header_row)

        # Dosya Tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Dosya Adı", "Kaynak Format", "Boyut", "Durum"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        # Dönüştürme Kontrolleri Satırı
        control_row = QHBoxLayout()

        control_row.addWidget(QLabel("Hedef Format:"))
        self.combo_target = QComboBox()
        self.combo_target.currentIndexChanged.connect(self._on_target_changed)
        control_row.addWidget(self.combo_target)

        self.chk_merge_pdf = QCheckBox("Görselleri tek bir PDF olarak birleştir")
        self.chk_merge_pdf.setVisible(False)
        control_row.addWidget(self.chk_merge_pdf)

        control_row.addStretch()

        self.btn_clear = QPushButton("Listeyi Temizle")
        self.btn_clear.clicked.connect(self._clear_list)
        control_row.addWidget(self.btn_clear)

        layout.addLayout(control_row)

        # İlerleme Çubuğu ve Durum
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.lbl_progress_status = QLabel("")
        self.lbl_progress_status.setStyleSheet("color: #a6adc8; font-weight: 600;")
        layout.addWidget(self.lbl_progress_status)

        # Alt Eylem Butonları
        bottom_row = QHBoxLayout()
        self.btn_open_folder = QPushButton("📁 Dönüştürülenler Klasörünü Aç")
        self.btn_open_folder.setVisible(False)
        self.btn_open_folder.clicked.connect(self._open_output_folder)
        bottom_row.addWidget(self.btn_open_folder)

        bottom_row.addStretch()

        self.btn_convert = QPushButton("Tümünü Dönüştür")
        self.btn_convert.setObjectName("btnPrimary")
        self.btn_convert.clicked.connect(self._start_conversion)
        bottom_row.addWidget(self.btn_convert)

        layout.addLayout(bottom_row)

    def _populate_files(self):
        self.table.setRowCount(0)
        valid_files = []

        for f in self.files:
            p = Path(f)
            if p.exists() and p.is_file():
                valid_files.append(str(p))

        self.files = valid_files
        self.table.setRowCount(len(self.files))

        for row, f in enumerate(self.files):
            p = Path(f)
            size_kb = p.stat().st_size / 1024
            size_str = f"{size_kb / 1024:.1f} MB" if size_kb > 1024 else f"{size_kb:.0f} KB"

            self.table.setItem(row, 0, QTableWidgetItem(p.name))
            self.table.setItem(row, 1, QTableWidgetItem(p.suffix.upper().lstrip(".")))
            self.table.setItem(row, 2, QTableWidgetItem(size_str))

            status_item = QTableWidgetItem("Bekliyor")
            status_item.setForeground(Qt.GlobalColor.gray)
            self.table.setItem(row, 3, status_item)

        # Hedef formatları hesapla
        self._update_target_combobox()

    def _update_target_combobox(self):
        self.combo_target.clear()
        if not self.files:
            return

        targets = self.manager.get_common_targets(self.files)
        if not targets:
            # Genel varsayılanlar
            targets = ["PNG", "JPG", "WebP", "PDF", "MP3", "MP4"]

        for t in targets:
            self.combo_target.addItem(t.upper(), t.lower())

        self._on_target_changed()

    def _on_target_changed(self):
        target = self.combo_target.currentData() or ""
        # PDF hedefse ve tüm dosyalar resimse "Birleştir" kutusunu göster
        is_pdf = target.lower() == "pdf"
        all_images = all(Path(f).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"} for f in self.files)
        self.chk_merge_pdf.setVisible(is_pdf and all_images and len(self.files) > 1)

    def _start_conversion(self):
        if not self.files:
            QMessageBox.warning(self, "Uyarı", "Dönüştürülecek dosya bulunamadı.")
            return

        target_ext = self.combo_target.currentData()
        if not target_ext:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hedef format seçin.")
            return

        self.btn_convert.setEnabled(False)
        self.btn_settings.setEnabled(False)
        self.btn_clear.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.files))
        self.progress_bar.setValue(0)
        self.btn_open_folder.setVisible(False)

        merge_pdf = self.chk_merge_pdf.isChecked()
        self.settings = load_settings()

        self.worker = ConversionWorker(
            self.manager,
            self.files,
            target_ext,
            merge_pdf,
            self.settings
        )
        self.worker.progress_signal.connect(self._on_progress)
        self.worker.finished_signal.connect(self._on_finished)
        self.worker.start()

    def _on_progress(self, curr: int, total: int, fname: str, success: bool):
        self.progress_bar.setValue(curr)
        self.lbl_progress_status.setText(f"Dönüştürülüyor ({curr}/{total}): {Path(fname).name}")

        # Tablo satır durumunu güncelle
        for row in range(self.table.rowCount()):
            if row < len(self.files) and self.files[row] == fname:
                item = self.table.item(row, 3)
                if success:
                    item.setText("✓ Tamamlandı")
                    item.setForeground(Qt.GlobalColor.green)
                else:
                    item.setText("✗ Hata")
                    item.setForeground(Qt.GlobalColor.red)
                break

    def _on_finished(self, results: list):
        self.btn_convert.setEnabled(True)
        self.btn_settings.setEnabled(True)
        self.btn_clear.setEnabled(True)
        self.progress_bar.setValue(len(self.files))

        success_count = sum(1 for _, ok, _, _ in results if ok)
        total_count = len(results)

        self.lbl_progress_status.setText(f"Tamamlandı: {success_count}/{total_count} dosya dönüştürüldü.")

        # Çıktı klasörünü bul
        if results and results[0][1]:
            out_file = results[0][2]
            if out_file:
                self.last_output_dir = str(Path(out_file).parent)
                self.btn_open_folder.setVisible(True)

        # Windows Bildirimi
        if self.settings.get("notify_on_complete", True):
            send_toast(
                "FileForm - Dönüştürme Tamamlandı",
                f"{success_count} dosya başarıyla dönüştürüldü."
            )

    def _open_output_folder(self):
        if self.last_output_dir and Path(self.last_output_dir).exists():
            subprocess.run(["explorer", self.last_output_dir])

    def _open_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec():
            self.settings = load_settings()
            self._apply_theme()

    def _clear_list(self):
        self.files.clear()
        self.table.setRowCount(0)
        self.combo_target.clear()
        self.progress_bar.setVisible(False)
        self.lbl_progress_status.setText("")
        self.btn_open_folder.setVisible(False)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        new_files = [u.toLocalFile() for u in urls if os.path.isfile(u.toLocalFile())]
        if new_files:
            self.files.extend(new_files)
            self._populate_files()
