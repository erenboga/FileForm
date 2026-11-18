"""
FileForm - Dönüştürücü Motoru Testleri
"""
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from PIL import Image
import pandas as pd

from converters.manager import ConversionManager
from converters.pdf_converter import PdfConverter

class TestConverters(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="fileform_test_")
        self.manager = ConversionManager()

        # Test görseli oluştur (100x100 RGB ve RGBA)
        self.sample_png = os.path.join(self.test_dir, "sample.png")
        img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
        img.save(self.sample_png)

        self.sample_png2 = os.path.join(self.test_dir, "sample2.png")
        img2 = Image.new("RGB", (100, 100), (0, 255, 0))
        img2.save(self.sample_png2)

        # Test CSV dosyası oluştur
        self.sample_csv = os.path.join(self.test_dir, "data.csv")
        df = pd.DataFrame({"isim": ["Ali", "Ayşe", "Mehmet"], "puan": [95, 88, 76]})
        df.to_csv(self.sample_csv, index=False)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_image_to_jpg(self):
        ok, out, err = self.manager.convert_single(self.sample_png, "jpg")
        self.assertTrue(ok, f"JPG dönüşüm hatası: {err}")
        self.assertTrue(os.path.exists(out))
        with Image.open(out) as im:
            self.assertEqual(im.format, "JPEG")

    def test_image_to_webp(self):
        ok, out, err = self.manager.convert_single(self.sample_png, "webp")
        self.assertTrue(ok, f"WebP dönüşüm hatası: {err}")
        self.assertTrue(os.path.exists(out))
        with Image.open(out) as im:
            self.assertEqual(im.format, "WEBP")

    def test_image_to_ico(self):
        ok, out, err = self.manager.convert_single(self.sample_png, "ico")
        self.assertTrue(ok, f"ICO dönüşüm hatası: {err}")
        self.assertTrue(os.path.exists(out))
        with Image.open(out) as im:
            self.assertEqual(im.format, "ICO")

    def test_image_to_pdf_and_merge(self):
        # Tek görsel -> PDF
        ok, out, err = self.manager.convert_single(self.sample_png, "pdf")
        self.assertTrue(ok, f"PDF dönüşüm hatası: {err}")
        self.assertTrue(os.path.exists(out))

        # Çoklu görsel birleştirme
        merged_pdf = os.path.join(self.test_dir, "merged.pdf")
        merge_ok = PdfConverter.merge_images_to_pdf([self.sample_png, self.sample_png2], merged_pdf)
        self.assertTrue(merge_ok)
        self.assertTrue(os.path.exists(merged_pdf))

        # PDF -> Resim
        ok_render, out_img, err_render = self.manager.convert_single(merged_pdf, "png")
        self.assertTrue(ok_render, f"PDF render hatası: {err_render}")

    def test_data_conversions(self):
        # CSV -> XLSX
        ok, out_xlsx, err = self.manager.convert_single(self.sample_csv, "xlsx")
        self.assertTrue(ok, f"XLSX dönüşüm hatası: {err}")
        self.assertTrue(os.path.exists(out_xlsx))

        # XLSX -> JSON
        ok_json, out_json, err_json = self.manager.convert_single(out_xlsx, "json")
        self.assertTrue(ok_json, f"JSON dönüşüm hatası: {err_json}")
        self.assertTrue(os.path.exists(out_json))

if __name__ == "__main__":
    unittest.main()
