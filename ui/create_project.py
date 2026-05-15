import flet as ft
import os
import tkinter as tk
from tkinter import filedialog
from modules.config import COLORS
from ui.components import make_button

def create_project_block(log_func, selected_path_ref, folder_text, page):
    """Создаёт блок 'Создать проект'"""
    
    project_name_input = ft.TextField(
        value="PROD",
        hint_text="Название проекта",
        width=200,
        height=40,
        text_size=13,
        bgcolor=COLORS["BG_INPUT"],
        border_color="#3d3d3d",
        color=COLORS["TEXT"],
    )
    
    platforms_inputs = []
    platforms_column = ft.Column(spacing=5)
    creative_names_inputs = []
    creative_names_column = ft.Column(spacing=5)
    
    def add_platform_field(value="Master"):
        """Добавляет новое поле для площадки"""
        text_field = ft.TextField(
            value=value,
            hint_text="Название площадки",
            width=200,  # добавьте эту строку
            expand=False,  # уберите expand или замените на False
            height=40,
            text_size=13,
            bgcolor=COLORS["BG_INPUT"],
            border_color="#3d3d3d",
            color=COLORS["TEXT"],
        )
        
        row = ft.Row(
            [text_field],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Исправлено: используем content вместо text
        remove_btn = ft.ElevatedButton(
            content=ft.Text("−", size=16, weight=ft.FontWeight.BOLD),
            bgcolor=COLORS["ERROR"],
            color=ft.Colors.WHITE,
            width=40,
            height=40,
        )
        add_btn = ft.ElevatedButton(
            content=ft.Text("+", size=16, weight=ft.FontWeight.BOLD),
            bgcolor=COLORS["SUCCESS"],
            color=ft.Colors.WHITE,
            width=40,
            height=40,
        )
        
        def remove_handler(e):
            if row in platforms_column.controls:
                idx = platforms_column.controls.index(row)
                platforms_column.controls.pop(idx)
                platforms_inputs.pop(idx)
                page.update()
        
        def add_handler(e):
            add_platform_field()
        
        remove_btn.on_click = remove_handler
        add_btn.on_click = add_handler
        
        row.controls.append(remove_btn)
        row.controls.append(add_btn)
        
        platforms_inputs.append(text_field)
        platforms_column.controls.append(row)
        page.update()
    
    def add_creative_field(value="creative"):
        """Добавляет новое поле для названия креатива"""
        text_field = ft.TextField(
            value=value,
            hint_text="Название креатива",
            expand=True,
            height=40,
            text_size=13,
            bgcolor=COLORS["BG_INPUT"],
            border_color="#3d3d3d",
            color=COLORS["TEXT"],
        )
        
        row = ft.Row(
            [text_field],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        remove_btn = ft.ElevatedButton(
            content=ft.Text("−", size=16, weight=ft.FontWeight.BOLD),
            bgcolor=COLORS["ERROR"],
            color=ft.Colors.WHITE,
            width=40,
            height=40,
        )
        add_btn = ft.ElevatedButton(
            content=ft.Text("+", size=16, weight=ft.FontWeight.BOLD),
            bgcolor=COLORS["SUCCESS"],
            color=ft.Colors.WHITE,
            width=40,
            height=40,
        )
        
        def remove_handler(e):
            if row in creative_names_column.controls:
                idx = creative_names_column.controls.index(row)
                creative_names_column.controls.pop(idx)
                creative_names_inputs.pop(idx)
                page.update()
        
        def add_handler(e):
            add_creative_field()
        
        remove_btn.on_click = remove_handler
        add_btn.on_click = add_handler
        
        row.controls.append(remove_btn)
        row.controls.append(add_btn)
        
        creative_names_inputs.append(text_field)
        creative_names_column.controls.append(row)
        page.update()
    
    # Добавляем поля по умолчанию
    add_platform_field("Master")
    add_creative_field("creative")
    
    def create_structure(e):
        project_name = project_name_input.value.strip()
        if not project_name:
            log_func("Введите название проекта!")
            return
        
        platforms = []
        for field in platforms_inputs:
            val = field.value.strip()
            if val:
                platforms.append(val)
        
        if not platforms:
            log_func("Добавьте хотя бы одну площадку!")
            return
        
        creatives = []
        for field in creative_names_inputs:
            val = field.value.strip()
            if val:
                creatives.append(val)
        
        if not creatives:
            log_func("Добавьте хотя бы одно название креатива!")
            return
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        base_folder = filedialog.askdirectory(title="Выберите папку для создания проекта")
        root.destroy()
        
        if not base_folder:
            log_func("Выбор папки отменён")
            return
        
        project_path = os.path.join(base_folder, project_name)
        main_folders = ["animate", "ai", "img", "opt_img", "psd", "screen", "publish"]
        
        try:
            os.makedirs(project_path, exist_ok=True)
            
            for main_folder in main_folders:
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
            
            log_func(f"\n✅ Проект '{project_name}' успешно создан!")
            log_func(f"📍 Путь: {project_path}")
            log_func(f"📁 Площадки ({len(platforms)}): {', '.join(platforms)}")
            log_func(f"📁 Креативы ({len(creatives)}): {', '.join(creatives)}")
            
            selected_path_ref[0] = project_path
            folder_text.value = os.path.basename(selected_path_ref[0])
            folder_text.color = COLORS["PRIMARY"]
            folder_text.tooltip = selected_path_ref[0]
            log_func(f"📂 Папка проекта выбрана как рабочая")
            
        except Exception as e:
            log_func(f"❌ Ошибка создания проекта: {str(e)}")
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Создать проект", size=12, weight=ft.FontWeight.BOLD, color=COLORS["TEXT"]),
            ft.Row([
                ft.Text("Название проекта:", size=12, color=COLORS["TEXT_SECONDARY"]),
                project_name_input,
            ], spacing=8, alignment=ft.MainAxisAlignment.START),
            ft.Text("Площадки:", size=12, color=COLORS["TEXT_SECONDARY"]),
            platforms_column,
            ft.Text("Названия креативов:", size=12, color=COLORS["TEXT_SECONDARY"]),
            creative_names_column,
            make_button("СОЗДАТЬ", create_structure, COLORS["SUCCESS"], True, 40),
        ], spacing=10),
        padding=12,
        bgcolor=COLORS["BG_CARD"],
        border_radius=8,
    )