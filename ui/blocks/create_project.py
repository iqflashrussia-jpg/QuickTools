"""
Блок "Создание проекта" - упрощённая версия.
"""

import flet as ft
import os
import tkinter as tk
from tkinter import filedialog

from ui.styles import AppColors, AppSizes
from ui.components import make_button, make_text_field


def create_project_block(log_func, selected_path_ref, is_working_ref, page, progress_widget=None, folder_update_callback=None):
    """
    Создаёт блок "Создание проекта".
    """
    
    # Списки для хранения полей
    platform_fields = []
    creative_fields = []
    
    # Контейнеры для динамических полей
    platforms_container = ft.Column(spacing=10)
    creatives_container = ft.Column(spacing=10)
    
    # Поле для названия проекта
    project_name_field = make_text_field(
        value="PROD",
        hint_text="Название проекта",
        width=AppSizes.INPUT_WIDTH_MEDIUM,
    )
    
    def add_platform_field(value="Master"):
        """Добавляет новое поле для площадки"""
        text_field = ft.TextField(
            value=value,
            hint_text="Название площадки",
            width=AppSizes.INPUT_WIDTH_LARGE,
            height=AppSizes.INPUT_HEIGHT,
            text_size=AppSizes.FONT_SIZE_LARGE,
            bgcolor=AppColors.BG_INPUT,
            border_color=AppColors.BORDER,
            color=AppColors.TEXT_PRIMARY,
        )
        
        row = ft.Row(
            [text_field],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        remove_btn = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE,
            icon_color=AppColors.ERROR,
            icon_size=24,
            tooltip="Удалить",
        )
        add_btn = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=AppColors.SUCCESS,
            icon_size=24,
            tooltip="Добавить",
        )
        
        def remove_handler(e):
            for i, r in enumerate(platforms_container.controls):
                if r == row:
                    platforms_container.controls.pop(i)
                    platform_fields.pop(i)
                    page.update()
                    break
        
        def add_handler(e):
            add_platform_field()
        
        remove_btn.on_click = remove_handler
        add_btn.on_click = add_handler
        
        row.controls.append(remove_btn)
        row.controls.append(add_btn)
        
        platforms_container.controls.append(row)
        platform_fields.append(text_field)
        page.update()
    
    def add_creative_field(value="creative"):
        """Добавляет новое поле для креатива"""
        text_field = ft.TextField(
            value=value,
            hint_text="Название креатива",
            width=AppSizes.INPUT_WIDTH_LARGE,
            height=AppSizes.INPUT_HEIGHT,
            text_size=AppSizes.FONT_SIZE_LARGE,
            bgcolor=AppColors.BG_INPUT,
            border_color=AppColors.BORDER,
            color=AppColors.TEXT_PRIMARY,
        )
        
        row = ft.Row(
            [text_field],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        remove_btn = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE,
            icon_color=AppColors.ERROR,
            icon_size=24,
            tooltip="Удалить",
        )
        add_btn = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=AppColors.SUCCESS,
            icon_size=24,
            tooltip="Добавить",
        )
        
        def remove_handler(e):
            for i, r in enumerate(creatives_container.controls):
                if r == row:
                    creatives_container.controls.pop(i)
                    creative_fields.pop(i)
                    page.update()
                    break
        
        def add_handler(e):
            add_creative_field()
        
        remove_btn.on_click = remove_handler
        add_btn.on_click = add_handler
        
        row.controls.append(remove_btn)
        row.controls.append(add_btn)
        
        creatives_container.controls.append(row)
        creative_fields.append(text_field)
        page.update()
    
    # Добавляем начальные поля
    add_platform_field("Master")
    add_creative_field("creative")
    
    def create_structure(e):
        """Создаёт структуру папок"""
        if is_working_ref[0]:
            log_func("Операция уже выполняется, подождите...")
            return
        
        project_name = project_name_field.value.strip()
        if not project_name:
            log_func("Введите название проекта!")
            return
        
        # Собираем названия площадок
        platforms = []
        for field in platform_fields:
            val = field.value.strip()
            if val:
                platforms.append(val)
        
        if not platforms:
            log_func("Добавьте хотя бы одну площадку!")
            return
        
        # Собираем названия креативов
        creatives = []
        for field in creative_fields:
            val = field.value.strip()
            if val:
                creatives.append(val)
        
        if not creatives:
            log_func("Добавьте хотя бы одно название креатива!")
            return
        
        # Выбираем папку
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        base_folder = filedialog.askdirectory(title="Выберите папку для создания проекта")
        root.destroy()
        
        if not base_folder:
            log_func("Выбор папки отменён")
            return
        
        project_path = os.path.join(base_folder, project_name)
        
        # Папки, в которых нужно создать креативы
        folders_with_creatives = ["animate", "ai", "img", "opt_img", "psd", "screen"]
        # Папка publish - создаётся, но остаётся пустой
        publish_folder = "publish"
        
        is_working_ref[0] = True
        
        try:
            os.makedirs(project_path, exist_ok=True)
            
            # Создаём папки с креативами (animate, ai, img, opt_img, psd, screen)
            for main_folder in folders_with_creatives:
                main_folder_path = os.path.join(project_path, main_folder)
                
                if main_folder == "animate":
                    for platform in platforms:
                        platform_path = os.path.join(main_folder_path, platform)
                        for creative in creatives:
                            creative_path = os.path.join(platform_path, creative)
                            os.makedirs(creative_path, exist_ok=True)
                else:
                    for creative in creatives:
                        creative_path = os.path.join(main_folder_path, creative)
                        os.makedirs(creative_path, exist_ok=True)
            
            # Создаём пустую папку publish (без креативов)
            publish_path = os.path.join(project_path, publish_folder)
            os.makedirs(publish_path, exist_ok=True)
            
            log_func(f"\n✅ Проект '{project_name}' успешно создан!")
            log_func(f"📍 Путь: {project_path}")
            log_func(f"📁 Площадки ({len(platforms)}): {', '.join(platforms)}")
            log_func(f"📁 Креативы ({len(creatives)}): {', '.join(creatives)}")
            log_func(f"📁 Папка 'publish' создана и оставлена пустой")
            
            # Выбираем созданную папку как рабочую
            selected_path_ref[0] = project_path
            if folder_update_callback:
                folder_update_callback()
            log_func(f"📂 Папка проекта выбрана как рабочая")
            
        except Exception as e:
            log_func(f"❌ Ошибка создания проекта: {str(e)}")
        finally:
            is_working_ref[0] = False
    
    # Собираем карточки
    project_card = ft.Container(
        content=ft.Column([
            ft.Text("Название проекта", size=AppSizes.FONT_SIZE_MEDIUM, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ft.Container(height=AppSizes.PADDING_MEDIUM),
            project_name_field,
        ]),
        bgcolor=AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_MEDIUM,
        padding=AppSizes.PADDING_MEDIUM,
    )
    
    platforms_card = ft.Container(
        content=ft.Column([
            ft.Text("Площадки", size=AppSizes.FONT_SIZE_MEDIUM, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ft.Container(height=AppSizes.PADDING_MEDIUM),
            platforms_container,
        ]),
        bgcolor=AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_MEDIUM,
        padding=AppSizes.PADDING_MEDIUM,
    )
    
    creatives_card = ft.Container(
        content=ft.Column([
            ft.Text("Названия креативов", size=AppSizes.FONT_SIZE_MEDIUM, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ft.Container(height=AppSizes.PADDING_MEDIUM),
            creatives_container,
        ]),
        bgcolor=AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_MEDIUM,
        padding=AppSizes.PADDING_MEDIUM,
    )
    
    create_btn = ft.Container(
        content=make_button("СОЗДАТЬ", create_structure, AppColors.SUCCESS, expand=True),
        padding=ft.Padding(left=0, top=AppSizes.PADDING_MEDIUM, right=0, bottom=0),
    )
    
    # Собираем всё вместе
    content = ft.Column(
        [
            project_card,
            platforms_card,
            creatives_card,
            create_btn,
        ],
        spacing=AppSizes.PADDING_MEDIUM,
        expand=True,
    )
    
    return content