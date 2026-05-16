"""
Блок "Оптимизация" - подбор качества сжатия изображений под целевой размер архива.
"""

import flet as ft
import os
import asyncio

from ui.styles import AppColors, AppSizes
from ui.components import make_button, make_text_field
from modules import settings_finder, image_optimizer


def optimizer_block(log_func, selected_path_ref, is_working_ref, page, progress_widget=None):
    """
    Создаёт блок "Оптимизация".
    """
    
    # Поле для целевого размера
    target_size_field = make_text_field(
        value="300",
        hint_text="Целевой размер",
        width=AppSizes.INPUT_WIDTH_SMALL,
    )
    
    # Статусная строка
    status_text = ft.Text(
        value="Готов к оптимизации",
        size=AppSizes.FONT_SIZE_SMALL,
        color=AppColors.TEXT_SECONDARY,
    )
    
    def find_size_folders(base_path):
        """Находит все папки с 'x' в имени (размеры) внутри папки animate"""
        folders = []
        if not os.path.exists(base_path):
            return folders
        
        # Ищем только внутри папки animate
        animate_path = os.path.join(base_path, "animate")
        if not os.path.exists(animate_path):
            return folders
        
        for platform in os.listdir(animate_path):
            platform_path = os.path.join(animate_path, platform)
            if not os.path.isdir(platform_path):
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
    
    def optimize_all_folders(e):
        """Оптимизирует все папки с размерами под целевой размер"""
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        
        if not selected_path_ref[0]:
            log_func("Сначала выберите рабочую папку!")
            return
        
        try:
            target_kb = int(target_size_field.value.strip())
            if target_kb < 50:
                target_kb = 50
                target_size_field.value = "50"
        except:
            target_kb = 300
            target_size_field.value = "300"
        
        is_working_ref[0] = True
        
        async def optimize_task():
            try:
                log_func(f"\n{'='*60}")
                log_func(f"🎯 ОПТИМИЗАЦИЯ ПОД РАЗМЕР {target_kb} KB")
                log_func(f"📁 Папка: {selected_path_ref[0]}")
                if image_optimizer.check_oxipng():
                    log_func(f"✅ Oxipng найден (lossless для лимитов ≥250 KB)")
                log_func(f"{'='*60}")
                
                # Поиск папок с размерами
                size_folders = find_size_folders(selected_path_ref[0])
                
                if not size_folders:
                    log_func("❌ Папки с 'x' в имени не найдены")
                    is_working_ref[0] = False
                    return
                
                total = len(size_folders)
                log_func(f"📁 Найдено папок: {total}")
                page.update()
                
                if progress_widget:
                    progress_widget.update_progress(0, f"Оптимизация: 0/{total}", page)
                
                total_before = 0
                total_after = 0
                processed = 0
                skipped = 0
                
                for idx, folder_info in enumerate(size_folders):
                    folder_path = folder_info['path']
                    folder_name = f"{folder_info['platform']}/{folder_info['campaign']}/{folder_info['size']}"
                    
                    progress_value = idx / total
                    if progress_widget:
                        progress_widget.update_progress(
                            progress_value,
                            f"🔍 Анализ: {folder_info['size']} ({idx+1}/{total})",
                            page
                        )
                    
                    log_func(f"\n[{idx+1}/{total}] {folder_name}")
                    
                    # Подбираем настройки для папки
                    result = settings_finder.find_best_settings(folder_path, target_kb, log_func)
                    
                    if result[0] is None:
                        log_func(f"  {result[4]}")
                        skipped += 1
                        continue
                    
                    method, jpg_q, png_param, archive_size, msg = result
                    log_func(f"  {msg}")
                    log_func(f"  🔄 Применяем сжатие...")
                    
                    # Собираем файлы для оптимизации
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
                        folder_before += old_size
                        
                        file_progress = (idx + file_idx / len(files_to_process)) / total
                        if progress_widget:
                            progress_widget.update_progress(
                                file_progress,
                                f"📦 {folder_info['size']}: {file} ({file_idx+1}/{len(files_to_process)})",
                                page
                            )
                        
                        if file.lower().endswith(('.jpg', '.jpeg')):
                            reduction = image_optimizer.optimize_jpeg(file_path, jpg_q)
                            new_size = os.path.getsize(file_path)
                            folder_after += new_size
                            if reduction > 0:
                                log_func(f"    ✅ {file}: {old_size//1024} KB → {new_size//1024} KB (-{reduction:.0f}%)")
                            else:
                                log_func(f"    ✓ {file}: {old_size//1024} KB")
                        
                        elif file.lower().endswith('.png'):
                            if method == 'lossless':
                                success, reduction = image_optimizer.optimize_png_oxipng(file_path, png_param)
                            else:
                                success, reduction = image_optimizer.optimize_png_lossy(file_path, png_param)
                            new_size = os.path.getsize(file_path)
                            folder_after += new_size
                            if success and reduction > 0:
                                log_func(f"    ✅ {file}: {old_size//1024} KB → {new_size//1024} KB (-{reduction:.0f}%)")
                            else:
                                log_func(f"    ✓ {file}: {old_size//1024} KB")
                        
                        await asyncio.sleep(0.01)
                    
                    folder_reduction = (1 - folder_after/folder_before) * 100 if folder_before > 0 else 0
                    total_before += folder_before
                    total_after += folder_after
                    processed += 1
                    log_func(f"  📊 Итого папки: {folder_before//1024} KB → {folder_after//1024} KB (сжатие {folder_reduction:.0f}%)")
                    
                    await asyncio.sleep(0.05)
                
                if progress_widget:
                    progress_widget.update_progress(1.0, "✅ Оптимизация завершена!", page)
                    await asyncio.sleep(0.5)
                    progress_widget.hide(page)
                
                log_func(f"\n{'='*60}")
                log_func(f"✅ ОПТИМИЗАЦИЯ ЗАВЕРШЕНА!")
                log_func(f"📁 Обработано папок: {processed}")
                log_func(f"⏭️ Пропущено: {skipped}")
                if total_before > 0:
                    total_reduction = (1 - total_after/total_before) * 100
                    log_func(f"📊 Общий размер: {total_before//1024} KB → {total_after//1024} KB")
                    log_func(f"📊 Общее сжатие: {total_reduction:.0f}%")
                log_func(f"🎯 Теперь можно запустить архивацию!")
                log_func(f"{'='*60}\n")
                
                status_text.value = f"Оптимизация завершена: {processed} папок, сжатие {total_reduction:.0f}%"
                
            except Exception as e:
                log_func(f"❌ Ошибка оптимизации: {str(e)}")
                status_text.value = f"Ошибка: {str(e)}"
                if progress_widget:
                    progress_widget.hide(page)
            finally:
                is_working_ref[0] = False
                page.update()
        
        asyncio.create_task(optimize_task())
    
    # Собираем карточку
    card = ft.Container(
        content=ft.Column([
            ft.Text("Оптимизация изображений", size=AppSizes.FONT_SIZE_MEDIUM, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ft.Container(height=AppSizes.PADDING_MEDIUM),
            
            ft.Row([
                ft.Text("Целевой размер архива:", size=AppSizes.FONT_SIZE_MEDIUM, color=AppColors.TEXT_SECONDARY),
                target_size_field,
                ft.Text("KB", size=AppSizes.FONT_SIZE_MEDIUM, color=AppColors.TEXT_SECONDARY),
            ], spacing=AppSizes.PADDING_MEDIUM, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            
            ft.Container(height=AppSizes.PADDING_MEDIUM),
            
            make_button("ОПТИМИЗИРОВАТЬ ВСЕ", optimize_all_folders, AppColors.SUCCESS, expand=True),
            
            ft.Container(height=AppSizes.PADDING_SMALL),
            
            status_text,
            
            ft.Container(height=AppSizes.PADDING_SMALL),
            
            ft.Text(
                "💡 Алгоритм:",
                size=AppSizes.FONT_SIZE_TINY,
                weight=ft.FontWeight.BOLD,
                color=AppColors.TEXT_SECONDARY,
            ),
            ft.Text(
                "   • Для лимита ≥250 KB используется lossless сжатие (Oxipng)",
                size=AppSizes.FONT_SIZE_TINY,
                color=AppColors.TEXT_SECONDARY,
            ),
            ft.Text(
                "   • Для лимита <250 KB используется lossy сжатие (pngquant)",
                size=AppSizes.FONT_SIZE_TINY,
                color=AppColors.TEXT_SECONDARY,
            ),
            ft.Text(
                "   • JPEG сжимается с качеством 85-45 в зависимости от лимита",
                size=AppSizes.FONT_SIZE_TINY,
                color=AppColors.TEXT_SECONDARY,
            ),
        ]),
        bgcolor=AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_MEDIUM,
        padding=AppSizes.PADDING_MEDIUM,
    )
    
    return card