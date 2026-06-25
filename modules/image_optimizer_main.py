"""
Главная функция для оптимизации изображений
Вызывает нужные функции из image_optimizer.py
"""

import os

from . import image_optimizer


def optimize_images(folder_path, limit_kb):
    """Главная функция оптимизации"""
    stats = {
        'processed': 0,
        'optimized': 0,
        'errors': 0,
        'saved_mb': 0
    }
    
    print(f"🔍 Поиск изображений в: {folder_path}")  # Отладка
    
    # Проходим по всем файлам в папке
    for root, dirs, files in os.walk(folder_path):
        print(f"📁 Сканируем: {root}")  # Отладка
        for file in files:
            ext = file.lower()
            if not (ext.endswith('.png') or ext.endswith('.jpg') or ext.endswith('.jpeg')):
                continue
                
            img_path = os.path.join(root, file)
            print(f"🖼 Обработка: {file}")  # Отладка
            
            try:
                size_kb = os.path.getsize(img_path) / 1024
                
                if size_kb <= limit_kb:
                    print(f"   ✓ Пропуск (уже меньше {limit_kb}KB)")  # Отладка
                    continue
                
                stats['processed'] += 1
                
                # PNG файлы
                if ext.endswith('.png'):
                    print("   📦 Сжатие PNG...")  # Отладка
                    # Сначала пробуем lossless oxipng
                    success, reduction = image_optimizer.optimize_png_oxipng(img_path)
                    if success:
                        stats['optimized'] += 1
                        stats['saved_mb'] += (size_kb - os.path.getsize(img_path)/1024) / 1024
                        print(f"   ✓ Lossless сжатие: -{reduction:.1f}%")  # Отладка
                        continue
                    
                    # Если lossless не помог, пробуем lossy
                    for colors in [256, 128, 64, 32]:
                        success, reduction = image_optimizer.optimize_png_lossy(img_path, colors)
                        new_size_kb = os.path.getsize(img_path) / 1024
                        if new_size_kb <= limit_kb:
                            stats['optimized'] += 1
                            stats['saved_mb'] += (size_kb - new_size_kb) / 1024
                            print(f"   ✓ Lossy сжатие ({colors} цветов): -{reduction:.1f}%")  # Отладка
                            break
                    else:
                        print(f"   ⚠ Не удалось сжать до {limit_kb}KB")  # Отладка
                
                # JPEG файлы
                elif ext.endswith(('.jpg', '.jpeg')):
                    print("   📸 Сжатие JPEG...")  # Отладка
                    for quality in range(85, 50, -5):
                        reduction = image_optimizer.optimize_jpeg(img_path, quality)
                        new_size_kb = os.path.getsize(img_path) / 1024
                        if new_size_kb <= limit_kb:
                            stats['optimized'] += 1
                            stats['saved_mb'] += (size_kb - new_size_kb) / 1024
                            print(f"   ✓ Качество {quality}: -{reduction:.1f}%")  # Отладка
                            break
                    else:
                        print(f"   ⚠ Не удалось сжать до {limit_kb}KB")  # Отладка
                            
            except Exception as e:
                stats['errors'] += 1
                print(f"   ❌ Ошибка: {e}")
    
    print(f"\n✅ Оптимизация завершена! Обработано: {stats['processed']}")  # Отладка
    return stats