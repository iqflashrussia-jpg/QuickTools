import os

from . import archive_handler, image_optimizer


def find_best_settings(folder_path, target_kb, log_func):
    """Гибридный подбор: lossless для больших лимитов, lossy для малых"""
    target_bytes = target_kb * 1024
    max_allowed = target_bytes - (5 * 1024)
    
    jpeg_files = []
    png_files = []
    other_files = []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and not file.endswith('.fla'):
            if file.lower().endswith(('.jpg', '.jpeg')):
                jpeg_files.append(file_path)
            elif file.lower().endswith('.png'):
                png_files.append(file_path)
            else:
                other_files.append(file_path)
    
    other_size = sum(os.path.getsize(f) for f in other_files)
    
    if not jpeg_files and not png_files:
        return None, None, None, None, "Нет изображений"
    
    log_func(f"  JPEG: {len(jpeg_files)}, PNG: {len(png_files)}, другие: {other_size//1024}KB")
    
    use_lossless = target_kb >= 250 and image_optimizer.check_oxipng()
    
    if use_lossless:
        log_func(f"  📌 Используем LOSSLESS сжатие (Oxipng) для PNG")
        for jpg_q in [85, 90]:
            for level in [1, 2, 3, 4]:
                test_size = archive_handler.get_archive_size_lossless(folder_path, jpg_q, level)
                log_func(f"  Тест JPEG={jpg_q}, level={level}: архив {test_size//1024}KB")
                if test_size <= max_allowed:
                    return 'lossless', jpg_q, level, test_size, f"🎯 Lossless: JPEG={jpg_q}, PNG level={level} | Архив {test_size//1024}KB / {target_kb}KB"
        log_func(f"  ⚠️ Lossless не хватило, пробуем Lossy...")
    
    log_func(f"  📌 Используем LOSSY сжатие (pngquant) для PNG")
    
    if target_kb < 200:
        jpg_qualities = [75, 65, 55, 45]
    else:
        jpg_qualities = [85, 75, 65]
    
    colors_list = [256, 192, 128, 96, 64, 48, 32, 24, 16]
    
    for jpg_q in jpg_qualities:
        for colors in colors_list:
            test_size = archive_handler.get_archive_size_lossy(folder_path, jpg_q, colors)
            log_func(f"  Тест JPEG={jpg_q}, colors={colors}: архив {test_size//1024}KB")
            if test_size <= max_allowed:
                return 'lossy', jpg_q, colors, test_size, f"🎯 Lossy: JPEG={jpg_q}, PNG={colors} цветов | Архив {test_size//1024}KB / {target_kb}KB"
    
    min_test = archive_handler.get_archive_size_lossy(folder_path, 45, 16)
    return None, None, None, None, f"❌ Лимит {target_kb}KB недостижим. Минимальный архив: {min_test//1024}KB"