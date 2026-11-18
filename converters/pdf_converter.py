"""
FileForm - PDF Dönüştürücü (pypdfium2 ve PyPDF2 Tabanlı)
"""
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image
import pypdfium2 as pdfium
from .base import BaseConverter

class PdfConverter(BaseConverter):
    TARGET_FORMATS = ["png", "jpg", "webp", "txt"]

    def can_convert(self, source_ext: str, target_ext: str) -> bool:
        src = source_ext.lower().lstrip(".")
        tgt = target_ext.lower().lstrip(".")
        return src == "pdf" and tgt in self.TARGET_FORMATS

    def get_supported_targets(self, source_ext: str) -> List[str]:
        if source_ext.lower().lstrip(".") == "pdf":
            return self.TARGET_FORMATS.copy()
        return []

    def convert(self, source_path: str, target_path: str, options: Optional[Dict[str, Any]] = None) -> bool:
        if options is None:
            options = {}

        dpi = int(options.get("pdf_dpi", 200))
        scale = dpi / 72.0  # Standart 72 DPI PDF ölçeği
        tgt_ext = os.path.splitext(target_path)[1].lower().lstrip(".")
        target_dir = Path(target_path).parent
        stem = Path(source_path).stem

        # PDF -> Metin
        if tgt_ext == "txt":
            pdf = pdfium.PdfDocument(source_path)
            full_text = []
            for i, page in enumerate(pdf):
                text_page = page.get_textpage()
                page_text = text_page.get_text_range()
                full_text.append(f"--- Sayfa {i+1} ---\n{page_text}\n")
            with open(target_path, "w", encoding="utf-8") as f:
                f.write("\n".join(full_text))
            return True

        # PDF -> Resimler (PNG, JPG, WebP)
        pdf = pdfium.PdfDocument(source_path)
        page_count = len(pdf)

        if page_count == 1:
            page = pdf[0]
            pil_image = page.render(scale=scale).to_pil()
            if tgt_ext in ("jpg", "jpeg") and pil_image.mode != "RGB":
                pil_image = pil_image.convert("RGB")
            pil_image.save(target_path)
        else:
            # Çok sayfalı PDF ise her sayfa için adlandır
            for idx in range(page_count):
                page = pdf[idx]
                pil_image = page.render(scale=scale).to_pil()
                if tgt_ext in ("jpg", "jpeg") and pil_image.mode != "RGB":
                    pil_image = pil_image.convert("RGB")
                page_file = target_dir / f"{stem}_sayfa_{idx+1}.{tgt_ext}"
                pil_image.save(str(page_file))

        return True

    @staticmethod
    def merge_images_to_pdf(image_paths: List[str], target_pdf_path: str) -> bool:
        """Birden fazla görseli tek bir çok sayfalı PDF dosyasında birleştirir."""
        if not image_paths:
            return False

        opened_images = []
        try:
            for path in image_paths:
                img = Image.open(path)
                if img.mode in ("RGBA", "LA", "P"):
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    alpha_img = img.convert("RGBA")
                    bg.paste(alpha_img, mask=alpha_img.split()[3])
                    opened_images.append(bg)
                elif img.mode != "RGB":
                    opened_images.append(img.convert("RGB"))
                else:
                    opened_images.append(img.copy())
                img.close()

            if opened_images:
                first = opened_images[0]
                rest = opened_images[1:]
                Path(target_pdf_path).parent.mkdir(parents=True, exist_ok=True)
                first.save(target_pdf_path, "PDF", resolution=100.0, save_all=True, append_images=rest)
                return True
        finally:
            for im in opened_images:
                try:
                    im.close()
                except Exception:
                    pass
        return False
