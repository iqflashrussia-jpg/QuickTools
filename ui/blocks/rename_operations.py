"""
Блок "Пакетное переименование" - замена текста в именах файлов и папок.
"""

import flet as ft
import os

from ui.styles import AppColors, AppSizes
from ui.components import make_button, make_text_field


def rename_operations_block(log_func, selected_path_ref, is_working_ref, page, progress_widget=None):
    """
    Создаёт блок "Пакетное переименование".
    """
    
    # Поля для поиска и замены
    find_field = make_text_field(
        value="",
        hint_text="Что ищем",
        width=AppSizes.INPUT_WIDTH_LARGE,
    )
    
    replace_field = make_text_field(
        value="",
        hint_text="На что заменяем",
        width=AppSizes.INPUT_WIDTH_LARGE,
    )
    
    # Чекбокс для учёта регистра
    case_sensitive_checkbox = ft.Checkbox(
        label="Учитывать регистр",
        value=False,
        label_style=ft.TextStyle(size=AppSizes.FONT_SIZE_SMALL, color=AppColors.TEXT_SECONDARY),
    )
    
    # Чекбокс для переименования папок
    rename_folders_checkbox = ft.Checkbox(
        label="Переименовывать папки",
        value=False,
        label_style=ft.TextStyle(size=AppSizes.FONT_SIZE_SMALL, color=AppColors.TEXT_SECONDARY),
    )
    
    # Статусная строка
    status_text = ft.Text(
        value="Готов к переименованию",
        size=AppSizes.FONT_SIZE_SMALL,
        color=AppColors.TEXT_SECONDARY,
    )
    
    def perform_rename(e):
        """Выполняет пакетное переименование"""
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        
        if not selected_path_ref[0]:
            log_func("Сначала выберите рабочую папку!")
            return
        
        find_text = find_field.value.strip()
        replace_text = replace_field.value.strip()
        
        if not find_text:
            log_func("Введите текст для поиска!")
            return
        
        case_sensitive = case_sensitive_checkbox.value
        rename_folders = rename_folders_checkbox.value
        
        log_func(f"\n{'='*50}")
        log_func(f"📝 ПАКЕТНОЕ ПЕРЕИМЕНОВАНИЕ")
        log_func(f"📁 Папка: {selected_path_ref[0]}")
        log_func(f"🔍 Поиск: '{find_text}' → Замена: '{replace_text}'")
        log_func(f"🔠 Учитывать регистр: {'Да' if case_sensitive else 'Нет'}")
        log_func(f"📂 Переименовывать папки: {'Да' if rename_folders else 'Нет'}")
        log_func(f"{'='*50}")
        
        try:
            # Собираем элементы для переименования
            items = os.listdir(selected_path_ref[0])
            
            # Фильтруем элементы
            items_to_rename = []
            for name in items:
                if name == 'zip':
                    continue
                
                # Проверяем, нужно ли переименовывать папки
                item_path = os.path.join(selected_path_ref[0], name)
                is_folder = os.path.isdir(item_path)
                
                if is_folder and not rename_folders:
                    continue
                
                # Проверяем наличие искомого текста
                if case_sensitive:
                    if find_text in name:
                        items_to_rename.append(name)
                else:
                    if find_text.lower() in name.lower():
                        items_to_rename.append(name)
            
            total = len(items_to_rename)
            
            if total == 0:
                log_func("⚠️ Нет файлов/папок для переименования")
                status_text.value = "Нет файлов для переименования"
                return
            
            log_func(f"📁 Найдено элементов для переименования: {total}")
            
            renamed_count = 0
            errors = 0
            
            for idx, name in enumerate(items_to_rename):
                old_path = os.path.join(selected_path_ref[0], name)
                
                # Выполняем замену с учётом регистра
                if case_sensitive:
                    new_name = name.replace(find_text, replace_text)
                else:
                    # Замена без учёта регистра (сохраняем оригинальный регистр)
                    new_name = name
                    lower_name = name.lower()
                    lower_find = find_text.lower()
                    idx_pos = lower_name.find(lower_find)
                    if idx_pos != -1:
                        new_name = name[:idx_pos] + replace_text + name[idx_pos + len(find_text):]
                
                new_path = os.path.join(selected_path_ref[0], new_name)
                
                # Проверяем, не существует ли уже файл с таким именем
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
            
            log_func(f"\n{'='*50}")
            log_func(f"✅ ПЕРЕИМЕНОВАНИЕ ЗАВЕРШЕНО!")
            log_func(f"✅ Успешно: {renamed_count}")
            log_func(f"❌ Ошибок: {errors}")
            log_func(f"{'='*50}\n")
            
            status_text.value = f"Переименовано: {renamed_count}, ошибок: {errors}"
            
        except Exception as e:
            log_func(f"❌ Ошибка: {str(e)}")
            status_text.value = f"Ошибка: {str(e)}"
        
        page.update()
    
    # Собираем карточку
    card = ft.Container(
        content=ft.Column([
            ft.Text("Пакетное переименование", size=AppSizes.FONT_SIZE_MEDIUM, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ft.Container(height=AppSizes.PADDING_MEDIUM),
            
            ft.Row([
                ft.Text("Искать:", size=AppSizes.FONT_SIZE_MEDIUM, color=AppColors.TEXT_SECONDARY),
                find_field,
            ], spacing=AppSizes.PADDING_MEDIUM, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            
            ft.Row([
                ft.Text("Заменить:", size=AppSizes.FONT_SIZE_MEDIUM, color=AppColors.TEXT_SECONDARY),
                replace_field,
            ], spacing=AppSizes.PADDING_MEDIUM, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            
            ft.Container(height=AppSizes.PADDING_SMALL),
            
            ft.Row([
                case_sensitive_checkbox,
                rename_folders_checkbox,
            ], spacing=AppSizes.PADDING_LARGE),
            
            ft.Container(height=AppSizes.PADDING_MEDIUM),
            
            make_button("ЗАМЕНИТЬ ВСЁ", perform_rename, AppColors.SUCCESS, expand=True),
            
            ft.Container(height=AppSizes.PADDING_SMALL),
            
            status_text,
        ]),
        bgcolor=AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_MEDIUM,
        padding=AppSizes.PADDING_MEDIUM,
    )
    
    return card