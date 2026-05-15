import flet as ft
import tkinter as tk
from tkinter import filedialog
import os
import time
import asyncio
from modules.config import COLORS
from modules import fla_operations as fla_ops
from ui.components import make_outlined_button
from ui.progress_ui import update_progress, hide_progress

def fla_operations_block(log_func, selected_path_ref, is_working_ref, page):
    """Создаёт блок '.fla операции'"""
    
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
    
    progress_bar_ref = [None]
    progress_text_ref = [None]
    
    def set_progress_refs(bar, text):
        progress_bar_ref[0] = bar
        progress_text_ref[0] = text
    
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
            is_working_ref[0] = True
            start_time = time.time()
            
            if progress_bar_ref[0] and progress_text_ref[0]:
                update_progress(progress_bar_ref[0], progress_text_ref[0], 0, f"Поиск {size}.fla...", page)
            
            try:
                found_files = []
                total_found = 0
                for result in fla_ops.find_fla_files(folder_path, size):
                    if isinstance(result, list):
                        found_files = result
                        total_found = len(found_files)
                        break
                    await asyncio.sleep(0.01)
                
                if total_found == 0:
                    log_func(f"Файл {size}.fla не найден")
                    if progress_bar_ref[0] and progress_text_ref[0]:
                        hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
                else:
                    log_func(f"Найдено файлов: {total_found}")
                    page.update()
                    
                    if progress_bar_ref[0] and progress_text_ref[0]:
                        update_progress(progress_bar_ref[0], progress_text_ref[0], 0.2, f"Открытие {total_found} файлов...", page)
                    
                    for idx, file_path in enumerate(found_files):
                        progress_val = 0.2 + (idx / total_found) * 0.8
                        if progress_bar_ref[0] and progress_text_ref[0]:
                            update_progress(
                                progress_bar_ref[0], progress_text_ref[0],
                                progress_val,
                                f"Открытие: {os.path.basename(file_path)} ({idx+1}/{total_found})",
                                page
                            )
                        try:
                            os.startfile(file_path)
                            log_func(f"  ✅ Открыт: {os.path.basename(file_path)}")
                        except Exception as e:
                            log_func(f"  ❌ Ошибка: {os.path.basename(file_path)}")
                        await asyncio.sleep(0.1)
                    
                    if progress_bar_ref[0] and progress_text_ref[0]:
                        update_progress(progress_bar_ref[0], progress_text_ref[0], 1.0, "✅ Готово!", page)
                        await asyncio.sleep(0.5)
                        hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
                    
                    elapsed = time.time() - start_time
                    log_func(f"\n✅ Открыто файлов: {total_found} за {elapsed:.1f} сек")
            except Exception as e:
                log_func(f"❌ Ошибка: {str(e)}")
                if progress_bar_ref[0] and progress_text_ref[0]:
                    hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
            finally:
                is_working_ref[0] = False
        
        asyncio.create_task(search_task())
    
    def open_all_fla(folder_path):
        log_func(f"\n🔍 ПОИСК ВСЕХ .fla в папке: {folder_path}")
        
        async def search_task():
            is_working_ref[0] = True
            start_time = time.time()
            
            if progress_bar_ref[0] and progress_text_ref[0]:
                update_progress(progress_bar_ref[0], progress_text_ref[0], 0, "Поиск всех .fla файлов...", page)
            
            try:
                found_files = []
                total_found = 0
                for result in fla_ops.find_fla_files(folder_path):
                    if isinstance(result, list):
                        found_files = result
                        total_found = len(found_files)
                        break
                    await asyncio.sleep(0.01)
                
                if total_found == 0:
                    log_func(".fla файлы не найдены")
                    if progress_bar_ref[0] and progress_text_ref[0]:
                        hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
                else:
                    log_func(f"Найдено .fla файлов: {total_found}")
                    page.update()
                    
                    if progress_bar_ref[0] and progress_text_ref[0]:
                        update_progress(progress_bar_ref[0], progress_text_ref[0], 0.2, f"Открытие {total_found} файлов...", page)
                    
                    for idx, file_path in enumerate(found_files):
                        progress_val = 0.2 + (idx / total_found) * 0.8
                        if progress_bar_ref[0] and progress_text_ref[0]:
                            update_progress(
                                progress_bar_ref[0], progress_text_ref[0],
                                progress_val,
                                f"Открытие: {os.path.basename(file_path)} ({idx+1}/{total_found})",
                                page
                            )
                        try:
                            os.startfile(file_path)
                            if (idx + 1) % 10 == 0:
                                log_func(f"  Открыто {idx+1}/{total_found} файлов")
                        except Exception as e:
                            log_func(f"  ❌ Ошибка: {os.path.basename(file_path)}")
                        await asyncio.sleep(0.05)
                    
                    if progress_bar_ref[0] and progress_text_ref[0]:
                        update_progress(progress_bar_ref[0], progress_text_ref[0], 1.0, "✅ Готово!", page)
                        await asyncio.sleep(0.5)
                        hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
                    
                    elapsed = time.time() - start_time
                    log_func(f"\n✅ Открыто всех .fla файлов: {total_found} за {elapsed:.1f} сек")
            except Exception as e:
                log_func(f"❌ Ошибка: {str(e)}")
                if progress_bar_ref[0] and progress_text_ref[0]:
                    hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
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
    
    container = ft.Container(
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
    )
    
    return container, set_progress_refs