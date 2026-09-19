"""
OBS Asistan - Üniversite Öğrenci Bilgi Sistemi Otomasyonu
"""

import sys

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

__version__ = "1.0.0"
__author__ = "Efe KIRBAŞ"
