import flet as ft
import asyncio
import os
from modules.config import COLORS
from modules import image_optimizer, archive_handler, folder_scanner, settings_finder
from ui.components import make_button
from ui.progress_ui import update_progress, hide_progress

def archiver_block(log_func, selected_path_ref, is_working_ref, page):
    """Создаёт блок 'Архиватор'"""
    
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
    
    # Ссылки на прогресс-бар (будут установлены из main_view)
    progress_bar_ref = [None]
    progress_text_ref = [None]
    
    def set_progress_refs(bar, text):
        progress_bar_ref[0] = bar
        progress_text_ref[0] = text
    
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
                
                if progress_bar_ref[0] and progress_text_ref[0]:
                    update_progress(progress_bar_ref[0], progress_text_ref[0], 0, f"Обработка папки 0/{total_folders}", page)
                
                for idx, folder_info in enumerate(size_folders):
                    folder_path = folder_info['path']
                    folder_name = f"{folder_info['platform']}/{folder_info['campaign']}/{folder_info['size']}"
                    
                    progress_value = idx / total_folders
                    if progress_bar_ref[0] and progress_text_ref[0]:
                        update_progress(
                            progress_bar_ref[0], progress_text_ref[0],
                            progress_value, 
                            f"🔍 Анализ: {folder_info['size']} ({idx+1}/{total_folders})",
                            page
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
                        
                        file_progress = (idx + file_idx / len(files_to_process)) / total_folders
                        if progress_bar_ref[0] and progress_text_ref[0]:
                            update_progress(
                                progress_bar_ref[0], progress_text_ref[0],
                                file_progress,
                                f"📦 {folder_info['size']}: {file} ({file_idx+1}/{len(files_to_process)})",
                                page
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
                    
                    await asyncio.sleep(0.05)
                
                if progress_bar_ref[0] and progress_text_ref[0]:
                    update_progress(progress_bar_ref[0], progress_text_ref[0], 1.0, "✅ Оптимизация завершена!", page)
                    await asyncio.sleep(0.5)
                    hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
                
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
                if progress_bar_ref[0] and progress_text_ref[0]:
                    hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
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
                
                if progress_bar_ref[0] and progress_text_ref[0]:
                    update_progress(progress_bar_ref[0], progress_text_ref[0], 0, f"Архивация: 0/{total}", page)
                
                archive_count = 0
                total_before = 0
                total_after = 0
                
                for idx, folder_info in enumerate(size_folders):
                    folder_path = folder_info['path']
                    platform = folder_info['platform']
                    campaign = folder_info['campaign']
                    size_name = folder_info['size']
                    
                    progress_value = idx / total
                    if progress_bar_ref[0] and progress_text_ref[0]:
                        update_progress(
                            progress_bar_ref[0], progress_text_ref[0],
                            progress_value,
                            f"📦 Архивация: {platform}/{campaign}/{size_name} ({idx+1}/{total})",
                            page
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
                
                if progress_bar_ref[0] and progress_text_ref[0]:
                    update_progress(progress_bar_ref[0], progress_text_ref[0], 1.0, "✅ Архивация завершена!", page)
                    await asyncio.sleep(0.5)
                    hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
                
                log_func(f"\n{'='*60}")
                log_func(f"✅ АРХИВАЦИЯ ЗАВЕРШЕНА!")
                log_func(f"Создано архивов: {archive_count} из {total}")
                if archive_count > 0:
                    log_func(f"Общий размер: {total_before//1024}KB → {total_after//1024}KB")
                    log_func(f"Общее сжатие: {(1 - total_after/total_before)*100:.0f}%")
                log_func(f"{'='*60}\n")
                
            except Exception as e:
                log_func(f"❌ Ошибка: {str(e)}")
                if progress_bar_ref[0] and progress_text_ref[0]:
                    hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
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
        
        if progress_bar_ref[0] and progress_text_ref[0]:
            update_progress(progress_bar_ref[0], progress_text_ref[0], 0, "Поиск архивов...", page)
        
        async def delete_task():
            try:
                deleted_zips, deleted_folders = archive_handler.delete_all_archives(selected_path_ref[0], log_func)
                
                if progress_bar_ref[0] and progress_text_ref[0]:
                    update_progress(progress_bar_ref[0], progress_text_ref[0], 1.0, "✅ Удаление завершено!", page)
                    await asyncio.sleep(0.5)
                    hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
                
                log_func(f"\n✅ УДАЛЕНИЕ ЗАВЕРШЕНО!")
                log_func(f"Удалено ZIP: {deleted_zips}, папок zip: {deleted_folders}")
            except Exception as e:
                log_func(f"❌ Ошибка: {str(e)}")
                if progress_bar_ref[0] and progress_text_ref[0]:
                    hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
            finally:
                is_working_ref[0] = False
        
        asyncio.create_task(delete_task())
    
    container = ft.Container(
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
    )
    
    # Возвращаем контейнер и функцию для установки ссылок на прогресс-бар
    return container, set_progress_refs