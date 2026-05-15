import flet as ft
import os
import zipfile
import shutil
import tempfile
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog
import time
import asyncio
from PIL import Image
import imagequant

# Путь к oxipng.exe
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

OXIPNG_PATH = get_oxipng_path()

def main(page: ft.Page):
    page.title = "QuickTools"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 25
    page.bgcolor = "#1e1e1e"
    
    page.window.width = 1150
    page.window.height = 800
    page.window.min_width = 1100
    page.window.min_height = 750
    page.window.resizable = True
    page.update()
    
    selected_path = None
    is_working = False
    
    # Цветовая схема
    PRIMARY = "#4a90d9"
    SUCCESS = "#6b8c5c"
    ERROR = "#c65d5d"
    WARNING = "#d4a55e"
    BG_CARD = "#2d2d2d"
    BG_INPUT = "#252525"
    TEXT_COLOR = "#e0e0e0"
    TEXT_SECONDARY = "#a0a0a0"
    
    # Элементы UI
    folder_text = ft.Text(value="Папка не выбрана", size=14, color=TEXT_SECONDARY)
    output_text = ft.TextField(
        multiline=True,
        min_lines=35,
        max_lines=40,
        read_only=True,
        value="Готов к работе...\n",
        text_size=11,
        bgcolor="#252525",
        border_color="#3d3d3d",
        color=TEXT_COLOR,
    )
    
    # Поля для переименования
    rename_find = ft.TextField(
        hint_text="исходный текст",
        expand=True,
        height=40,
        text_size=13,
        bgcolor=BG_INPUT,
        border_color="#3d3d3d",
        color=TEXT_COLOR,
    )
    rename_replace = ft.TextField(
        hint_text="финальный текст",
        expand=True,
        height=40,
        text_size=13,
        bgcolor=BG_INPUT,
        border_color="#3d3d3d",
        color=TEXT_COLOR,
    )
    
    # Поля для авто-оптимизации под размер
    target_archive_size = ft.TextField(
        value="300",
        hint_text="целевой размер в KB",
        width=120,
        height=40,
        text_size=13,
        text_align=ft.TextAlign.CENTER,
        bgcolor=BG_INPUT,
        border_color="#3d3d3d",
        color=TEXT_COLOR,
    )
    
    def log(message):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        output_text.value += f"[{timestamp}] {message}\n"
        lines = output_text.value.split('\n')
        if len(lines) > 500:
            output_text.value = '\n'.join(lines[-400:])
        page.update()
    
    def clear_output(e):
        output_text.value = "Лог очищен\n"
        page.update()
    
    def pick_folder(e):
        nonlocal selected_path
        log("Открытие диалога выбора папки...")
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_selected = filedialog.askdirectory(title="Выберите рабочую папку")
        root.destroy()
        if folder_selected:
            selected_path = folder_selected
            folder_text.value = os.path.basename(selected_path)
            folder_text.color = PRIMARY
            folder_text.tooltip = selected_path
            log(f"Выбрана папка: {selected_path}")
        else:
            log("Выбор папки отменён")
    
    def check_oxipng():
        return OXIPNG_PATH is not None
    
    def optimize_png_oxipng(img_path, level=2):
        try:
            if not OXIPNG_PATH:
                return False, 0
            orig_size = os.path.getsize(img_path)
            subprocess.run(
                [OXIPNG_PATH, '-o', str(level), '--strip', 'safe', '--out', img_path, img_path],
                capture_output=True
            )
            new_size = os.path.getsize(img_path)
            reduction = (1 - new_size/orig_size) * 100
            return True, reduction
        except:
            return False, 0
    
    def optimize_png_lossy(img_path, colors):
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
        except:
            return False, 0
    
    def optimize_jpeg(img_path, quality):
        try:
            orig_size = os.path.getsize(img_path)
            with Image.open(img_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(img_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            new_size = os.path.getsize(img_path)
            return (1 - new_size/orig_size) * 100
        except:
            return 0
    
    def get_archive_size_lossless(folder_path, jpg_quality, png_level):
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
                    optimize_jpeg(dst, jpg_quality)
                elif src.lower().endswith('.png'):
                    optimize_png_oxipng(dst, png_level)
            
            zip_path = os.path.join(tmpdir, "test.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(tmpdir):
                    for f in files:
                        if f == "test.zip":
                            continue
                        zf.write(os.path.join(root, f), f)
            return os.path.getsize(zip_path)
    
    def get_archive_size_lossy(folder_path, jpg_quality, png_colors):
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
                    optimize_jpeg(dst, jpg_quality)
                elif src.lower().endswith('.png'):
                    optimize_png_lossy(dst, png_colors)
            
            zip_path = os.path.join(tmpdir, "test.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(tmpdir):
                    for f in files:
                        if f == "test.zip":
                            continue
                        zf.write(os.path.join(root, f), f)
            return os.path.getsize(zip_path)
    
    def find_size_folders(base_path):
        folders = []
        for platform in os.listdir(base_path):
            platform_path = os.path.join(base_path, platform)
            if not os.path.isdir(platform_path) or platform == 'zip':
                continue
            for campaign in os.listdir(platform_path):
                campaign_path = os.path.join(platform_path, campaign)
                if not os.path.isdir(campaign_path):
                    continue
                for size_folder in os.listdir(campaign_path):
                    size_path = os.path.join(campaign_path, size_folder)
                    if os.path.isdir(size_path) and 'x' in size_folder.lower():
                        folders.append({
                            'path': size_path,
                            'platform': platform,
                            'campaign': campaign,
                            'size': size_folder
                        })
        return folders
    
    def find_best_settings(folder_path, target_kb):
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
        
        log(f"  JPEG: {len(jpeg_files)}, PNG: {len(png_files)}, другие: {other_size//1024}KB")
        
        use_lossless = target_kb >= 250 and check_oxipng()
        
        if use_lossless:
            log(f"  📌 Используем LOSSLESS сжатие (Oxipng) для PNG")
            for jpg_q in [85, 90]:
                for level in [1, 2, 3, 4]:
                    test_size = get_archive_size_lossless(folder_path, jpg_q, level)
                    log(f"  Тест JPEG={jpg_q}, level={level}: архив {test_size//1024}KB")
                    if test_size <= max_allowed:
                        return 'lossless', jpg_q, level, test_size, f"🎯 Lossless: JPEG={jpg_q}, PNG level={level} | Архив {test_size//1024}KB / {target_kb}KB"
            log(f"  ⚠️ Lossless не хватило, пробуем Lossy...")
        
        log(f"  📌 Используем LOSSY сжатие (pngquant) для PNG")
        
        if target_kb < 200:
            jpg_qualities = [75, 65, 55, 45]
        else:
            jpg_qualities = [85, 75, 65]
        
        colors_list = [256, 192, 128, 96, 64, 48, 32, 24, 16]
        
        for jpg_q in jpg_qualities:
            for colors in colors_list:
                test_size = get_archive_size_lossy(folder_path, jpg_q, colors)
                log(f"  Тест JPEG={jpg_q}, colors={colors}: архив {test_size//1024}KB")
                if test_size <= max_allowed:
                    return 'lossy', jpg_q, colors, test_size, f"🎯 Lossy: JPEG={jpg_q}, PNG={colors} цветов | Архив {test_size//1024}KB / {target_kb}KB"
        
        min_test = get_archive_size_lossy(folder_path, 45, 16)
        return None, None, None, None, f"❌ Лимит {target_kb}KB недостижим. Минимальный архив: {min_test//1024}KB"
    
    def optimize_all_with_target_size(e):
        nonlocal is_working
        if not selected_path:
            log("Сначала выберите папку!")
            return
        if is_working:
            log("Операция уже выполняется, подождите...")
            return
        
        try:
            target_kb = int(target_archive_size.value)
            if target_kb < 50:
                target_kb = 50
                target_archive_size.value = "50"
        except:
            target_kb = 300
            target_archive_size.value = "300"
        
        is_working = True
        
        async def optimize_task():
            nonlocal is_working
            try:
                log(f"\n{'='*60}")
                log(f"🎯 ОПТИМИЗАЦИЯ ВСЕХ ПАПОК ПОД РАЗМЕР")
                log(f"Папка: {selected_path}")
                log(f"Целевой размер архива: {target_kb} KB")
                if check_oxipng():
                    log(f"✅ Oxipng найден (lossless для лимитов ≥250KB)")
                log(f"{'='*60}")
                
                size_folders = find_size_folders(selected_path)
                if not size_folders:
                    log("Папки с 'x' в имени не найдены")
                    is_working = False
                    return
                
                log(f"Найдено папок: {len(size_folders)}")
                page.update()
                
                total_before = 0
                total_after = 0
                processed = 0
                skipped = 0
                
                for idx, folder_info in enumerate(size_folders):
                    folder_path = folder_info['path']
                    folder_name = f"{folder_info['platform']}/{folder_info['campaign']}/{folder_info['size']}"
                    log(f"\n[{idx+1}/{len(size_folders)}] {folder_name}")
                    
                    result = find_best_settings(folder_path, target_kb)
                    
                    if result[0] is None:
                        log(f"  {result[4]}")
                        skipped += 1
                        continue
                    
                    method, jpg_q, png_param, archive_size, msg = result
                    log(f"  {msg}")
                    log(f"  🔄 Применяем сжатие...")
                    
                    folder_before = 0
                    folder_after = 0
                    
                    for file in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file)
                        if not os.path.isfile(file_path) or file.endswith('.fla'):
                            continue
                        
                        old_size = os.path.getsize(file_path)
                        
                        if file.lower().endswith(('.jpg', '.jpeg')):
                            folder_before += old_size
                            reduction = optimize_jpeg(file_path, jpg_q)
                            new_size = os.path.getsize(file_path)
                            folder_after += new_size
                            if reduction > 0:
                                log(f"    ✅ {file}: {old_size//1024}KB → {new_size//1024}KB (-{reduction:.0f}%)")
                            else:
                                log(f"    ✓ {file}: {old_size//1024}KB")
                        
                        elif file.lower().endswith('.png'):
                            folder_before += old_size
                            if method == 'lossless':
                                success, reduction = optimize_png_oxipng(file_path, png_param)
                            else:
                                success, reduction = optimize_png_lossy(file_path, png_param)
                            new_size = os.path.getsize(file_path)
                            folder_after += new_size
                            if success and reduction > 0:
                                log(f"    ✅ {file}: {old_size//1024}KB → {new_size//1024}KB (-{reduction:.0f}%)")
                            else:
                                log(f"    ✓ {file}: {old_size//1024}KB")
                        else:
                            folder_before += old_size
                            folder_after += old_size
                    
                    folder_reduction = (1 - folder_after/folder_before) * 100 if folder_before > 0 else 0
                    total_before += folder_before
                    total_after += folder_after
                    processed += 1
                    log(f"  📊 Итого папки: {folder_before//1024}KB → {folder_after//1024}KB (сжатие {folder_reduction:.0f}%)")
                    await asyncio.sleep(0.01)
                
                log(f"\n{'='*60}")
                log(f"✅ ОПТИМИЗАЦИЯ ЗАВЕРШЕНА!")
                log(f"Обработано папок: {processed}")
                log(f"Пропущено: {skipped}")
                if total_before > 0:
                    total_reduction = (1 - total_after/total_before) * 100
                    log(f"Общий размер: {total_before//1024}KB → {total_after//1024}KB")
                    log(f"Общее сжатие: {total_reduction:.0f}%")
                log(f"🎯 Теперь можно запустить архивацию!")
                log(f"{'='*60}\n")
                
            except Exception as e:
                log(f"❌ Критическая ошибка: {str(e)}")
                import traceback
                traceback.print_exc()
            finally:
                is_working = False
        
        asyncio.create_task(optimize_task())
    
    def archive_all_folders(e):
        nonlocal is_working
        if not selected_path:
            log("Сначала выберите папку!")
            return
        if is_working:
            log("Операция уже выполняется, подождите...")
            return
        
        is_working = True
        log("\n📦 АРХИВАЦИЯ ВСЕХ ПАПОК")
        page.update()
        
        async def archive_task():
            nonlocal is_working
            try:
                size_folders = find_size_folders(selected_path)
                if not size_folders:
                    log("Папки с 'x' в имени не найдены")
                    is_working = False
                    return
                
                total = len(size_folders)
                log(f"Найдено папок: {total}")
                page.update()
                
                archive_count = 0
                total_before = 0
                total_after = 0
                
                for idx, folder_info in enumerate(size_folders):
                    folder_path = folder_info['path']
                    platform = folder_info['platform']
                    campaign = folder_info['campaign']
                    size_name = folder_info['size']
                    
                    log(f"\n📦 {idx+1}/{total}: {platform}/{campaign}/{size_name}")
                    
                    files_to_zip = []
                    folder_size = 0
                    
                    for file in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file)
                        if os.path.isfile(file_path) and not file.endswith('.fla'):
                            files_to_zip.append(file_path)
                            folder_size += os.path.getsize(file_path)
                    
                    log(f"  Файлов: {len(files_to_zip)} (без .fla)")
                    log(f"  Размер: {folder_size // 1024} KB")
                    
                    if files_to_zip:
                        zip_name = f"{size_name}_{campaign}_{platform}.zip"
                        zip_output_dir = os.path.join(os.path.dirname(folder_path), "zip")
                        
                        try:
                            os.makedirs(zip_output_dir, exist_ok=True)
                            zip_path = os.path.join(zip_output_dir, zip_name)
                            
                            if os.path.exists(zip_path):
                                log(f"  ⚠️ Архив уже существует: {zip_name}")
                                continue
                            
                            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                                for file in files_to_zip:
                                    zipf.write(file, os.path.basename(file))
                            
                            archive_size = os.path.getsize(zip_path)
                            total_before += folder_size
                            total_after += archive_size
                            
                            reduction = (1 - archive_size/folder_size) * 100 if folder_size > 0 else 0
                            log(f"  ✅ Создан: {zip_name}")
                            log(f"     Размер: {archive_size // 1024} KB (сжатие {reduction:.0f}%)")
                            archive_count += 1
                        except Exception as e:
                            log(f"  ❌ Ошибка: {str(e)}")
                    else:
                        log(f"  ⚠️ Нет файлов для архивации")
                    
                    await asyncio.sleep(0.01)
                
                log(f"\n{'='*60}")
                log(f"✅ АРХИВАЦИЯ ЗАВЕРШЕНА!")
                log(f"Создано архивов: {archive_count} из {total}")
                if archive_count > 0:
                    log(f"Общий размер: {total_before//1024}KB → {total_after//1024}KB")
                    log(f"Общее сжатие: {(1 - total_after/total_before)*100:.0f}%")
                log(f"{'='*60}\n")
                
            except Exception as e:
                log(f"❌ Ошибка: {str(e)}")
            finally:
                is_working = False
        
        asyncio.create_task(archive_task())
    
    def delete_all_zips(e):
        nonlocal is_working
        if not selected_path:
            log("Сначала выберите папку!")
            return
        if is_working:
            log("Операция уже выполняется, подождите...")
            return
        
        is_working = True
        log("\n🗑️ УДАЛЕНИЕ ВСЕХ ZIP ФАЙЛОВ И ПАПОК")
        page.update()
        
        async def delete_task():
            nonlocal is_working
            try:
                all_zips = []
                all_zip_folders = []
                
                for root, dirs, files in os.walk(selected_path):
                    for file in files:
                        if file.endswith('.zip'):
                            all_zips.append(os.path.join(root, file))
                    for dir_name in dirs:
                        if dir_name.lower() == "zip":
                            all_zip_folders.append(os.path.join(root, dir_name))
                    await asyncio.sleep(0.01)
                
                total_items = len(all_zips) + len(all_zip_folders)
                if total_items == 0:
                    log("Архивы и папки zip не найдены")
                    is_working = False
                    return
                
                log(f"Найдено ZIP: {len(all_zips)}, папок zip: {len(all_zip_folders)}")
                page.update()
                
                deleted_zips = 0
                deleted_folders = 0
                
                for file_path in all_zips:
                    try:
                        os.remove(file_path)
                        deleted_zips += 1
                        log(f"  ✅ Удалён: {os.path.basename(file_path)}")
                    except Exception as e:
                        log(f"  ❌ Ошибка: {os.path.basename(file_path)}")
                    await asyncio.sleep(0.01)
                
                for folder_path in all_zip_folders:
                    try:
                        shutil.rmtree(folder_path)
                        deleted_folders += 1
                        log(f"  ✅ Удалена папка: {os.path.basename(folder_path)}")
                    except Exception as e:
                        log(f"  ❌ Ошибка: {os.path.basename(folder_path)}")
                    await asyncio.sleep(0.01)
                
                log(f"\n✅ УДАЛЕНИЕ ЗАВЕРШЕНО!")
                log(f"Удалено ZIP: {deleted_zips}, папок zip: {deleted_folders}")
                
            except Exception as e:
                log(f"❌ Ошибка: {str(e)}")
            finally:
                is_working = False
        
        asyncio.create_task(delete_task())
    
    # === .fla операции ===
    size_input = ft.TextField(
        hint_text="240x400",
        width=180,
        height=40,
        text_size=13,
        text_align=ft.TextAlign.CENTER,
        bgcolor=BG_INPUT,
        border_color="#3d3d3d",
        color=TEXT_COLOR,
    )
    
    def pick_folder_for_fla(title, callback):
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        initial_dir = selected_path if selected_path else os.path.expanduser("~")
        folder_selected = filedialog.askdirectory(title=title, initialdir=initial_dir)
        root.destroy()
        if folder_selected:
            callback(folder_selected)
        else:
            log("Выбор папки отменён")
    
    def open_fla_by_size_in_folder(folder_path):
        size = size_input.value.strip()
        if not size:
            log("Введите размер файла!")
            return
        
        log(f"\n🔍 ПОИСК {size}.fla в папке: {folder_path}")
        
        async def search_task():
            nonlocal is_working
            is_working = True
            start_time = time.time()
            try:
                found_files = []
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        if file == f"{size}.fla":
                            found_files.append(os.path.join(root, file))
                    await asyncio.sleep(0.01)
                
                total = len(found_files)
                if total == 0:
                    log(f"Файл {size}.fla не найден")
                else:
                    log(f"Найдено файлов: {total}")
                    page.update()
                    for file_path in found_files:
                        try:
                            os.startfile(file_path)
                            log(f"  ✅ Открыт: {os.path.basename(file_path)}")
                        except Exception as e:
                            log(f"  ❌ Ошибка: {os.path.basename(file_path)}")
                        await asyncio.sleep(0.05)
                    elapsed = time.time() - start_time
                    log(f"\n✅ Открыто файлов: {total} за {elapsed:.1f} сек")
            except Exception as e:
                log(f"❌ Ошибка: {str(e)}")
            finally:
                is_working = False
        
        asyncio.create_task(search_task())
    
    def open_all_fla_in_folder(folder_path):
        log(f"\n🔍 ПОИСК ВСЕХ .fla в папке: {folder_path}")
        
        async def search_task():
            nonlocal is_working
            is_working = True
            start_time = time.time()
            try:
                found_files = []
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        if file.endswith('.fla'):
                            found_files.append(os.path.join(root, file))
                    await asyncio.sleep(0.01)
                
                total = len(found_files)
                if total == 0:
                    log(".fla файлы не найдены")
                else:
                    log(f"Найдено .fla файлов: {total}")
                    page.update()
                    for idx, file_path in enumerate(found_files):
                        try:
                            os.startfile(file_path)
                            if (idx + 1) % 10 == 0:
                                log(f"  Открыто {idx+1}/{total} файлов")
                        except Exception as e:
                            log(f"  ❌ Ошибка: {os.path.basename(file_path)}")
                        await asyncio.sleep(0.03)
                    elapsed = time.time() - start_time
                    log(f"\n✅ Открыто всех .fla файлов: {total} за {elapsed:.1f} сек")
            except Exception as e:
                log(f"❌ Ошибка: {str(e)}")
            finally:
                is_working = False
        
        asyncio.create_task(search_task())
    
    def run_fla_by_size_with_picker(e):
        if is_working:
            log("Операция уже выполняется, подождите...")
            return
        pick_folder_for_fla("Выберите папку для поиска .fla по размеру", open_fla_by_size_in_folder)
    
    def run_all_fla_with_picker(e):
        if is_working:
            log("Операция уже выполняется, подождите...")
            return
        pick_folder_for_fla("Выберите папку для поиска всех .fla", open_all_fla_in_folder)
    
    def perform_rename(e):
        if not selected_path:
            log("Сначала выберите папку!")
            return
        
        find_text = rename_find.value.strip()
        replace_text = rename_replace.value.strip()
        
        if not find_text:
            log("Введите текст для поиска!")
            return
        
        log(f"\n{'='*50}")
        log(f"ПАКЕТНОЕ ПЕРЕИМЕНОВАНИЕ")
        log(f"Папка: {selected_path}")
        log(f"Поиск: '{find_text}' → Замена: '{replace_text}'")
        log(f"{'='*50}")
        
        renamed_count = 0
        errors = 0
        
        try:
            items = os.listdir(selected_path)
            log(f"Найдено объектов: {len(items)}")
            
            for name in items:
                if name == 'zip':
                    continue
                
                if find_text in name:
                    old_path = os.path.join(selected_path, name)
                    new_name = name.replace(find_text, replace_text)
                    new_path = os.path.join(selected_path, new_name)
                    
                    log(f"\n{name} → {new_name}")
                    
                    if os.path.exists(new_path) and old_path != new_path:
                        log(f"  ⚠️ Пропущен: {new_name} уже существует")
                        errors += 1
                        continue
                    
                    try:
                        os.rename(old_path, new_path)
                        renamed_count += 1
                        log(f"  ✅ УСПЕШНО!")
                    except Exception as e:
                        log(f"  ❌ Ошибка: {str(e)}")
                        errors += 1
            
            log(f"\n{'='*50}")
            log(f"ПЕРЕИМЕНОВАНИЕ ЗАВЕРШЕНО!")
            log(f"Успешно: {renamed_count}, Ошибок: {errors}")
            log(f"{'='*50}\n")
            
        except Exception as e:
            log(f"Критическая ошибка: {str(e)}")
    
    # === ИНТЕРФЕЙС ===
    def make_button(text, on_click, bgcolor=None, expand=False, height=40):
        return ft.Container(
            content=ft.Text(text, size=13, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
            bgcolor=bgcolor if bgcolor else BG_CARD,
            border_radius=6,
            padding=12,
            ink=True,
            on_click=on_click,
            expand=expand,
            height=height,
        )
    
    def make_outlined_button(text, on_click, bgcolor=None, color=PRIMARY, expand=False, height=40):
        return ft.Container(
            content=ft.Text(text, size=13, color=color, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
            bgcolor=bgcolor if bgcolor else BG_CARD,
            border_radius=6,
            border=ft.border.all(1, "#4a4a4a"),
            padding=12,
            ink=True,
            on_click=on_click,
            expand=expand,
            height=height,
        )
    
    left_panel = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Рабочая папка", size=12, color=TEXT_SECONDARY),
                    ft.Row([
                        ft.Container(content=folder_text, expand=True, height=35),
                        make_button("Выбрать", pick_folder, PRIMARY, expand=False, height=35),
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ], spacing=8),
                padding=12,
                bgcolor=BG_CARD,
                border_radius=8,
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Архиватор", size=12, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                    ft.Row([
                        ft.Text("Целевой размер:", size=12, color=TEXT_SECONDARY),
                        target_archive_size,
                        ft.Text("KB", size=12, color=TEXT_SECONDARY),
                    ], spacing=8, alignment=ft.MainAxisAlignment.START),
                    make_button("ОПТИМИЗИРОВАТЬ ВСЕ ПОД РАЗМЕР", optimize_all_with_target_size, SUCCESS, True, 45),
                    make_button("АРХИВИРОВАТЬ ВСЕ", archive_all_folders, PRIMARY, True, 45),
                    make_button("УДАЛИТЬ ВСЕ АРХИВЫ", delete_all_zips, ERROR, True, 40),
                    ft.Text("💡 Лимит ≥250KB → lossless (Oxipng), <250KB → lossy (pngquant)", size=10, color=TEXT_SECONDARY),
                ], spacing=10),
                padding=12,
                bgcolor=BG_CARD,
                border_radius=8,
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text(".fla операции", size=12, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                    ft.Row([
                        ft.Text("Размер:", size=13, color=TEXT_SECONDARY),
                        size_input,
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    make_outlined_button("Открыть .fla по размеру", run_fla_by_size_with_picker, BG_CARD, PRIMARY, True, 40),
                    make_outlined_button("Открыть все .fla", run_all_fla_with_picker, BG_CARD, SUCCESS, True, 40),
                ], spacing=10),
                padding=12,
                bgcolor=BG_CARD,
                border_radius=8,
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Пакетное переименование", size=12, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                    ft.Row([
                        rename_find,
                        ft.Text("→", size=14, color=TEXT_SECONDARY),
                        rename_replace,
                    ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    make_button("ЗАМЕНИТЬ ВСЁ", perform_rename, SUCCESS, True, 40),
                ], spacing=10),
                padding=12,
                bgcolor=BG_CARD,
                border_radius=8,
            ),
        ], spacing=12),
        width=480,
    )
    
    right_panel = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Лог операций", size=12, color=TEXT_SECONDARY),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.CLEAR_ALL, on_click=clear_output, tooltip="Очистить лог", icon_color=TEXT_SECONDARY, icon_size=18),
            ], spacing=10),
            ft.Container(content=output_text, expand=True, height=600),
        ], spacing=5, expand=True),
        expand=True,
        padding=12,
        bgcolor=BG_CARD,
        border_radius=8,
    )
    
    main_container = ft.Row([left_panel, ft.Container(width=15), right_panel], spacing=0, expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
    page.add(main_container)
    
    log("🚀 QuickTools запущена!")
    log("💡 Выберите рабочую папку")
    log("📦 Схема работы:")
    log("   1. Задайте целевой размер архива в KB")
    log("   2. Нажмите 'ОПТИМИЗИРОВАТЬ ВСЕ ПОД РАЗМЕР' — подбор параметров и сжатие")
    log("   3. Нажмите 'АРХИВИРОВАТЬ ВСЕ' — создание архивов")
    log("   .fla файлы игнорируются при архивации")
    if OXIPNG_PATH:
        log(f"✅ Oxipng найден (lossless сжатие для PNG при лимитах ≥250KB)")
    else:
        log(f"⚠️ Oxipng не найден. Положите oxipng.exe в папку с программой для lossless сжатия PNG")

if __name__ == "__main__":
    ft.app(target=main)