"""
FileForm - Veri ve Tablo Dosyaları Dönüştürücü (CSV, XLSX, JSON)
"""
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from .base import BaseConverter

class DataConverter(BaseConverter):
    DATA_EXTS = {".csv", ".xlsx", ".xls", ".json"}
    DATA_TARGETS = ["csv", "xlsx", "json"]

    def can_convert(self, source_ext: str, target_ext: str) -> bool:
        src = source_ext.lower()
        if not src.startswith("."):
            src = f".{src}"
        tgt = target_ext.lower().lstrip(".")
        return src in self.DATA_EXTS and tgt in self.DATA_TARGETS

    def get_supported_targets(self, source_ext: str) -> List[str]:
        src = source_ext.lower()
        if not src.startswith("."):
            src = f".{src}"
        curr = src.lstrip(".")
        if curr == "xls":
            curr = "xlsx"
        if src in self.DATA_EXTS:
            return [t for t in self.DATA_TARGETS if t != curr]
        return []

    def convert(self, source_path: str, target_path: str, options: Optional[Dict[str, Any]] = None) -> bool:
        src_ext = Path(source_path).suffix.lower()
        tgt_ext = Path(target_path).suffix.lower().lstrip(".")

        # 1. Kaynağı pandas ile DataFrame'e oku
        if src_ext == ".csv":
            df = pd.read_csv(source_path)
        elif src_ext in (".xlsx", ".xls"):
            df = pd.read_excel(source_path)
        elif src_ext == ".json":
            df = pd.read_json(source_path)
        else:
            return False

        # 2. Hedef formata kaydet
        if tgt_ext == "csv":
            df.to_csv(target_path, index=False, encoding="utf-8-sig")
            return True
        elif tgt_ext == "xlsx":
            df.to_excel(target_path, index=False, engine="openpyxl")
            return True
        elif tgt_ext == "json":
            df.to_json(target_path, orient="records", force_ascii=False, indent=2)
            return True

        return False
