"""
FileForm - Dönüştürücü Yöneticisi (Conversion Manager)
Tüm alt dönüştürücüleri koordine eder, dosya tiplerini tespit eder ve toplu işlemleri yürütür.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Callable
import send2trash

from core.config import resolve_output_path, load_settings
from .base import BaseConverter
from .image_converter import ImageConverter
from .pdf_converter import PdfConverter
from .office_converter import OfficeConverter
from .media_converter import MediaConverter
from .data_converter import DataConverter

class ConversionManager:
    def __init__(self):
        self.converters: List[BaseConverter] = [
            ImageConverter(),
            PdfConverter(),
            OfficeConverter(),
            MediaConverter(),
            DataConverter()
        ]

    def get_supported_targets(self, file_path: str) -> List[str]:
        """Verilen tek bir dosya için dönüştürülebilecek hedef formatları listeler."""
        ext = Path(file_path).suffix.lower()
        targets = set()
        for conv in self.converters:
            for t in conv.get_supported_targets(ext):
                targets.add(t)
        return sorted(list(targets))

    def get_common_targets(self, file_paths: List[str]) -> List[str]:
        """
        Seçilen birden fazla dosyanın ortak veya uygulanabilir hedef formatlarını bulur.
        Eğer tüm dosyalar aynı türdense (örn. hepsi resim) kesişimini döner.
        """
        if not file_paths:
            return []

        all_target_lists = [set(self.get_supported_targets(f)) for f in file_paths]
        # Önce ortak kesişimi bul
        common = set.intersection(*all_target_lists)
        if common:
            return sorted(list(common))

        # Kesişim boşsa (örn: hem resim hem video seçilmişse) birleşimdeki popüler formatları döner
        union = set.union(*all_target_lists)
        return sorted(list(union))

    def find_converter(self, source_ext: str, target_ext: str) -> Optional[BaseConverter]:
        """Uzantı eşleşmesine göre uygun dönüştürücüyü bulur."""
        for conv in self.converters:
            if conv.can_convert(source_ext, target_ext):
                return conv
        return None

    def convert_single(
        self,
        source_file: str,
        target_ext: str,
        options: Optional[Dict[str, Any]] = None,
        custom_target_path: Optional[str] = None
    ) -> Tuple[bool, str, str]:
        """
        Tek bir dosyayı dönüştürür.
        Dönüş: (Başarılı_mı, Çıktı_Dosya_Yolu, Hata_Mesajı)
        """
        if options is None:
            options = load_settings()

        src_path = Path(source_file)
        if not src_path.exists():
            return False, "", f"Kaynak dosya bulunamadı: {source_file}"

        src_ext = src_path.suffix.lower()
        converter = self.find_converter(src_ext, target_ext)
        if not converter:
            return False, "", f"{src_ext} formatından {target_ext} formatına dönüştürücü bulunamadı."

        out_path = custom_target_path or resolve_output_path(source_file, target_ext, options)

        try:
            success = converter.convert(source_file, out_path, options)
            if success:
                # İsteğe bağlı: Orijinal dosyayı Geri Dönüşüm Kutusu'na taşı
                if options.get("delete_originals", False):
                    try:
                        send2trash.send2trash(source_file)
                    except Exception as e:
                        print(f"Geri Dönüşüm Kutusu'na gönderme hatası: {e}")
                return True, out_path, ""
            else:
                return False, "", "Dönüştürme başarısız oldu."
        except Exception as e:
            return False, "", str(e)

    def convert_batch(
        self,
        file_paths: List[str],
        target_ext: str,
        options: Optional[Dict[str, Any]] = None,
        merge_images_to_pdf: bool = False,
        progress_callback: Optional[Callable[[int, int, str, bool], None]] = None
    ) -> List[Tuple[str, bool, str, str]]:
        """
        Toplu dosya dönüştürme gerçekleştirir.
        Dönüş: [(Kaynak_Dosya, Başarılı_mı, Çıktı_Yolu, Hata_Mesajı), ...]
        """
        if options is None:
            options = load_settings()

        results = []
        total = len(file_paths)

        # Özel Durum: Birden fazla görseli tek bir PDF'te birleştirme seçeneği
        if merge_images_to_pdf and target_ext.lower().lstrip(".") == "pdf" and total > 1:
            first_file = file_paths[0]
            merged_pdf_path = resolve_output_path(first_file, "pdf", options)
            stem = Path(first_file).stem
            merged_pdf_path = str(Path(merged_pdf_path).parent / f"{stem}_birlestirilmis.pdf")

            try:
                ok = PdfConverter.merge_images_to_pdf(file_paths, merged_pdf_path)
                if ok:
                    if options.get("delete_originals", False):
                        for f in file_paths:
                            try:
                                send2trash.send2trash(f)
                            except Exception:
                                pass
                    for f in file_paths:
                        results.append((f, True, merged_pdf_path, ""))
                    if progress_callback:
                        progress_callback(total, total, merged_pdf_path, True)
                    return results
            except Exception as e:
                # Hata durumunda tek tek dönüştürmeye devam et
                pass

        for idx, file_path in enumerate(file_paths):
            ok, out_path, err = self.convert_single(file_path, target_ext, options)
            results.append((file_path, ok, out_path, err))
            if progress_callback:
                progress_callback(idx + 1, total, file_path, ok)

        return results
