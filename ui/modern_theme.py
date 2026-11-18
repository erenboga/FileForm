"""
FileForm - Modern Fluent Arayüz Temaları (Dark & Light QSS)
"""

DARK_THEME = """
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', 'Segoe UI Variable', sans-serif;
    font-size: 13px;
}

QMainWindow, QDialog {
    background-color: #1e1e2e;
}

QGroupBox {
    border: 1px solid #313244;
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 10px;
    font-weight: bold;
    color: #89b4fa;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    background-color: #1e1e2e;
}

QTableWidget {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 6px;
    gridline-color: #313244;
    selection-background-color: #45475a;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #11111b;
    color: #a6adc8;
    padding: 6px;
    border: 1px solid #313244;
    font-weight: 600;
}

QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #45475a;
    border-color: #585b70;
}

QPushButton:pressed {
    background-color: #585b70;
}

QPushButton#btnPrimary {
    background-color: #89b4fa;
    color: #11111b;
    border: none;
    font-size: 14px;
    font-weight: bold;
    padding: 8px 20px;
}

QPushButton#btnPrimary:hover {
    background-color: #b4befe;
}

QPushButton#btnPrimary:pressed {
    background-color: #74c7ec;
}

QComboBox {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 4px 10px;
    color: #cdd6f4;
    min-height: 24px;
}

QComboBox:hover {
    border-color: #89b4fa;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox QAbstractItemView {
    background-color: #1e1e2e;
    border: 1px solid #45475a;
    selection-background-color: #89b4fa;
    selection-color: #11111b;
}

QProgressBar {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 6px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    height: 18px;
}

QProgressBar::chunk {
    background-color: #a6e3a1;
    border-radius: 5px;
}

QCheckBox {
    spacing: 8px;
    color: #cdd6f4;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #45475a;
    border-radius: 4px;
    background-color: #313244;
}

QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}

QSlider::groove:horizontal {
    height: 6px;
    background: #313244;
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background: #89b4fa;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #cdd6f4;
    border: 1px solid #89b4fa;
    width: 16px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 8px;
}

QScrollBar:vertical {
    border: none;
    background: #181825;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #45475a;
    min-height: 20px;
    border-radius: 4px;
}
"""

LIGHT_THEME = """
QWidget {
    background-color: #f8f9fa;
    color: #212529;
    font-family: 'Segoe UI', 'Segoe UI Variable', sans-serif;
    font-size: 13px;
}

QMainWindow, QDialog {
    background-color: #f8f9fa;
}

QGroupBox {
    border: 1px solid #dee2e6;
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 10px;
    font-weight: bold;
    color: #0d6efd;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    background-color: #f8f9fa;
}

QTableWidget {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-radius: 6px;
    gridline-color: #e9ecef;
    selection-background-color: #e7f1ff;
    selection-color: #0d6efd;
}

QHeaderView::section {
    background-color: #f1f3f5;
    color: #495057;
    padding: 6px;
    border: 1px solid #dee2e6;
    font-weight: 600;
}

QPushButton {
    background-color: #ffffff;
    color: #212529;
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #e9ecef;
    border-color: #adb5bd;
}

QPushButton#btnPrimary {
    background-color: #0d6efd;
    color: #ffffff;
    border: none;
    font-size: 14px;
    font-weight: bold;
    padding: 8px 20px;
}

QPushButton#btnPrimary:hover {
    background-color: #0b5ed7;
}

QComboBox {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 4px 10px;
    color: #212529;
    min-height: 24px;
}

QProgressBar {
    background-color: #e9ecef;
    border: 1px solid #ced4da;
    border-radius: 6px;
    text-align: center;
    color: #212529;
    font-weight: bold;
    height: 18px;
}

QProgressBar::chunk {
    background-color: #198754;
    border-radius: 5px;
}
"""
