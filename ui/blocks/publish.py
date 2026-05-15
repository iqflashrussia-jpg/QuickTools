"""
Блок "Publish" - создание структуры внутри папки publish.
Структура: проект/подканал/площадка/креатив
"""

import flet as ft
import os

from ui.styles import AppColors, AppSizes
from ui.components import make_button, make_text_field


def publish_block(log_func, selected_path_ref, page, progress_widget=None):
    """
    Создаёт блок "Publish".
    """
    
    # Поле для названия проекта
    project_name_field = make_text_field(
        value="PROD",
        hint_text="Название проекта",
        width=AppSizes.INPUT_WIDTH_MEDIUM,
    )
    
    # Списки для хранения динамических полей
    subchannels_data = []  # список словарей: {"name_field": TextField, "platforms": [], "platforms_container": Column}
    subchannels_container = ft.Column(spacing=15)
    
    # Креативы (общие для всех подканалов и площадок)
    creative_fields = []
    creatives_container = ft.Column(spacing=10)
    
    def add_platform_to_subchannel(subchannel_index, platform_value="Яндекс - Баннеры"):
        """Добавляет площадку к конкретному подканалу"""
        subchannel = subchannels_data[subchannel_index]
        platforms = subchannel["platforms"]
        platforms_container = subchannel["platforms_container"]
        
        # Поле для названия площадки
        text_field = ft.TextField(
            value=platform_value,
            hint_text="Название площадки",
            width=AppSizes.INPUT_WIDTH_LARGE,
            height=AppSizes.INPUT_HEIGHT,
            text_size=AppSizes.FONT_SIZE_LARGE,
            bgcolor=AppColors.BG_INPUT,
            border_color=AppColors.BORDER,
            color=AppColors.TEXT_PRIMARY,
        )
        
        # Строка с полем и кнопками
        row = ft.Row([text_field], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Кнопки
        remove_btn = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE,
            icon_color=AppColors.ERROR,
            icon_size=24,
            tooltip="Удалить площадку",
        )
        add_btn = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=AppColors.SUCCESS,
            icon_size=24,
            tooltip="Добавить площадку",
        )
        
        def remove_handler(e):
            for i, r in enumerate(platforms_container.controls):
                if r == row:
                    platforms_container.controls.pop(i)
                    platforms.pop(i)
                    page.update()
                    break
        
        def add_handler(e):
            add_platform_to_subchannel(subchannel_index)
        
        remove_btn.on_click = remove_handler
        add_btn.on_click = add_handler
        
        row.controls.append(remove_btn)
        row.controls.append(add_btn)
        
        platforms_container.controls.append(row)
        platforms.append(text_field)
        page.update()
    
    def add_subchannel_field(value="5_Context_Media"):
        """Добавляет новый подканал со своим списком площадок"""
        subchannel_index = len(subchannels_data)
        
        # Поле для названия подканала
        name_field = ft.TextField(
            value=value,
            hint_text="Название подканала",
            width=AppSizes.INPUT_WIDTH_LARGE,
            height=AppSizes.INPUT_HEIGHT,
            text_size=AppSizes.FONT_SIZE_LARGE,
            bgcolor=AppColors.BG_INPUT,
            border_color=AppColors.BORDER,
            color=AppColors.TEXT_PRIMARY,
        )
        
        # Контейнер для площадок
        platforms = []
        platforms_container = ft.Column(spacing=5)
        
        # Заголовок "Площадки"
        platforms_header = ft.Text("Площадки:", size=AppSizes.FONT_SIZE_SMALL, color=AppColors.TEXT_SECONDARY)
        
        # Карточка подканала
        subchannel_card = ft.Container(
            content=ft.Column([
                name_field,
                ft.Container(height=AppSizes.PADDING_SMALL),
                platforms_header,
                platforms_container,
            ], spacing=5),
            bgcolor=AppColors.BG_INPUT,
            border_radius=AppSizes.BORDER_RADIUS_SMALL,
            padding=AppSizes.PADDING_SMALL,
        )
        
        # Строка с карточкой и кнопками управления
        row = ft.Row([subchannel_card], spacing=10, vertical_alignment=ft.CrossAxisAlignment.START)
        
        # Кнопки для подканала
        remove_btn = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE,
            icon_color=AppColors.ERROR,
            icon_size=24,
            tooltip="Удалить подканал",
        )
        add_btn = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=AppColors.SUCCESS,
            icon_size=24,
            tooltip="Добавить подканал",
        )
        
        def remove_handler(e):
            for i, data in enumerate(subchannels_data):
                if data["row"] == row:
                    subchannels_data.pop(i)
                    subchannels_container.controls.pop(i)
                    page.update()
                    break
        
        def add_handler(e):
            add_subchannel_field()
        
        remove_btn.on_click = remove_handler
        add_btn.on_click = add_handler
        
        row.controls.append(remove_btn)
        row.controls.append(add_btn)
        
        # Сохраняем данные
        subchannels_data.append({
            "name_field": name_field,
            "platforms": platforms,
            "platforms_container": platforms_container,
            "row": row,
        })
        
        subchannels_container.controls.append(row)
        
        # Добавляем первую площадку по умолчанию
        add_platform_to_subchannel(subchannel_index, "Яндекс - Баннеры")
        
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
        
        row = ft.Row([text_field], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        remove_btn = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE,
            icon_color=AppColors.ERROR,
            icon_size=24,
            tooltip="Удалить креатив",
        )
        add_btn = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=AppColors.SUCCESS,
            icon_size=24,
            tooltip="Добавить креатив",
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
    add_subchannel_field("5_Context_Media")
    add_creative_field("creative")
    
    def create_structure(e):
        """Создаёт структуру папок внутри publish"""
        # Проверяем, выбрана ли рабочая папка
        if not selected_path_ref[0]:
            log_func("Сначала выберите рабочую папку с проектом или создайте проект!")
            return
        
        project_name = project_name_field.value.strip()
        if not project_name:
            log_func("Введите название проекта!")
            return
        
        # Собираем подканалы и площадки
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
        
        # Собираем креативы
        creatives = []
        for field in creative_fields:
            val = field.value.strip()
            if val:
                creatives.append(val)
        
        if not creatives:
            log_func("Добавьте хотя бы одно название креатива!")
            return
        
        try:
            # Путь к папке publish
            publish_path = os.path.join(selected_path_ref[0], "publish", project_name)
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
    
    subchannels_card = ft.Container(
        content=ft.Column([
            ft.Text("Подканалы и площадки", size=AppSizes.FONT_SIZE_MEDIUM, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
            ft.Container(height=AppSizes.PADDING_MEDIUM),
            subchannels_container,
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
            subchannels_card,
            creatives_card,
            create_btn,
        ],
        spacing=AppSizes.PADDING_MEDIUM,
        expand=True,
    )
    
    return content