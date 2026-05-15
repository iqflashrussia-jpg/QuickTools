import flet as ft
import os
import tkinter as tk
from tkinter import filedialog
from modules.config import COLORS
from ui.components import make_button

def publish_block(log_func, selected_path_ref, folder_text, page):
    """Создаёт блок 'Publish'"""
    
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
    
    subchannels_inputs = []
    subchannels_column = ft.Column(spacing=5)
    platforms_inputs = []
    platforms_column = ft.Column(spacing=5)
    creative_names_inputs = []
    creative_names_column = ft.Column(spacing=5)
    
    def add_subchannel_field(value="5_Context_Media"):
        text_field = ft.TextField(
            value=value,
            hint_text="Название подканала",
            expand=True,
            height=40,
            text_size=13,
            bgcolor=COLORS["BG_INPUT"],
            border_color="#3d3d3d",
            color=COLORS["TEXT"],
        )
        
        row = ft.Row([text_field], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        remove_btn = ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE, icon_color=COLORS["ERROR"], icon_size=20)
        add_btn = ft.IconButton(icon=ft.Icons.ADD_CIRCLE, icon_color=COLORS["SUCCESS"], icon_size=20)
        
        def remove_handler(e):
            if row in subchannels_column.controls:
                idx = subchannels_column.controls.index(row)
                subchannels_column.controls.pop(idx)
                subchannels_inputs.pop(idx)
                page.update()
        
        def add_handler(e):
            add_subchannel_field()
        
        remove_btn.on_click = remove_handler
        add_btn.on_click = add_handler
        
        row.controls.append(remove_btn)
        row.controls.append(add_btn)
        
        subchannels_inputs.append(text_field)
        subchannels_column.controls.append(row)
        page.update()
    
    def add_platform_field(value="Яндекс - Баннеры"):
        text_field = ft.TextField(
            value=value,
            hint_text="Название площадки",
            expand=True,
            height=40,
            text_size=13,
            bgcolor=COLORS["BG_INPUT"],
            border_color="#3d3d3d",
            color=COLORS["TEXT"],
        )
        
        row = ft.Row([text_field], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        remove_btn = ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE, icon_color=COLORS["ERROR"], icon_size=20)
        add_btn = ft.IconButton(icon=ft.Icons.ADD_CIRCLE, icon_color=COLORS["SUCCESS"], icon_size=20)
        
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
        
        row = ft.Row([text_field], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        remove_btn = ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE, icon_color=COLORS["ERROR"], icon_size=20)
        add_btn = ft.IconButton(icon=ft.Icons.ADD_CIRCLE, icon_color=COLORS["SUCCESS"], icon_size=20)
        
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
    
    add_subchannel_field("5_Context_Media")
    add_platform_field("Яндекс - Баннеры")
    add_creative_field("creative")
    
    def create_structure(e):
        project_name = project_name_input.value.strip()
        if not project_name:
            log_func("Введите название проекта!")
            return
        
        subchannels = [f.value.strip() for f in subchannels_inputs if f.value.strip()]
        if not subchannels:
            log_func("Добавьте хотя бы один подканал!")
            return
        
        platforms = [f.value.strip() for f in platforms_inputs if f.value.strip()]
        if not platforms:
            log_func("Добавьте хотя бы одну площадку!")
            return
        
        creatives = [f.value.strip() for f in creative_names_inputs if f.value.strip()]
        if not creatives:
            log_func("Добавьте хотя бы одно название креатива!")
            return
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        base_folder = filedialog.askdirectory(title="Выберите папку для создания структуры публикации")
        root.destroy()
        
        if not base_folder:
            log_func("Выбор папки отменён")
            return
        
        project_path = os.path.join(base_folder, project_name)
        
        try:
            os.makedirs(project_path, exist_ok=True)
            
            for subchannel in subchannels:
                subchannel_path = os.path.join(project_path, subchannel)
                for platform in platforms:
                    platform_path = os.path.join(subchannel_path, platform)
                    for creative in creatives:
                        creative_path = os.path.join(platform_path, creative)
                        os.makedirs(creative_path, exist_ok=True)
            
            log_func(f"\n✅ Структура публикации успешно создана!")
            log_func(f"📍 Путь: {project_path}")
            log_func(f"📁 Подканалы ({len(subchannels)}): {', '.join(subchannels)}")
            log_func(f"📁 Площадки ({len(platforms)}): {', '.join(platforms)}")
            log_func(f"📁 Креативы ({len(creatives)}): {', '.join(creatives)}")
            
            selected_path_ref[0] = project_path
            folder_text.value = os.path.basename(selected_path_ref[0])
            folder_text.color = COLORS["PRIMARY"]
            folder_text.tooltip = selected_path_ref[0]
            log_func(f"📂 Папка проекта выбрана как рабочая")
            
        except Exception as e:
            log_func(f"❌ Ошибка создания структуры: {str(e)}")
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Publish", size=12, weight=ft.FontWeight.BOLD, color=COLORS["TEXT"]),
            ft.Row([
                ft.Text("Название проекта:", size=12, color=COLORS["TEXT_SECONDARY"]),
                project_name_input,
            ], spacing=8, alignment=ft.MainAxisAlignment.START),
            ft.Text("Подканал:", size=12, color=COLORS["TEXT_SECONDARY"]),
            subchannels_column,
            ft.Text("Площадка:", size=12, color=COLORS["TEXT_SECONDARY"]),
            platforms_column,
            ft.Text("Названия креативов:", size=12, color=COLORS["TEXT_SECONDARY"]),
            creative_names_column,
            make_button("СОЗДАТЬ", create_structure, COLORS["SUCCESS"], True, 40),
        ], spacing=10),
        padding=12,
        bgcolor=COLORS["BG_CARD"],
        border_radius=8,
    )