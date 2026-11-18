"""
FileForm - Temel Dönüştürücü Arayüzü
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseConverter(ABC):
    """Tüm format dönüştürücüler için soyut temel sınıf."""

    @abstractmethod
    def can_convert(self, source_ext: str, target_ext: str) -> bool:
        """Belirtilen kaynak uzantıdan hedef uzantıya dönüşüm destekleniyor mu?"""
        pass

    @abstractmethod
    def get_supported_targets(self, source_ext: str) -> List[str]:
        """Bu kaynak uzantı için desteklenen hedef formatların listesini döner."""
        pass

    @abstractmethod
    def convert(self, source_path: str, target_path: str, options: Optional[Dict[str, Any]] = None) -> bool:
        """
        Dönüştürme işlemini gerçekleştirir.
        Başarılıysa True, aksi halde False veya Exception fırlatır.
        """
        pass
