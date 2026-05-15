"""
Блок "FLA операции" - поиск и открытие .fla файлов.
"""

import flet as ft
import os
import time
import tkinter as tk
from tkinter import filedialog

from ui.styles import AppColors, AppSizes
from ui.components import make_button, make_text_field, make_outlined_button


def fla_operations_block(log_func, selected_path_ref, is_working_ref, page, progress_widget=None):
    """
    Создаёт блок "FLA операции".
    """
    
    # Поле для ввода размера
    size_input = make_text_field(
        value="240x400",
        hint_text="Размер (например, 240x400)",
        width=AppSizes.INPUT_WIDTH_MEDIUM,
    )
    
    # Статусная строка
    status_text = ft.Text(
        value="Готов к поиску",
        size=AppSizes.FONT_SIZE_SMALL,
        color=AppColors.TEXT_SECONDARY,
    )
    
    def find_fla_files(folder_path, size=None):
        """Поиск .fla файлов в папке"""
        found_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if size:
                    if file == f"{size}.fla":
                        found_files.append(os.path.join(root, file))
                elif file.endswith('.fla'):
                    found_files.append(os.path.join(root, file))
        return found_files
    
    def pick_folder(callback):
        """Открывает диалог выбора папки"""
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        initial_dir = selected_path_ref[0] if selected_path_ref[0] else os.path.expanduser("~")
        folder_selected = filedialog.askdirectory(title="Выберите папку для поиска", initialdir=initial_dir)
        root.destroy()
        if folder_selected:
            callback(folder_selected)
        else:
            log_func("Выбор папки отменён")
    
    def search_and_open_by_size(folder_path):
        """Поиск и открытие .fla по размеру"""
        size = size_input.value.strip()
        if not size:
            log_func("Введите размер файла!")
            return
        
        log_func(f"\n🔍 ПОИСК {size}.fla в папке: {folder_path}")
        
        try:
            # Поиск файлов
            found_files = find_fla_files(folder_path, size)
            total_found = len(found_files)
            
            if total_found == 0:
                log_func(f"❌ Файл {size}.fla не найден")
                status_text.value = f"Файл {size}.fla не найден"
            else:
                log_func(f"📁 Найдено файлов: {total_found}")
                page.update()
                
                # Открываем файлы
                for idx, file_path in enumerate(found_files):
                    try:
                        os.startfile(file_path)
                        log_func(f"  ✅ Открыт: {os.path.basename(file_path)}")
                    except Exception as e:
                        log_func(f"  ❌ Ошибка: {os.path.basename(file_path)} - {str(e)}")
                
                log_func(f"\n✅ Открыто файлов: {total_found}")
                status_text.value = f"Открыто {total_found} файлов"
                
        except Exception as e:
            log_func(f"❌ Ошибка: {str(e)}")
            status_text.value = f"Ошибка: {str(e)}"
        finally:
            page.update()
    
    def search_and_open_all(folder_path):
        """Поиск и открытие всех .fla файлов"""
        log_func(f"\n🔍 ПОИСК ВСЕХ .fla в папке: {folder_path}")
        
        try:
            # Поиск файлов
            found_files = find_fla_files(folder_path)
            total_found = len(found_files)
            
            if total_found == 0:
                log_func("❌ .fla файлы не найдены")
                status_text.value = "Файлы .fla не найдены"
            else:
                log_func(f"📁 Найдено .fla файлов: {total_found}")
                page.update()
                
                # Открываем файлы
                for idx, file_path in enumerate(found_files):
                    try:
                        os.startfile(file_path)
                        if (idx + 1) % 10 == 0:
                            log_func(f"  Открыто {idx+1}/{total_found} файлов")
                    except Exception as e:
                        log_func(f"  ❌ Ошибка: {os.path.basename(file_path)} - {str(e)}")
                
                log_func(f"\n✅ Открыто всех .fla файлов: {total_found}")
                status_text.value = f"Открыто {total_found} файлов"
                
        except Exception as e:
            log_func(f"❌ Ошибка: {str(e)}")
            status_text.value = f"Ошибка: {str(e)}"
        finally:
            page.update()
    
    def on_search_by_size(e):
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        if not selected_path_ref[0]:
            log_func("Сначала выберите рабочую папку!")
            return
        pick_folder(search_and_open_by_size)
    
    def on_search_all(e):
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        if not selected_path_ref[0]:
            log_func("Сначала выберите рабочую папку!")
            return
        pick_folder(search_and_open_all)
    
    # Собираем карточку
    card = ft.Container(
        content=ft.Column([
            ft.Text("FLA операции", size=AppSizes.FONT_SIZE_MEDIUM, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ft.Container(height=AppSizes.PADDING_MEDIUM),
            
            ft.Row([
                ft.Text("Размер файла:", size=AppSizes.FONT_SIZE_MEDIUM, color=AppColors.TEXT_SECONDARY),
                size_input,
            ], spacing=AppSizes.PADDING_MEDIUM, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            
            ft.Container(height=AppSizes.PADDING_SMALL),
            
            ft.Row([
                make_outlined_button("Открыть .fla по размеру", on_search_by_size, AppColors.BG_CARD, AppColors.PRIMARY, expand=True),
                make_outlined_button("Открыть все .fla", on_search_all, AppColors.BG_CARD, AppColors.SUCCESS, expand=True),
            ], spacing=AppSizes.PADDING_MEDIUM),
            
            ft.Container(height=AppSizes.PADDING_SMALL),
            
            status_text,
        ]),
        bgcolor=AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_MEDIUM,
        padding=AppSizes.PADDING_MEDIUM,
    )
    
    return card