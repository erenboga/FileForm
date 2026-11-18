"""
FileForm - Multimedya (Ses ve Video) Dönüştürücü (FFmpeg Tabanlı)
"""
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import imageio_ffmpeg
from .base import BaseConverter

class MediaConverter(BaseConverter):
    VIDEO_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".m4v"}
    AUDIO_EXTS = {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"}

    VIDEO_TARGETS = ["mp4", "webm", "gif", "mp3", "wav", "mkv", "avi"]
    AUDIO_TARGETS = ["mp3", "wav", "aac", "flac", "ogg", "m4a"]

    def __init__(self):
        self._ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def can_convert(self, source_ext: str, target_ext: str) -> bool:
        src = source_ext.lower()
        if not src.startswith("."):
            src = f".{src}"
        tgt = target_ext.lower().lstrip(".")

        if src in self.VIDEO_EXTS:
            return tgt in self.VIDEO_TARGETS
        if src in self.AUDIO_EXTS:
            return tgt in self.AUDIO_TARGETS
        return False

    def get_supported_targets(self, source_ext: str) -> List[str]:
        src = source_ext.lower()
        if not src.startswith("."):
            src = f".{src}"
        curr = src.lstrip(".")
        if src in self.VIDEO_EXTS:
            return [t for t in self.VIDEO_TARGETS if t != curr]
        if src in self.AUDIO_EXTS:
            return [t for t in self.AUDIO_TARGETS if t != curr]
        return []

    def convert(self, source_path: str, target_path: str, options: Optional[Dict[str, Any]] = None) -> bool:
        if options is None:
            options = {}

        src_ext = Path(source_path).suffix.lower()
        tgt_ext = Path(target_path).suffix.lower().lstrip(".")
        crf = str(options.get("video_crf", 23))
        audio_bitrate = str(options.get("audio_bitrate", "192k"))

        # FFmpeg komut dizisi oluştur
        cmd = [self._ffmpeg_exe, "-y", "-i", source_path]

        # 1. Video -> GIF Dönüşümü (Yüksek kaliteli palet filtresi ile)
        if tgt_ext == "gif":
            cmd.extend([
                "-vf", "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer",
                target_path
            ])

        # 2. Videodan Ses Ayıklama veya Ses Dönüşümü -> MP3
        elif tgt_ext == "mp3":
            cmd.extend([
                "-vn", "-c:a", "libmp3lame", "-b:a", audio_bitrate,
                target_path
            ])

        # 3. Videodan Ses Ayıklama veya Ses Dönüşümü -> WAV
        elif tgt_ext == "wav":
            cmd.extend([
                "-vn", "-c:a", "pcm_s16le",
                target_path
            ])

        # 4. Ses Dönüşümü (AAC, FLAC, OGG, M4A)
        elif src_ext in self.AUDIO_EXTS or (src_ext in self.VIDEO_EXTS and tgt_ext in self.AUDIO_TARGETS):
            cmd.extend([
                "-vn", target_path
            ])

        # 5. Video -> MP4 (H.264 / AAC)
        elif tgt_ext == "mp4":
            cmd.extend([
                "-c:v", "libx264", "-crf", crf, "-preset", "fast",
                "-c:a", "aac", "-b:a", audio_bitrate,
                "-movflags", "+faststart",
                target_path
            ])

        # 6. Video -> WebM (VP9 / Opus)
        elif tgt_ext == "webm":
            cmd.extend([
                "-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0",
                "-c:a", "libopus",
                target_path
            ])

        # 7. Diğer Video Formatları (MKV, AVI)
        else:
            cmd.append(target_path)

        # Sessizce arka planda çalıştır
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        proc = subprocess.run(cmd, capture_output=True, text=True, creationflags=flags)

        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg dönüştürme hatası: {proc.stderr[:300]}")

        return True
