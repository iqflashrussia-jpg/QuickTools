import os
import sys


def get_oxipng_path():
    """Возвращает путь к oxipng.exe"""
    exe_dir = os.path.dirname(sys.argv[0])
    exe_path = os.path.join(exe_dir, "oxipng.exe")
    if os.path.exists(exe_path):
        return exe_path
    if os.path.exists("oxipng.exe"):
        return "oxipng.exe"
    import shutil
    path_exe = shutil.which("oxipng")
    if path_exe:
        return path_exe
    return None

# Цветовая схема
COLORS = {
    "PRIMARY": "#4a90d9",
    "SUCCESS": "#6b8c5c",
    "ERROR": "#c65d5d",
    "WARNING": "#d4a55e",
    "BG_CARD": "#2d2d2d",
    "BG_INPUT": "#252525",
    "TEXT": "#e0e0e0",
    "TEXT_SECONDARY": "#a0a0a0",
}