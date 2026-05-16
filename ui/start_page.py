"""
Стартовая страница приложения.
"""

import flet as ft
import os
from ui.styles import AppColors, AppSizes
from ui.components import make_button
from ui.widgets.drag_drop_zone import DragDropZone


def create_start_page(page, selected_path_ref, log_func, on_project_loaded):
    """
    Создаёт стартовую страницу.
    
    Args:
        page: Страница Flet
        selected_path_ref: Ссылка на выбранную папку
        log_func: Функция логирования
        on_project_loaded: Callback после загрузки/создания проекта
    """
    
    status_text = ft.Text(
        value="",
        size=AppSizes.FONT_SIZE_SMALL,
        color=AppColors.TEXT_SECONDARY,
    )
    
    def on_create_project(e):
        """Создаёт новый проект - открывает вкладку Создание проекта"""
        on_project_loaded(show_create_tab=True)
    
    def on_drag_drop_project(project_path):
        """Обработчик выбора проекта через Drag&Drop или кнопку"""
        selected_path_ref[0] = project_path
        log_func(f"📂 Открыт проект: {project_path}")
        on_project_loaded(show_create_tab=False)
    
    # Создаем Drag & Drop зону
    drag_drop_zone = DragDropZone(
        on_project_selected=on_drag_drop_project,
        page=page
    )
    
    # Собираем карточку
    card = ft.Container(
        content=ft.Column([
            ft.Text("QuickTools", size=AppSizes.FONT_SIZE_TITLE, weight=ft.FontWeight.BOLD, color=AppColors.PRIMARY),
            ft.Text("Инструменты для работы с проектами", size=AppSizes.FONT_SIZE_MEDIUM, color=AppColors.TEXT_SECONDARY),
            ft.Container(height=AppSizes.PADDING_LARGE),
            
            # Drag & Drop зона
            drag_drop_zone,
            
            ft.Row([
                make_button("Создать проект", on_create_project, AppColors.SUCCESS, expand=True),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Container(height=AppSizes.PADDING_SMALL),
            status_text,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_LARGE,
        padding=AppSizes.PADDING_XLARGE,
        width=500,
    )
    
    container = ft.Container(
        content=card,
        expand=True,
    )
    
    return container