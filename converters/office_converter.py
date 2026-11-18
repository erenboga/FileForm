"""
FileForm - Ofis Belgeleri Dönüştürücü (Microsoft Office COM ve python-docx Tabanlı)
"""
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from .base import BaseConverter

class OfficeConverter(BaseConverter):
    WORD_EXTS = {".docx", ".doc"}
    EXCEL_EXTS = {".xlsx", ".xls"}
    PPT_EXTS = {".pptx", ".ppt"}
    ALL_OFFICE_EXTS = WORD_EXTS | EXCEL_EXTS | PPT_EXTS

    def can_convert(self, source_ext: str, target_ext: str) -> bool:
        src = source_ext.lower()
        if not src.startswith("."):
            src = f".{src}"
        tgt = target_ext.lower().lstrip(".")

        if src in self.WORD_EXTS:
            return tgt in ("pdf", "txt")
        if src in self.EXCEL_EXTS:
            return tgt in ("pdf", "csv")
        if src in self.PPT_EXTS:
            return tgt == "pdf"
        return False

    def get_supported_targets(self, source_ext: str) -> List[str]:
        src = source_ext.lower()
        if not src.startswith("."):
            src = f".{src}"
        if src in self.WORD_EXTS:
            return ["pdf", "txt"]
        if src in self.EXCEL_EXTS:
            return ["pdf", "csv"]
        if src in self.PPT_EXTS:
            return ["pdf"]
        return []

    def convert(self, source_path: str, target_path: str, options: Optional[Dict[str, Any]] = None) -> bool:
        src_ext = Path(source_path).suffix.lower()
        tgt_ext = Path(target_path).suffix.lower().lstrip(".")
        abs_src = str(Path(source_path).resolve())
        abs_tgt = str(Path(target_path).resolve())

        if src_ext in self.WORD_EXTS:
            return self._convert_word(abs_src, abs_tgt, tgt_ext)
        elif src_ext in self.EXCEL_EXTS:
            return self._convert_excel(abs_src, abs_tgt, tgt_ext)
        elif src_ext in self.PPT_EXTS:
            return self._convert_powerpoint(abs_src, abs_tgt, tgt_ext)
        return False

    def _convert_word(self, source_path: str, target_path: str, tgt_ext: str) -> bool:
        # Word COM otomasyonu ile orijinal düzeni koruyarak dönüştür
        try:
            import win32com.client
            import pythoncom
            pythoncom.CoInitialize()
            word = win32com.client.DispatchEx("Word.Application")
            word.Visible = False
            word.DisplayAlerts = False
            try:
                doc = word.Documents.Open(source_path, ReadOnly=True)
                if tgt_ext == "pdf":
                    # wdExportFormatPDF = 17
                    doc.ExportAsFixedFormat(target_path, 17)
                elif tgt_ext == "txt":
                    # wdFormatDOSText = 4, wdFormatUnicodeText = 7
                    doc.SaveAs(target_path, FileFormat=7)
                doc.Close(SaveChanges=False)
                return True
            finally:
                word.Quit()
                pythoncom.CoUninitialize()
        except Exception:
            # Fallback: python-docx ile metin çıkarma
            if tgt_ext == "txt" and source_path.endswith(".docx"):
                import docx
                doc = docx.Document(source_path)
                full_text = [p.text for p in doc.paragraphs]
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(full_text))
                return True
            raise

    def _convert_excel(self, source_path: str, target_path: str, tgt_ext: str) -> bool:
        if tgt_ext == "csv":
            import pandas as pd
            df = pd.read_excel(source_path)
            df.to_csv(target_path, index=False, encoding="utf-8-sig")
            return True

        # Excel -> PDF
        try:
            import win32com.client
            import pythoncom
            pythoncom.CoInitialize()
            excel = win32com.client.DispatchEx("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False
            try:
                wb = excel.Workbooks.Open(source_path, ReadOnly=True)
                # xlTypePDF = 0
                wb.ExportAsFixedFormat(0, target_path)
                wb.Close(SaveChanges=False)
                return True
            finally:
                excel.Quit()
                pythoncom.CoUninitialize()
        except Exception:
            raise

    def _convert_powerpoint(self, source_path: str, target_path: str, tgt_ext: str) -> bool:
        if tgt_ext != "pdf":
            return False
        try:
            import win32com.client
            import pythoncom
            pythoncom.CoInitialize()
            ppt = win32com.client.DispatchEx("PowerPoint.Application")
            try:
                # WithWindow = False (1)
                presentation = ppt.Presentations.Open(source_path, WithWindow=False)
                # ppSaveAsPDF = 32
                presentation.SaveAs(target_path, 32)
                presentation.Close()
                return True
            finally:
                ppt.Quit()
                pythoncom.CoUninitialize()
        except Exception:
            raise
