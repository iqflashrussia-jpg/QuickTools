import flet as ft
import tkinter as tk
from tkinter import filedialog
import time
import asyncio
import os

from modules.config import COLORS
from modules import image_optimizer, archive_handler, folder_scanner, settings_finder, fla_operations, rename_utils
from ui.components import make_button, make_outlined_button

def create_main_view(page: ft.Page, selected_path_ref, is_working_ref, log_func):
    """Создаёт основной интерфейс"""
    
    folder_text = ft.Text(value="Папка не выбрана", size=14, color=COLORS["TEXT_SECONDARY"])
    
    # Прогресс-бар
    progress_bar = ft.ProgressBar(
        width=None,
        height=6,
        color=COLORS["SUCCESS"],
        bgcolor="#3d3d3d",
        value=0,
        visible=False,
    )
    progress_text = ft.Text(
        value="",
        size=11,
        color=COLORS["TEXT_SECONDARY"],
        visible=False,
    )
    
    output_text = ft.TextField(
        multiline=True,
        min_lines=30,
        max_lines=35,
        read_only=True,
        value="Готов к работе...\n",
        text_size=11,
        bgcolor=COLORS["BG_INPUT"],
        border_color="#3d3d3d",
        color=COLORS["TEXT"],
    )
    
    target_archive_size = ft.TextField(
        value="300",
        hint_text="целевой размер в KB",
        width=120,
        height=40,
        text_size=13,
        text_align=ft.TextAlign.CENTER,
        bgcolor=COLORS["BG_INPUT"],
        border_color="#3d3d3d",
        color=COLORS["TEXT"],
    )
    
    rename_find = ft.TextField(
        hint_text="исходный текст",
        expand=True,
        height=40,
        text_size=13,
        bgcolor=COLORS["BG_INPUT"],
        border_color="#3d3d3d",
        color=COLORS["TEXT"],
    )
    rename_replace = ft.TextField(
        hint_text="финальный текст",
        expand=True,
        height=40,
        text_size=13,
        bgcolor=COLORS["BG_INPUT"],
        border_color="#3d3d3d",
        color=COLORS["TEXT"],
    )
    
    size_input = ft.TextField(
        hint_text="240x400",
        width=180,
        height=40,
        text_size=13,
        text_align=ft.TextAlign.CENTER,
        bgcolor=COLORS["BG_INPUT"],
        border_color="#3d3d3d",
        color=COLORS["TEXT"],
    )
    
    def update_progress(progress, status, visible=True):
        """Обновляет прогресс-бар и текст"""
        progress_bar.value = progress
        progress_text.value = status
        progress_bar.visible = visible
        progress_text.visible = visible
        page.update()
    
    def hide_progress():
        """Скрывает прогресс-бар"""
        progress_bar.visible = False
        progress_text.visible = False
        page.update()
    
    def pick_folder(e):
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_selected = filedialog.askdirectory(title="Выберите рабочую папку")
        root.destroy()
        if folder_selected:
            selected_path_ref[0] = folder_selected
            folder_text.value = os.path.basename(selected_path_ref[0])
            folder_text.color = COLORS["PRIMARY"]
            folder_text.tooltip = selected_path_ref[0]
            log_func(f"Выбрана папка: {selected_path_ref[0]}")
        else:
            log_func("Выбор папки отменён")
    
    def optimize_all(e):
        if not selected_path_ref[0]:
            log_func("Сначала выберите папку!")
            return
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        
        try:
            target_kb = int(target_archive_size.value)
            if target_kb < 50:
                target_kb = 50
                target_archive_size.value = "50"
        except:
            target_kb = 300
            target_archive_size.value = "300"
        
        is_working_ref[0] = True
        
        async def optimize_task():
            try:
                log_func(f"\n{'='*60}")
                log_func(f"🎯 ОПТИМИЗАЦИЯ ВСЕХ ПАПОК ПОД РАЗМЕР")
                log_func(f"Папка: {selected_path_ref[0]}")
                log_func(f"Целевой размер архива: {target_kb} KB")
                if image_optimizer.check_oxipng():
                    log_func(f"✅ Oxipng найден (lossless для лимитов ≥250KB)")
                log_func(f"{'='*60}")
                
                size_folders = folder_scanner.find_size_folders(selected_path_ref[0])
                if not size_folders:
                    log_func("Папки с 'x' в имени не найдены")
                    is_working_ref[0] = False
                    return
                
                total_folders = len(size_folders)
                log_func(f"Найдено папок: {total_folders}")
                page.update()
                
                total_before = 0
                total_after = 0
                processed = 0
                skipped = 0
                
                # Показываем прогресс-бар
                update_progress(0, f"Обработка папки 0/{total_folders}")
                
                for idx, folder_info in enumerate(size_folders):
                    folder_path = folder_info['path']
                    folder_name = f"{folder_info['platform']}/{folder_info['campaign']}/{folder_info['size']}"
                    
                    # Обновляем прогресс
                    progress_value = idx / total_folders
                    update_progress(
                        progress_value, 
                        f"🔍 Анализ: {folder_info['size']} ({idx+1}/{total_folders})"
                    )
                    log_func(f"\n[{idx+1}/{total_folders}] {folder_name}")
                    
                    result = settings_finder.find_best_settings(folder_path, target_kb, log_func)
                    
                    if result[0] is None:
                        log_func(f"  {result[4]}")
                        skipped += 1
                        continue
                    
                    method, jpg_q, png_param, archive_size, msg = result
                    log_func(f"  {msg}")
                    log_func(f"  🔄 Применяем сжатие...")
                    
                    # Обновляем прогресс для сжатия файлов в папке
                    files_to_process = []
                    for file in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file)
                        if os.path.isfile(file_path) and not file.endswith('.fla'):
                            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                                files_to_process.append(file)
                    
                    folder_before = 0
                    folder_after = 0
                    
                    for file_idx, file in enumerate(files_to_process):
                        file_path = os.path.join(folder_path, file)
                        old_size = os.path.getsize(file_path)
                        
                        # Обновляем прогресс для текущего файла
                        file_progress = (idx + file_idx / len(files_to_process)) / total_folders
                        update_progress(
                            file_progress,
                            f"📦 {folder_info['size']}: {file} ({file_idx+1}/{len(files_to_process)})"
                        )
                        
                        if file.lower().endswith(('.jpg', '.jpeg')):
                            folder_before += old_size
                            reduction = image_optimizer.optimize_jpeg(file_path, jpg_q)
                            new_size = os.path.getsize(file_path)
                            folder_after += new_size
                            if reduction > 0:
                                log_func(f"    ✅ {file}: {old_size//1024}KB → {new_size//1024}KB (-{reduction:.0f}%)")
                            else:
                                log_func(f"    ✓ {file}: {old_size//1024}KB")
                        
                        elif file.lower().endswith('.png'):
                            folder_before += old_size
                            if method == 'lossless':
                                success, reduction = image_optimizer.optimize_png_oxipng(file_path, png_param)
                            else:
                                success, reduction = image_optimizer.optimize_png_lossy(file_path, png_param)
                            new_size = os.path.getsize(file_path)
                            folder_after += new_size
                            if success and reduction > 0:
                                log_func(f"    ✅ {file}: {old_size//1024}KB → {new_size//1024}KB (-{reduction:.0f}%)")
                            else:
                                log_func(f"    ✓ {file}: {old_size//1024}KB")
                    
                    folder_reduction = (1 - folder_after/folder_before) * 100 if folder_before > 0 else 0
                    total_before += folder_before
                    total_after += folder_after
                    processed += 1
                    log_func(f"  📊 Итого папки: {folder_before//1024}KB → {folder_after//1024}KB (сжатие {folder_reduction:.0f}%)")
                    
                    # Небольшая задержка для плавности анимации
                    await asyncio.sleep(0.05)
                
                # Завершаем прогресс
                update_progress(1.0, "✅ Оптимизация завершена!")
                await asyncio.sleep(0.5)
                hide_progress()
                
                log_func(f"\n{'='*60}")
                log_func(f"✅ ОПТИМИЗАЦИЯ ЗАВЕРШЕНА!")
                log_func(f"Обработано папок: {processed}")
                log_func(f"Пропущено: {skipped}")
                if total_before > 0:
                    total_reduction = (1 - total_after/total_before) * 100
                    log_func(f"Общий размер: {total_before//1024}KB → {total_after//1024}KB")
                    log_func(f"Общее сжатие: {total_reduction:.0f}%")
                log_func(f"🎯 Теперь можно запустить архивацию!")
                log_func(f"{'='*60}\n")
                
            except Exception as e:
                log_func(f"❌ Критическая ошибка: {str(e)}")
                import traceback
                traceback.print_exc()
                hide_progress()
            finally:
                is_working_ref[0] = False
        
        asyncio.create_task(optimize_task())
    
    def archive_all(e):
        if not selected_path_ref[0]:
            log_func("Сначала выберите папку!")
            return
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        
        is_working_ref[0] = True
        
        async def archive_task():
            try:
                log_func("\n📦 АРХИВАЦИЯ ВСЕХ ПАПОК")
                
                size_folders = folder_scanner.find_size_folders(selected_path_ref[0])
                if not size_folders:
                    log_func("Папки с 'x' в имени не найдены")
                    is_working_ref[0] = False
                    return
                
                total = len(size_folders)
                log_func(f"Найдено папок: {total}")
                page.update()
                
                # Показываем прогресс-бар
                update_progress(0, f"Архивация: 0/{total}")
                
                archive_count = 0
                total_before = 0
                total_after = 0
                
                for idx, folder_info in enumerate(size_folders):
                    folder_path = folder_info['path']
                    platform = folder_info['platform']
                    campaign = folder_info['campaign']
                    size_name = folder_info['size']
                    
                    # Обновляем прогресс
                    progress_value = idx / total
                    update_progress(
                        progress_value,
                        f"📦 Архивация: {platform}/{campaign}/{size_name} ({idx+1}/{total})"
                    )
                    
                    log_func(f"\n📦 {idx+1}/{total}: {platform}/{campaign}/{size_name}")
                    
                    files_to_zip = []
                    folder_size = 0
                    
                    for file in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file)
                        if os.path.isfile(file_path) and not file.endswith('.fla'):
                            files_to_zip.append(file_path)
                            folder_size += os.path.getsize(file_path)
                    
                    log_func(f"  Файлов: {len(files_to_zip)} (без .fla)")
                    log_func(f"  Размер: {folder_size // 1024} KB")
                    
                    if files_to_zip:
                        zip_name = f"{size_name}_{campaign}_{platform}.zip"
                        zip_output_dir = os.path.join(os.path.dirname(folder_path), "zip")
                        zip_path = os.path.join(zip_output_dir, zip_name)
                        
                        archive_size = archive_handler.create_archive(folder_path, zip_path)
                        
                        if archive_size:
                            total_before += folder_size
                            total_after += archive_size
                            reduction = (1 - archive_size/folder_size) * 100 if folder_size > 0 else 0
                            log_func(f"  ✅ Создан: {zip_name}")
                            log_func(f"     Размер: {archive_size // 1024} KB (сжатие {reduction:.0f}%)")
                            archive_count += 1
                        else:
                            log_func(f"  ❌ Ошибка создания архива")
                    else:
                        log_func(f"  ⚠️ Нет файлов для архивации")
                    
                    await asyncio.sleep(0.05)
                
                # Завершаем прогресс
                update_progress(1.0, "✅ Архивация завершена!")
                await asyncio.sleep(0.5)
                hide_progress()
                
                log_func(f"\n{'='*60}")
                log_func(f"✅ АРХИВАЦИЯ ЗАВЕРШЕНА!")
                log_func(f"Создано архивов: {archive_count} из {total}")
                if archive_count > 0:
                    log_func(f"Общий размер: {total_before//1024}KB → {total_after//1024}KB")
                    log_func(f"Общее сжатие: {(1 - total_after/total_before)*100:.0f}%")
                log_func(f"{'='*60}\n")
                
            except Exception as e:
                log_func(f"❌ Ошибка: {str(e)}")
                hide_progress()
            finally:
                is_working_ref[0] = False
        
        asyncio.create_task(archive_task())
    
    def delete_zips(e):
        if not selected_path_ref[0]:
            log_func("Сначала выберите папку!")
            return
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        
        is_working_ref[0] = True
        log_func("\n🗑️ УДАЛЕНИЕ ВСЕХ ZIP ФАЙЛОВ И ПАПОК")
        page.update()
        
        # Показываем прогресс-бар для удаления
        update_progress(0, "Поиск архивов...")
        
        async def delete_task():
            try:
                deleted_zips, deleted_folders = archive_handler.delete_all_archives(selected_path_ref[0], log_func)
                
                update_progress(1.0, "✅ Удаление завершено!")
                await asyncio.sleep(0.5)
                hide_progress()
                
                log_func(f"\n✅ УДАЛЕНИЕ ЗАВЕРШЕНО!")
                log_func(f"Удалено ZIP: {deleted_zips}, папок zip: {deleted_folders}")
            except Exception as e:
                log_func(f"❌ Ошибка: {str(e)}")
                hide_progress()
            finally:
                is_working_ref[0] = False
        
        asyncio.create_task(delete_task())
    
    def pick_folder_for_fla(title, callback):
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        initial_dir = selected_path_ref[0] if selected_path_ref[0] else os.path.expanduser("~")
        folder_selected = filedialog.askdirectory(title=title, initialdir=initial_dir)
        root.destroy()
        if folder_selected:
            callback(folder_selected)
        else:
            log_func("Выбор папки отменён")
    
    def open_fla_by_size(folder_path):
        size = size_input.value.strip()
        if not size:
            log_func("Введите размер файла!")
            return
        
        log_func(f"\n🔍 ПОИСК {size}.fla в папке: {folder_path}")
        
        async def search_task():
            nonlocal is_working_ref
            is_working_ref[0] = True
            start_time = time.time()
            
            # Показываем прогресс для поиска
            update_progress(0, f"Поиск {size}.fla...")
            
            try:
                found_files = []
                total_found = 0
                for result in fla_operations.find_fla_files(folder_path, size):
                    if isinstance(result, list):
                        found_files = result
                        total_found = len(found_files)
                        break
                    await asyncio.sleep(0.01)
                
                if total_found == 0:
                    log_func(f"Файл {size}.fla не найден")
                    hide_progress()
                else:
                    log_func(f"Найдено файлов: {total_found}")
                    page.update()
                    
                    update_progress(0.2, f"Открытие {total_found} файлов...")
                    
                    for idx, file_path in enumerate(found_files):
                        progress_val = 0.2 + (idx / total_found) * 0.8
                        update_progress(
                            progress_val,
                            f"Открытие: {os.path.basename(file_path)} ({idx+1}/{total_found})"
                        )
                        try:
                            os.startfile(file_path)
                            log_func(f"  ✅ Открыт: {os.path.basename(file_path)}")
                        except Exception as e:
                            log_func(f"  ❌ Ошибка: {os.path.basename(file_path)}")
                        await asyncio.sleep(0.1)
                    
                    update_progress(1.0, "✅ Готово!")
                    await asyncio.sleep(0.5)
                    hide_progress()
                    
                    elapsed = time.time() - start_time
                    log_func(f"\n✅ Открыто файлов: {total_found} за {elapsed:.1f} сек")
            except Exception as e:
                log_func(f"❌ Ошибка: {str(e)}")
                hide_progress()
            finally:
                is_working_ref[0] = False
        
        asyncio.create_task(search_task())
    
    def open_all_fla(folder_path):
        log_func(f"\n🔍 ПОИСК ВСЕХ .fla в папке: {folder_path}")
        
        async def search_task():
            nonlocal is_working_ref
            is_working_ref[0] = True
            start_time = time.time()
            
            update_progress(0, "Поиск всех .fla файлов...")
            
            try:
                found_files = []
                total_found = 0
                for result in fla_operations.find_fla_files(folder_path):
                    if isinstance(result, list):
                        found_files = result
                        total_found = len(found_files)
                        break
                    await asyncio.sleep(0.01)
                
                if total_found == 0:
                    log_func(".fla файлы не найдены")
                    hide_progress()
                else:
                    log_func(f"Найдено .fla файлов: {total_found}")
                    page.update()
                    
                    update_progress(0.2, f"Открытие {total_found} файлов...")
                    
                    for idx, file_path in enumerate(found_files):
                        progress_val = 0.2 + (idx / total_found) * 0.8
                        update_progress(
                            progress_val,
                            f"Открытие: {os.path.basename(file_path)} ({idx+1}/{total_found})"
                        )
                        try:
                            os.startfile(file_path)
                            if (idx + 1) % 10 == 0:
                                log_func(f"  Открыто {idx+1}/{total_found} файлов")
                        except Exception as e:
                            log_func(f"  ❌ Ошибка: {os.path.basename(file_path)}")
                        await asyncio.sleep(0.05)
                    
                    update_progress(1.0, "✅ Готово!")
                    await asyncio.sleep(0.5)
                    hide_progress()
                    
                    elapsed = time.time() - start_time
                    log_func(f"\n✅ Открыто всех .fla файлов: {total_found} за {elapsed:.1f} сек")
            except Exception as e:
                log_func(f"❌ Ошибка: {str(e)}")
                hide_progress()
            finally:
                is_working_ref[0] = False
        
        asyncio.create_task(search_task())
    
    def run_fla_by_size(e):
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        pick_folder_for_fla("Выберите папку для поиска .fla по размеру", open_fla_by_size)
    
    def run_all_fla(e):
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        pick_folder_for_fla("Выберите папку для поиска всех .fla", open_all_fla)
    
    def perform_rename(e):
        if not selected_path_ref[0]:
            log_func("Сначала выберите папку!")
            return
        
        find_text = rename_find.value.strip()
        replace_text = rename_replace.value.strip()
        
        if not find_text:
            log_func("Введите текст для поиска!")
            return
        
        log_func(f"\n{'='*50}")
        log_func(f"ПАКЕТНОЕ ПЕРЕИМЕНОВАНИЕ")
        log_func(f"Папка: {selected_path_ref[0]}")
        log_func(f"Поиск: '{find_text}' → Замена: '{replace_text}'")
        log_func(f"{'='*50}")
        
        is_working_ref[0] = True
        
        # Показываем прогресс
        update_progress(0, "Поиск файлов для переименования...")
        
        async def rename_task():
            try:
                items = os.listdir(selected_path_ref[0])
                items_to_rename = [name for name in items if name != 'zip' and find_text in name]
                total = len(items_to_rename)
                
                if total == 0:
                    log_func("Нет файлов для переименования")
                    hide_progress()
                    is_working_ref[0] = False
                    return
                
                renamed_count = 0
                errors = 0
                
                for idx, name in enumerate(items_to_rename):
                    progress_val = idx / total
                    update_progress(
                        progress_val,
                        f"Переименование: {name} → {name.replace(find_text, replace_text)}"
                    )
                    
                    old_path = os.path.join(selected_path_ref[0], name)
                    new_name = name.replace(find_text, replace_text)
                    new_path = os.path.join(selected_path_ref[0], new_name)
                    
                    if os.path.exists(new_path) and old_path != new_path:
                        log_func(f"  ⚠️ Пропущен: {new_name} уже существует")
                        errors += 1
                        continue
                    
                    try:
                        os.rename(old_path, new_path)
                        renamed_count += 1
                        log_func(f"  ✅ {name} → {new_name}")
                    except Exception as e:
                        log_func(f"  ❌ Ошибка: {name} → {str(e)}")
                        errors += 1
                    
                    await asyncio.sleep(0.01)
                
                update_progress(1.0, "✅ Переименование завершено!")
                await asyncio.sleep(0.5)
                hide_progress()
                
                log_func(f"\n{'='*50}")
                log_func(f"ПЕРЕИМЕНОВАНИЕ ЗАВЕРШЕНО!")
                log_func(f"Успешно: {renamed_count}, Ошибок: {errors}")
                log_func(f"{'='*50}\n")
                
            except Exception as e:
                log_func(f"Ошибка: {str(e)}")
                hide_progress()
            finally:
                is_working_ref[0] = False
        
        asyncio.create_task(rename_task())
    
    def clear_output(e):
        output_text.value = "Лог очищен\n"
        page.update()
    
    # Левый сайдбар
    left_panel = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Рабочая папка", size=12, color=COLORS["TEXT_SECONDARY"]),
                    ft.Row([
                        ft.Container(content=folder_text, expand=True, height=35),
                        make_button("Выбрать", pick_folder, COLORS["PRIMARY"], expand=False, height=35),
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ], spacing=8),
                padding=12,
                bgcolor=COLORS["BG_CARD"],
                border_radius=8,
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Архиватор", size=12, weight=ft.FontWeight.BOLD, color=COLORS["TEXT"]),
                    ft.Row([
                        ft.Text("Целевой размер:", size=12, color=COLORS["TEXT_SECONDARY"]),
                        target_archive_size,
                        ft.Text("KB", size=12, color=COLORS["TEXT_SECONDARY"]),
                    ], spacing=8, alignment=ft.MainAxisAlignment.START),
                    make_button("ОПТИМИЗИРОВАТЬ ВСЕ ПОД РАЗМЕР", optimize_all, COLORS["SUCCESS"], True, 45),
                    make_button("АРХИВИРОВАТЬ ВСЕ", archive_all, COLORS["PRIMARY"], True, 45),
                    make_button("УДАЛИТЬ ВСЕ АРХИВЫ", delete_zips, COLORS["ERROR"], True, 40),
                    ft.Text("💡 Лимит ≥250KB → lossless (Oxipng), <250KB → lossy (pngquant)", size=10, color=COLORS["TEXT_SECONDARY"]),
                ], spacing=10),
                padding=12,
                bgcolor=COLORS["BG_CARD"],
                border_radius=8,
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text(".fla операции", size=12, weight=ft.FontWeight.BOLD, color=COLORS["TEXT"]),
                    ft.Row([
                        ft.Text("Размер:", size=13, color=COLORS["TEXT_SECONDARY"]),
                        size_input,
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    make_outlined_button("Открыть .fla по размеру", run_fla_by_size, COLORS["BG_CARD"], COLORS["PRIMARY"], True, 40),
                    make_outlined_button("Открыть все .fla", run_all_fla, COLORS["BG_CARD"], COLORS["SUCCESS"], True, 40),
                ], spacing=10),
                padding=12,
                bgcolor=COLORS["BG_CARD"],
                border_radius=8,
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Пакетное переименование", size=12, weight=ft.FontWeight.BOLD, color=COLORS["TEXT"]),
                    ft.Row([
                        rename_find,
                        ft.Text("→", size=14, color=COLORS["TEXT_SECONDARY"]),
                        rename_replace,
                    ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    make_button("ЗАМЕНИТЬ ВСЁ", perform_rename, COLORS["SUCCESS"], True, 40),
                ], spacing=10),
                padding=12,
                bgcolor=COLORS["BG_CARD"],
                border_radius=8,
            ),
        ], spacing=12),
        width=480,
    )
    
    # Правая панель - лог с прогресс-баром
    right_panel = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Лог операций", size=12, color=COLORS["TEXT_SECONDARY"]),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.CLEAR_ALL, on_click=clear_output, tooltip="Очистить лог", icon_color=COLORS["TEXT_SECONDARY"], icon_size=18),
            ], spacing=10),
            # Прогресс-бар над логом
            ft.Column([
                progress_bar,
                progress_text,
            ], spacing=5),
            ft.Container(content=output_text, expand=True, height=550),
        ], spacing=5, expand=True),
        expand=True,
        padding=12,
        bgcolor=COLORS["BG_CARD"],
        border_radius=8,
    )
    
    main_container = ft.Row([left_panel, ft.Container(width=15), right_panel], spacing=0, expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
    page.add(main_container)
    
    return output_text