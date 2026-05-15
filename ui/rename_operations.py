import flet as ft
import os
import asyncio
from modules.config import COLORS
from modules import rename_utils
from ui.components import make_button
from ui.progress_ui import update_progress, hide_progress

def rename_operations_block(log_func, selected_path_ref, is_working_ref, page):
    """Создаёт блок 'Пакетное переименование'"""
    
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
    
    progress_bar_ref = [None]
    progress_text_ref = [None]
    
    def set_progress_refs(bar, text):
        progress_bar_ref[0] = bar
        progress_text_ref[0] = text
    
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
        
        if progress_bar_ref[0] and progress_text_ref[0]:
            update_progress(progress_bar_ref[0], progress_text_ref[0], 0, "Поиск файлов для переименования...", page)
        
        async def rename_task():
            try:
                items = os.listdir(selected_path_ref[0])
                items_to_rename = [name for name in items if name != 'zip' and find_text in name]
                total = len(items_to_rename)
                
                if total == 0:
                    log_func("Нет файлов для переименования")
                    if progress_bar_ref[0] and progress_text_ref[0]:
                        hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
                    is_working_ref[0] = False
                    return
                
                renamed_count = 0
                errors = 0
                
                for idx, name in enumerate(items_to_rename):
                    progress_val = idx / total
                    if progress_bar_ref[0] and progress_text_ref[0]:
                        update_progress(
                            progress_bar_ref[0], progress_text_ref[0],
                            progress_val,
                            f"Переименование: {name} → {name.replace(find_text, replace_text)}",
                            page
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
                
                if progress_bar_ref[0] and progress_text_ref[0]:
                    update_progress(progress_bar_ref[0], progress_text_ref[0], 1.0, "✅ Переименование завершено!", page)
                    await asyncio.sleep(0.5)
                    hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
                
                log_func(f"\n{'='*50}")
                log_func(f"ПЕРЕИМЕНОВАНИЕ ЗАВЕРШЕНО!")
                log_func(f"Успешно: {renamed_count}, Ошибок: {errors}")
                log_func(f"{'='*50}\n")
                
            except Exception as e:
                log_func(f"Ошибка: {str(e)}")
                if progress_bar_ref[0] and progress_text_ref[0]:
                    hide_progress(progress_bar_ref[0], progress_text_ref[0], page)
            finally:
                is_working_ref[0] = False
        
        asyncio.create_task(rename_task())
    
    container = ft.Container(
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
    )
    
    return container, set_progress_refs