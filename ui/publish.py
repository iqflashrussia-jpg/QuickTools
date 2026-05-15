import flet as ft
import os
from modules.config import COLORS
from ui.components import make_button

def publish_block(log_func, selected_path_ref, folder_text, page):
    """Создаёт блок 'Publish' - создаёт структуру внутри папки publish"""
    
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
    
    # Названия креативов (будут созданы как папки)
    creative_names_inputs = []
    creative_names_column = ft.Column(spacing=5)
    
    def add_creative_field(value="creative"):
        """Добавляет новое поле для названия креатива"""
        text_field = ft.TextField(
            value=value,
            hint_text="Название креатива",
            width=200,
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
        
        remove_btn = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE,
            icon_color=COLORS["ERROR"],
            icon_size=24,
            tooltip="Удалить креатив",
        )
        add_btn = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=COLORS["SUCCESS"],
            icon_size=24,
            tooltip="Добавить креатив",
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
    
    # Структура: список подканалов, у каждого свой список площадок
    subchannels_data = []
    subchannels_column = ft.Column(spacing=15)
    
    def add_platform_to_subchannel(subchannel_index, platform_value="Яндекс - Баннеры"):
        """Добавляет площадку к конкретному подканалу"""
        subchannel = subchannels_data[subchannel_index]
        platforms_inputs = subchannel["platforms"]
        platforms_column = subchannel["platforms_column"]
        
        text_field = ft.TextField(
            value=platform_value,
            hint_text="Название площадки",
            width=200,
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
        
        remove_btn = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE,
            icon_color=COLORS["ERROR"],
            icon_size=24,
            tooltip="Удалить площадку",
        )
        add_btn = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=COLORS["SUCCESS"],
            icon_size=24,
            tooltip="Добавить площадку",
        )
        
        def remove_handler(e):
            if row in platforms_column.controls:
                idx = platforms_column.controls.index(row)
                platforms_column.controls.pop(idx)
                platforms_inputs.pop(idx)
                page.update()
        
        def add_handler(e):
            add_platform_to_subchannel(subchannel_index)
        
        remove_btn.on_click = remove_handler
        add_btn.on_click = add_handler
        
        row.controls.append(remove_btn)
        row.controls.append(add_btn)
        
        platforms_inputs.append(text_field)
        platforms_column.controls.append(row)
        page.update()
    
    def add_subchannel_field(value="5_Context_Media"):
        """Добавляет новый подканал со своим списком площадок"""
        subchannel_name = ft.TextField(
            value=value,
            hint_text="Название подканала",
            width=250,
            height=40,
            text_size=13,
            bgcolor=COLORS["BG_INPUT"],
            border_color="#3d3d3d",
            color=COLORS["TEXT"],
        )
        
        platforms_inputs = []
        platforms_column = ft.Column(spacing=5)
        
        platforms_header = ft.Text("Площадки:", size=11, color=COLORS["TEXT_SECONDARY"])
        
        subchannel_container = ft.Column(spacing=5)
        subchannel_container.controls.append(subchannel_name)
        subchannel_container.controls.append(platforms_header)
        subchannel_container.controls.append(platforms_column)
        
        subchannel_row = ft.Row(
            [subchannel_container],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
        
        remove_subchannel_btn = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE,
            icon_color=COLORS["ERROR"],
            icon_size=24,
            tooltip="Удалить подканал",
        )
        add_subchannel_btn = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=COLORS["SUCCESS"],
            icon_size=24,
            tooltip="Добавить подканал",
        )
        
        def remove_subchannel_handler(e):
            for i, data in enumerate(subchannels_data):
                if data["row"] == subchannel_row:
                    subchannels_data.pop(i)
                    break
            if subchannel_row in subchannels_column.controls:
                idx = subchannels_column.controls.index(subchannel_row)
                subchannels_column.controls.pop(idx)
                page.update()
        
        def add_subchannel_handler(e):
            add_subchannel_field()
        
        remove_subchannel_btn.on_click = remove_subchannel_handler
        add_subchannel_btn.on_click = add_subchannel_handler
        
        subchannel_row.controls.append(remove_subchannel_btn)
        subchannel_row.controls.append(add_subchannel_btn)
        
        subchannels_data.append({
            "name_field": subchannel_name,
            "platforms": platforms_inputs,
            "platforms_column": platforms_column,
            "row": subchannel_row,
            "container": subchannel_container
        })
        
        add_platform_to_subchannel(len(subchannels_data) - 1, "Яндекс - Баннеры")
        
        subchannels_column.controls.append(subchannel_row)
        page.update()
    
    # Добавляем первый подканал и первый креатив по умолчанию
    add_subchannel_field("5_Context_Media")
    add_creative_field("creative")
    
    def create_structure(e):
        if not selected_path_ref[0]:
            log_func("Сначала выберите рабочую папку с проектом или создайте проект!")
            return
        
        project_name = project_name_input.value.strip()
        if not project_name:
            log_func("Введите название проекта!")
            return
        
        # Собираем названия креативов
        creatives = []
        for field in creative_names_inputs:
            val = field.value.strip()
            if val:
                creatives.append(val)
        
        if not creatives:
            log_func("Добавьте хотя бы одно название креатива!")
            return
        
        subchannels = []
        for data in subchannels_data:
            subchannel_name = data["name_field"].value.strip()
            if not subchannel_name:
                log_func("Название подканала не может быть пустым!")
                return
            
            platforms = []
            for field in data["platforms"]:
                val = field.value.strip()
                if val:
                    platforms.append(val)
            
            if not platforms:
                log_func(f"Для подканала '{subchannel_name}' добавьте хотя бы одну площадку!")
                return
            
            subchannels.append({
                "name": subchannel_name,
                "platforms": platforms
            })
        
        if not subchannels:
            log_func("Добавьте хотя бы один подканал!")
            return
        
        # Путь к папке publish
        project_path = selected_path_ref[0]
        publish_path = os.path.join(project_path, "publish", project_name)
        
        try:
            os.makedirs(publish_path, exist_ok=True)
            
            # Создаём структуру: подканал → площадка → креатив
            for subchannel in subchannels:
                subchannel_path = os.path.join(publish_path, subchannel["name"])
                for platform in subchannel["platforms"]:
                    platform_path = os.path.join(subchannel_path, platform)
                    for creative in creatives:
                        creative_path = os.path.join(platform_path, creative)
                        os.makedirs(creative_path, exist_ok=True)
            
            log_func(f"\n✅ Структура публикации успешно создана!")
            log_func(f"📍 Путь: {publish_path}")
            log_func(f"📁 Проект: {project_name}")
            log_func(f"📁 Подканалы ({len(subchannels)}):")
            for sub in subchannels:
                log_func(f"     - {sub['name']} → площадки: {', '.join(sub['platforms'])}")
            log_func(f"📁 Креативы ({len(creatives)}): {', '.join(creatives)}")
            
        except Exception as e:
            log_func(f"❌ Ошибка создания структуры: {str(e)}")
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Publish", size=12, weight=ft.FontWeight.BOLD, color=COLORS["TEXT"]),
            ft.Row([
                ft.Text("Название проекта:", size=12, color=COLORS["TEXT_SECONDARY"]),
                project_name_input,
            ], spacing=8, alignment=ft.MainAxisAlignment.START),
            ft.Text("Подканалы и площадки:", size=12, color=COLORS["TEXT_SECONDARY"]),
            subchannels_column,
            ft.Text("Названия креативов:", size=12, color=COLORS["TEXT_SECONDARY"]),
            creative_names_column,
            make_button("СОЗДАТЬ", create_structure, COLORS["SUCCESS"], True, 40),
        ], spacing=10),
        padding=12,
        bgcolor=COLORS["BG_CARD"],
        border_radius=8,
    )