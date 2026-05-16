"""
Стартовая страница приложения.
"""

import flet as ft
import tkinter as tk
from tkinter import filedialog
import os

from ui.styles import AppColors, AppSizes
from ui.components import make_button


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
    
    def on_open_project(e):
        """Открывает существующий проект"""
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_selected = filedialog.askdirectory(title="Выберите папку проекта")
        root.destroy()
        
        if folder_selected:
            selected_path_ref[0] = folder_selected
            log_func(f"📂 Открыт проект: {folder_selected}")
            on_project_loaded(show_create_tab=False)
        else:
            status_text.value = "Выбор папки отменён"
            page.update()
    
    # Собираем карточку
    card = ft.Container(
        content=ft.Column([
            ft.Text("QuickTools", size=AppSizes.FONT_SIZE_TITLE, weight=ft.FontWeight.BOLD, color=AppColors.PRIMARY),
            ft.Text("Инструменты для работы с проектами", size=AppSizes.FONT_SIZE_MEDIUM, color=AppColors.TEXT_SECONDARY),
            ft.Container(height=AppSizes.PADDING_LARGE),
            
            ft.Row([
                make_button("Создать проект", on_create_project, AppColors.SUCCESS, expand=True),
                make_button("Открыть проект", on_open_project, AppColors.PRIMARY, expand=True),
            ], spacing=AppSizes.PADDING_MEDIUM),
            
            ft.Container(height=AppSizes.PADDING_SMALL),
            status_text,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_LARGE,
        padding=AppSizes.PADDING_XLARGE,
        width=500,
    )
    
    # Простой контейнер без центрирования
    container = ft.Container(
        content=card,
        expand=True,
    )
    
    return container