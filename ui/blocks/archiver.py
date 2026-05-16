"""
Блок "Архивация" - создание ZIP архивов для папок с размерами.
"""

import flet as ft
import os
import zipfile
import shutil
import asyncio

from ui.styles import AppColors, AppSizes
from ui.components import make_button, make_outlined_button


def archiver_block(log_func, selected_path_ref, is_working_ref, page, progress_widget=None):
    """
    Создаёт блок "Архивация".
    """
    
    # Статусная строка
    status_text = ft.Text(
        value="Готов к архивации",
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
    
    def create_archive(folder_path, output_path):
        """Создаёт ZIP архив из файлов в папке (исключая .fla)"""
        files_to_zip = []
        folder_size = 0
        
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path) and not file.endswith('.fla'):
                files_to_zip.append(file_path)
                folder_size += os.path.getsize(file_path)
        
        if not files_to_zip:
            return None, 0
        
        # Создаём папку для архивов
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in files_to_zip:
                zf.write(file_path, os.path.basename(file_path))
        
        archive_size = os.path.getsize(output_path)
        return archive_size, folder_size
    
    def archive_all_folders(e):
        """Архивирует все папки с размерами"""
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        
        if not selected_path_ref[0]:
            log_func("Сначала выберите рабочую папку!")
            return
        
        is_working_ref[0] = True
        
        async def archive_task():
            try:
                log_func(f"\n{'='*60}")
                log_func(f"📦 АРХИВАЦИЯ ВСЕХ ПАПОК С РАЗМЕРАМИ")
                log_func(f"📁 Папка: {selected_path_ref[0]}")
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
                    progress_widget.update_progress(0, f"Архивация: 0/{total}", page)
                
                archive_count = 0
                total_before = 0
                total_after = 0
                
                for idx, folder_info in enumerate(size_folders):
                    folder_path = folder_info['path']
                    platform = folder_info['platform']
                    campaign = folder_info['campaign']
                    size_name = folder_info['size']
                    
                    progress_value = idx / total
                    if progress_widget:
                        progress_widget.update_progress(
                            progress_value,
                            f"📦 Архивация: {platform}/{campaign}/{size_name} ({idx+1}/{total})",
                            page
                        )
                    
                    log_func(f"\n📦 [{idx+1}/{total}] {platform}/{campaign}/{size_name}")
                    
                    # Создаём архив
                    zip_name = f"{size_name}_{campaign}_{platform}.zip"
                    zip_output_dir = os.path.join(os.path.dirname(folder_path), "zip")
                    zip_path = os.path.join(zip_output_dir, zip_name)
                    
                    # Проверяем, не существует ли уже архив
                    if os.path.exists(zip_path):
                        log_func(f"  ⚠️ Архив уже существует: {zip_name}")
                        continue
                    
                    archive_size, folder_size = create_archive(folder_path, zip_path)
                    
                    if archive_size:
                        total_before += folder_size
                        total_after += archive_size
                        reduction = (1 - archive_size/folder_size) * 100 if folder_size > 0 else 0
                        log_func(f"  ✅ Создан: {zip_name}")
                        log_func(f"     Размер: {archive_size // 1024} KB (сжатие {reduction:.0f}%)")
                        archive_count += 1
                    else:
                        log_func(f"  ⚠️ Нет файлов для архивации (или только .fla)")
                    
                    await asyncio.sleep(0.05)
                
                if progress_widget:
                    progress_widget.update_progress(1.0, "✅ Архивация завершена!", page)
                    await asyncio.sleep(0.5)
                    progress_widget.hide(page)
                
                log_func(f"\n{'='*60}")
                log_func(f"✅ АРХИВАЦИЯ ЗАВЕРШЕНА!")
                log_func(f"✅ Создано архивов: {archive_count} из {total}")
                if archive_count > 0:
                    log_func(f"📊 Общий размер: {total_before//1024} KB → {total_after//1024} KB")
                    log_func(f"📊 Общее сжатие: {(1 - total_after/total_before)*100:.0f}%")
                log_func(f"{'='*60}\n")
                
                status_text.value = f"Архивация завершена: {archive_count} архивов"
                
            except Exception as e:
                log_func(f"❌ Ошибка архивации: {str(e)}")
                status_text.value = f"Ошибка: {str(e)}"
                if progress_widget:
                    progress_widget.hide(page)
            finally:
                is_working_ref[0] = False
                page.update()
        
        asyncio.create_task(archive_task())
    
    def delete_all_zips(e):
        """Удаляет все созданные ZIP архивы и папки zip"""
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        
        if not selected_path_ref[0]:
            log_func("Сначала выберите рабочую папку!")
            return
        
        is_working_ref[0] = True
        
        async def delete_task():
            try:
                log_func(f"\n{'='*60}")
                log_func(f"🗑️ УДАЛЕНИЕ ВСЕХ ZIP АРХИВОВ")
                log_func(f"📁 Папка: {selected_path_ref[0]}")
                log_func(f"{'='*60}")
                
                if progress_widget:
                    progress_widget.update_progress(0, "Поиск архивов...", page)
                
                all_zips = []
                all_zip_folders = []
                
                for root, dirs, files in os.walk(selected_path_ref[0]):
                    for file in files:
                        if file.endswith('.zip'):
                            all_zips.append(os.path.join(root, file))
                    for dir_name in dirs:
                        if dir_name.lower() == "zip":
                            all_zip_folders.append(os.path.join(root, dir_name))
                    await asyncio.sleep(0.01)
                
                total_zips = len(all_zips)
                total_folders = len(all_zip_folders)
                
                if total_zips == 0 and total_folders == 0:
                    log_func("❌ Архивы и папки zip не найдены")
                    if progress_widget:
                        progress_widget.hide(page)
                    is_working_ref[0] = False
                    return
                
                log_func(f"📁 Найдено ZIP: {total_zips}, папок zip: {total_folders}")
                
                if progress_widget:
                    progress_widget.update_progress(0.2, f"Удаление архивов...", page)
                
                deleted_zips = 0
                deleted_folders = 0
                
                for idx, file_path in enumerate(all_zips):
                    progress_val = 0.2 + (idx / total_zips) * 0.6 if total_zips > 0 else 0.2
                    if progress_widget:
                        progress_widget.update_progress(
                            progress_val,
                            f"Удаление: {os.path.basename(file_path)} ({idx+1}/{total_zips})",
                            page
                        )
                    try:
                        os.remove(file_path)
                        deleted_zips += 1
                        log_func(f"  ✅ Удалён: {os.path.basename(file_path)}")
                    except Exception as e:
                        log_func(f"  ❌ Ошибка: {os.path.basename(file_path)} - {str(e)}")
                    await asyncio.sleep(0.01)
                
                for idx, folder_path in enumerate(all_zip_folders):
                    progress_val = 0.8 + (idx / total_folders) * 0.2 if total_folders > 0 else 0.8
                    if progress_widget:
                        progress_widget.update_progress(
                            progress_val,
                            f"Удаление папки: {os.path.basename(folder_path)}",
                            page
                        )
                    try:
                        shutil.rmtree(folder_path)
                        deleted_folders += 1
                        log_func(f"  ✅ Удалена папка: {os.path.basename(folder_path)}")
                    except Exception as e:
                        log_func(f"  ❌ Ошибка: {os.path.basename(folder_path)} - {str(e)}")
                    await asyncio.sleep(0.01)
                
                if progress_widget:
                    progress_widget.update_progress(1.0, "✅ Удаление завершено!", page)
                    await asyncio.sleep(0.5)
                    progress_widget.hide(page)
                
                log_func(f"\n{'='*60}")
                log_func(f"✅ УДАЛЕНИЕ ЗАВЕРШЕНО!")
                log_func(f"✅ Удалено ZIP: {deleted_zips}, папок zip: {deleted_folders}")
                log_func(f"{'='*60}\n")
                
                status_text.value = f"Удалено архивов: {deleted_zips}, папок: {deleted_folders}"
                
            except Exception as e:
                log_func(f"❌ Ошибка удаления: {str(e)}")
                status_text.value = f"Ошибка: {str(e)}"
                if progress_widget:
                    progress_widget.hide(page)
            finally:
                is_working_ref[0] = False
                page.update()
        
        asyncio.create_task(delete_task())
    
    # Собираем карточку
    card = ft.Container(
        content=ft.Column([
            ft.Text("Архивация", size=AppSizes.FONT_SIZE_MEDIUM, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ft.Container(height=AppSizes.PADDING_MEDIUM),
            
            ft.Row([
                make_button("АРХИВИРОВАТЬ ВСЕ", archive_all_folders, AppColors.SUCCESS, expand=True),
                make_outlined_button("УДАЛИТЬ ВСЕ АРХИВЫ", delete_all_zips, AppColors.BG_CARD, AppColors.ERROR, expand=True),
            ], spacing=AppSizes.PADDING_MEDIUM),
            
            ft.Container(height=AppSizes.PADDING_SMALL),
            
            status_text,
            
            ft.Container(height=AppSizes.PADDING_SMALL),
            
            ft.Text(
                "💡 Архивы создаются для папок, содержащих 'x' в имени (размеры)",
                size=AppSizes.FONT_SIZE_TINY,
                color=AppColors.TEXT_SECONDARY,
            ),
            ft.Text(
                "   Файлы .fla исключаются из архивов",
                size=AppSizes.FONT_SIZE_TINY,
                color=AppColors.TEXT_SECONDARY,
            ),
        ]),
        bgcolor=AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_MEDIUM,
        padding=AppSizes.PADDING_MEDIUM,
    )
    
    return card