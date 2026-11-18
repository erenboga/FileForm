"""
FileForm - Görsel Dönüştürücü (Pillow Tabanlı)
"""
import os
from typing import List, Dict, Any, Optional
from PIL import Image
from .base import BaseConverter

class ImageConverter(BaseConverter):
    IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".ico", ".tiff", ".tif", ".gif", ".tga", ".ppm"}
    TARGET_FORMATS = ["png", "jpg", "jpeg", "webp", "pdf", "ico", "bmp", "tiff"]

    def can_convert(self, source_ext: str, target_ext: str) -> bool:
        src = source_ext.lower()
        if not src.startswith("."):
            src = f".{src}"
        tgt = target_ext.lower().lstrip(".")
        return src in self.IMAGE_EXTS and tgt in self.TARGET_FORMATS

    def get_supported_targets(self, source_ext: str) -> List[str]:
        src = source_ext.lower()
        if not src.startswith("."):
            src = f".{src}"
        if src in self.IMAGE_EXTS:
            curr = src.lstrip(".")
            if curr == "jpeg":
                curr = "jpg"
            return [fmt for fmt in self.TARGET_FORMATS if fmt != curr]
        return []

    def convert(self, source_path: str, target_path: str, options: Optional[Dict[str, Any]] = None) -> bool:
        if options is None:
            options = {}

        quality = int(options.get("image_quality", 92))
        tgt_ext = os.path.splitext(target_path)[1].lower().lstrip(".")

        with Image.open(source_path) as img:
            # ICO formatına özel dönüşüm
            if tgt_ext == "ico":
                sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                # ICO RGBA'yı korumalıdır
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                img.save(target_path, format="ICO", sizes=sizes)
                return True

            # JPEG dönüşümünde şeffaflık beyaz arka plana yapıştırılmalıdır
            if tgt_ext in ("jpg", "jpeg"):
                if img.mode in ("RGBA", "LA", "P"):
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    alpha_img = img.convert("RGBA")
                    bg.paste(alpha_img, mask=alpha_img.split()[3])
                    img = bg
                elif img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(target_path, format="JPEG", quality=quality, optimize=True)
                return True

            # PDF dönüşümü
            if tgt_ext == "pdf":
                if img.mode in ("RGBA", "LA", "P"):
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    alpha_img = img.convert("RGBA")
                    bg.paste(alpha_img, mask=alpha_img.split()[3])
                    img = bg
                elif img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(target_path, format="PDF", resolution=100.0)
                return True

            # WebP dönüşümü
            if tgt_ext == "webp":
                save_kwargs = {"format": "WEBP", "quality": quality}
                # Animasyonlu GIF -> Animasyonlu WebP desteği
                if getattr(img, "is_animated", False):
                    save_kwargs["save_all"] = True
                img.save(target_path, **save_kwargs)
                return True

            # PNG dönüşümü
            if tgt_ext == "png":
                img.save(target_path, format="PNG", optimize=True)
                return True

            # BMP dönüşümü
            if tgt_ext == "bmp":
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                img.save(target_path, format="BMP")
                return True

            # TIFF dönüşümü
            if tgt_ext in ("tiff", "tif"):
                img.save(target_path, format="TIFF")
                return True

            # Genel kayıt
            img.save(target_path)
            return True
