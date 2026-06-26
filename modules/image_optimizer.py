import os
import subprocess

import imagequant
from PIL import Image

from . import config


def check_oxipng():
    """Проверяет, доступен ли oxipng"""
    return config.get_oxipng_path() is not None

def optimize_png_oxipng(img_path, level=2):
    """Lossless сжатие PNG через oxipng"""
    try:
        oxipng_path = config.get_oxipng_path()
        if not oxipng_path:
            return False, 0
        orig_size = os.path.getsize(img_path)
        subprocess.run(
            [oxipng_path, '-o', str(level), '--strip', 'safe', '--out', img_path, img_path],
            capture_output=True
        )
        new_size = os.path.getsize(img_path)
        reduction = (1 - new_size/orig_size) * 100
        return True, reduction
    except Exception:
        return False, 0

def optimize_png_lossy(img_path, colors):
    """Lossy сжатие PNG через pngquant"""
    try:
        orig_size = os.path.getsize(img_path)
        with Image.open(img_path) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            quantized = imagequant.quantize_pil_image(
                img, max_colors=colors, dithering_level=1.0
            )
            quantized.save(img_path, 'PNG', optimize=True, compress_level=9)
        new_size = os.path.getsize(img_path)
        reduction = (1 - new_size/orig_size) * 100
        return True, reduction
    except Exception:
        return False, 0

def optimize_jpeg(img_path, quality):
    """Сжатие JPEG через PIL"""
    try:
        orig_size = os.path.getsize(img_path)
        with Image.open(img_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(img_path, 'JPEG', quality=quality, optimize=True, progressive=True)
        new_size = os.path.getsize(img_path)
        return (1 - new_size/orig_size) * 100
    except Exception:
        return 0