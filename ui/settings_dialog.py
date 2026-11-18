"""
FileForm - Ayarlar ve Sistem Entegrasyon Penceresi
"""
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QSlider, QComboBox, QGroupBox, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt

from core.config import load_settings, save_settings
from core.registry import (
    install_context_menu, uninstall_context_menu,
    is_context_menu_installed, create_sendto_shortcut, remove_sendto_shortcut
)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FileForm - Ayarlar ve Sistem Entegrasyonu")
        self.setFixedSize(540, 480)
        self.settings = load_settings()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        # 1. Grup: Windows Entegrasyonu
        grp_sys = QGroupBox("Windows Sağ Tık ve Sistem Entegrasyonu")
        sys_layout = QVBoxLayout(grp_sys)

        self.lbl_status = QLabel()
        self._update_reg_status_label()
        sys_layout.addWidget(self.lbl_status)

        btn_row = QHBoxLayout()
        self.btn_install = QPushButton("Sağ Tık Menüsüne Ekle")
        self.btn_install.clicked.connect(self._on_install_clicked)
        self.btn_uninstall = QPushButton("Menüden Kaldır")
        self.btn_uninstall.clicked.connect(self._on_uninstall_clicked)
        btn_row.addWidget(self.btn_install)
        btn_row.addWidget(self.btn_uninstall)
        sys_layout.addLayout(btn_row)

        self.chk_sendto = QCheckBox("Windows 11 'Gönder' (SendTo) Menü Kısayolu Ekle")
        self.chk_sendto.setChecked(True)
        self.chk_sendto.toggled.connect(self._on_sendto_toggled)
        sys_layout.addWidget(self.chk_sendto)

        layout.addWidget(grp_sys)

        # 2. Grup: Dosya ve Çıktı Ayarları
        grp_out = QGroupBox("Dönüştürme ve Çıktı Tercihleri")
        out_layout = QVBoxLayout(grp_out)

        self.chk_delete_orig = QCheckBox("Dönüştürme başarılı olursa orijinal dosyaları Geri Dönüşüm Kutusu'na taşı")
        self.chk_delete_orig.setChecked(self.settings.get("delete_originals", False))
        out_layout.addWidget(self.chk_delete_orig)

        self.chk_notify = QCheckBox("İşlem tamamlandığında Windows Toast bildirimi göster")
        self.chk_notify.setChecked(self.settings.get("notify_on_complete", True))
        out_layout.addWidget(self.chk_notify)

        # Görsel Kalitesi
        lbl_q = QLabel("Varsayılan Görsel Kalitesi (JPEG/WebP):")
        out_layout.addWidget(lbl_q)

        slider_row = QHBoxLayout()
        self.slider_quality = QSlider(Qt.Orientation.Horizontal)
        self.slider_quality.setRange(50, 100)
        curr_q = self.settings.get("image_quality", 92)
        self.slider_quality.setValue(curr_q)
        self.lbl_q_val = QLabel(f"%{curr_q}")
        self.slider_quality.valueChanged.connect(lambda v: self.lbl_q_val.setText(f"%{v}"))
        slider_row.addWidget(self.slider_quality)
        slider_row.addWidget(self.lbl_q_val)
        out_layout.addLayout(slider_row)

        layout.addWidget(grp_out)

        # 3. Grup: Görünüm ve Tema
        grp_theme = QGroupBox("Arayüz Teması")
        theme_layout = QHBoxLayout(grp_theme)
        theme_layout.addWidget(QLabel("Tema:"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Koyu (Dark)", "Açık (Light)"])
        curr_theme = self.settings.get("theme", "dark")
        self.combo_theme.setCurrentIndex(0 if curr_theme == "dark" else 1)
        theme_layout.addWidget(self.combo_theme)
        layout.addWidget(grp_theme)

        # Alt Butonlar
        btn_box = QHBoxLayout()
        btn_box.addStretch()
        self.btn_save = QPushButton("Kaydet ve Kapat")
        self.btn_save.setObjectName("btnPrimary")
        self.btn_save.clicked.connect(self._save_and_close)
        btn_box.addWidget(self.btn_save)
        layout.addLayout(btn_box)

    def _update_reg_status_label(self):
        if is_context_menu_installed():
            self.lbl_status.setText("Durum: <font color='#a6e3a1'><b>Sağ Tık Menüsü Kurulu ve Aktif</b></font>")
        else:
            self.lbl_status.setText("Durum: <font color='#f38ba8'><b>Sağ Tık Menüsü Kurulu Değil</b></font>")

    def _on_install_clicked(self):
        ok, msg = install_context_menu()
        if ok:
            QMessageBox.information(self, "Başarılı", msg)
        else:
            QMessageBox.critical(self, "Hata", msg)
        self._update_reg_status_label()

    def _on_uninstall_clicked(self):
        ok, msg = uninstall_context_menu()
        if ok:
            QMessageBox.information(self, "Başarılı", msg)
        else:
            QMessageBox.critical(self, "Hata", msg)
        self._update_reg_status_label()

    def _on_sendto_toggled(self, checked: bool):
        if checked:
            create_sendto_shortcut()
        else:
            remove_sendto_shortcut()

    def _save_and_close(self):
        self.settings["delete_originals"] = self.chk_delete_orig.isChecked()
        self.settings["notify_on_complete"] = self.chk_notify.isChecked()
        self.settings["image_quality"] = self.slider_quality.value()
        self.settings["theme"] = "dark" if self.combo_theme.currentIndex() == 0 else "light"
        save_settings(self.settings)
        self.accept()
