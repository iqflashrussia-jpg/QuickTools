import os
import zipfile
import os
import shutil
import tempfile
from . import image_optimizer

def get_archive_size_lossless(folder_path, jpg_quality, png_level):
    """Тест с lossless сжатием (Oxipng)"""
    all_files = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and not file.endswith('.fla'):
            all_files.append(file_path)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for src in all_files:
            dst = os.path.join(tmpdir, os.path.basename(src))
            shutil.copy2(src, dst)
            if src.lower().endswith(('.jpg', '.jpeg')):
                image_optimizer.optimize_jpeg(dst, jpg_quality)
            elif src.lower().endswith('.png'):
                image_optimizer.optimize_png_oxipng(dst, png_level)
        
        zip_path = os.path.join(tmpdir, "test.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(tmpdir):
                for f in files:
                    if f == "test.zip":
                        continue
                    zf.write(os.path.join(root, f), f)
        return os.path.getsize(zip_path)

def get_archive_size_lossy(folder_path, jpg_quality, png_colors):
    """Тест с lossy сжатием (pngquant + JPEG сжатие)"""
    all_files = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and not file.endswith('.fla'):
            all_files.append(file_path)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for src in all_files:
            dst = os.path.join(tmpdir, os.path.basename(src))
            shutil.copy2(src, dst)
            if src.lower().endswith(('.jpg', '.jpeg')):
                image_optimizer.optimize_jpeg(dst, jpg_quality)
            elif src.lower().endswith('.png'):
                image_optimizer.optimize_png_lossy(dst, png_colors)
        
        zip_path = os.path.join(tmpdir, "test.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(tmpdir):
                for f in files:
                    if f == "test.zip":
                        continue
                    zf.write(os.path.join(root, f), f)
        return os.path.getsize(zip_path)

def create_archive(folder_path, output_path):
    """Создание реального архива"""
    files = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and not file.endswith('.fla'):
            files.append(file_path)
    
    if not files:
        return None
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, os.path.basename(f))
    
    return os.path.getsize(output_path)

def delete_all_archives(root_path, log_func):
    """Удаление всех ZIP и папок zip"""
    all_zips = []
    all_zip_folders = []
    
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith('.zip'):
                all_zips.append(os.path.join(root, file))
        for dir_name in dirs:
            if dir_name.lower() == "zip":
                all_zip_folders.append(os.path.join(root, dir_name))
    
    deleted_zips = 0
    deleted_folders = 0
    
    for file_path in all_zips:
        try:
            os.remove(file_path)
            deleted_zips += 1
            log_func(f"  ✅ Удалён: {os.path.basename(file_path)}")
        except Exception as e:
            log_func(f"  ❌ Ошибка: {os.path.basename(file_path)}")
    
    for folder_path in all_zip_folders:
        try:
            shutil.rmtree(folder_path)
            deleted_folders += 1
            log_func(f"  ✅ Удалена папка: {os.path.basename(folder_path)}")
        except Exception as e:
            log_func(f"  ❌ Ошибка: {os.path.basename(folder_path)}")
    
    return deleted_zips, deleted_folders