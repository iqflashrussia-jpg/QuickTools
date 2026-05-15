"""
Главный вид приложения с вкладками.
"""

import flet as ft
import os
import tkinter as tk
from tkinter import filedialog

from ui.styles import AppColors, AppSizes
from ui.widgets.progress_widget import ProgressWidget
from ui.widgets.log_view import LogView
from ui.components import make_button

# Импортируем все блоки
from ui.blocks import (
    create_project_block,
    publish_block,
    archiver_block,
    fla_operations_block,
    rename_operations_block,
)


class MainView:
    """
    Главный вид приложения с вкладками.
    """
    
    def __init__(self, page: ft.Page, selected_path_ref, is_working_ref, log_func):
        self.page = page
        self.selected_path_ref = selected_path_ref
        self.is_working_ref = is_working_ref
        self.log_func = log_func
        self.tabs = None
        self.tab_contents = {}
        
        # Настройка страницы
        self._setup_page()
        
        # Создание UI
        self._build_ui()
    
    def _setup_page(self):
        """Настройка параметров страницы"""
        self.page.title = "QuickTools"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = AppSizes.PADDING_LARGE
        self.page.bgcolor = AppColors.BG_MAIN
        self.page.window.width = AppSizes.WINDOW_WIDTH
        self.page.window.height = AppSizes.WINDOW_HEIGHT
        self.page.window.min_width = AppSizes.WINDOW_MIN_WIDTH
        self.page.window.min_height = AppSizes.WINDOW_MIN_HEIGHT
        self.page.window.resizable = True
        self.page.update()
    
    def _pick_folder(self, e):
        """Открывает диалог выбора папки"""
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_selected = filedialog.askdirectory(title="Выберите рабочую папку")
        root.destroy()
        
        if folder_selected:
            self.selected_path_ref[0] = folder_selected
            self._update_folder_display()
            self.log_func(f"Выбрана папка: {self.selected_path_ref[0]}")
        else:
            self.log_func("Выбор папки отменён")
    
    def _update_folder_display(self):
        """Обновляет отображение выбранной папки"""
        if self.selected_path_ref[0]:
            self.folder_text.value = os.path.basename(self.selected_path_ref[0])
            self.folder_text.color = AppColors.PRIMARY
        else:
            self.folder_text.value = "Папка не выбрана"
            self.folder_text.color = AppColors.TEXT_SECONDARY
        self.page.update()
    
    def _get_folder_update_callback(self):
        """Возвращает callback для обновления отображения папки"""
        return self._update_folder_display
    
    def _get_tabs(self):
        """Создаёт и возвращает компонент вкладок (совместимый со старой версией Flet)"""
        # Используем Row с кнопками вместо Tabs для совместимости
        tab_buttons = ft.Row(spacing=0)
        self.tab_content = ft.Column(expand=True)
        
        # Список вкладок
        tabs_list = [
            ("Создание проекта", self._create_tab_create_project),
            ("Публикация", self._create_tab_publish),
            ("Оптимизация", self._create_tab_archiver),
            ("Архивация", self._create_tab_archiver),
            ("FLA операции", self._create_tab_fla),
            ("Переименование", self._create_tab_rename),
        ]
        
        def make_tab_button(text, index, create_func):
            btn = ft.Container(
                content=ft.Text(text, size=AppSizes.FONT_SIZE_MEDIUM, color=AppColors.TEXT_SECONDARY),
                padding=ft.Padding(left=15, top=10, right=15, bottom=10),
                bgcolor=AppColors.BG_CARD,
                border_radius=ft.BorderRadius(
                    top_left=AppSizes.BORDER_RADIUS_SMALL,
                    top_right=AppSizes.BORDER_RADIUS_SMALL,
                    bottom_left=0,
                    bottom_right=0,
                ),
                ink=True,
                on_click=lambda e, idx=index, func=create_func: self._select_tab(idx, func),
            )
            return btn
        
        for i, (name, create_func) in enumerate(tabs_list):
            btn = make_tab_button(name, i, create_func)
            tab_buttons.controls.append(btn)
        
        # Контейнер для вкладок
        tabs_container = ft.Container(
            content=ft.Column([
                tab_buttons,
                ft.Divider(height=1, color=AppColors.BORDER),
                self.tab_content,
            ], spacing=0),
            expand=True,
        )
        
        return tabs_container
    
    def _select_tab(self, index, create_func):
        """Переключает вкладку"""
        # Очищаем содержимое
        self.tab_content.controls.clear()
        # Создаём новое содержимое
        content = create_func()
        self.tab_content.controls.append(content)
        self.page.update()
    
    def _create_tab_create_project(self):
        """Создаёт содержимое вкладки 'Создание проекта'"""
        return create_project_block(
            self.log_func,
            self.selected_path_ref,
            self.is_working_ref,
            self.page,
            self.progress_widget,
            self._get_folder_update_callback()
        )
    
    def _create_tab_publish(self):
        """Создаёт содержимое вкладки 'Публикация'"""
        return publish_block(
            self.log_func,
            self.selected_path_ref,
            self.page,
            self.progress_widget
        )
    
    def _create_tab_archiver(self):
        """Создаёт содержимое вкладки 'Оптимизация/Архивация'"""
        return archiver_block()
    
    def _create_tab_fla(self):
        """Создаёт содержимое вкладки 'FLA операции'"""
        return fla_operations_block(
            self.log_func,
            self.selected_path_ref,
            self.is_working_ref,
            self.page,
            self.progress_widget
        )
    
    def _create_tab_rename(self):
        """Создаёт содержимое вкладки 'Переименование'"""
        return rename_operations_block(
            self.log_func,
            self.selected_path_ref,
            self.is_working_ref,
            self.page,
            self.progress_widget
        )
    
    def _build_ui(self):
        """Собирает основной интерфейс"""
        
        # === ВЕРХНЯЯ ПАНЕЛЬ (выбор папки) ===
        self.folder_text = ft.Text(
            value="Папка не выбрана",
            size=AppSizes.FONT_SIZE_MEDIUM,
            color=AppColors.TEXT_SECONDARY,
        )
        
        top_panel = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Рабочая папка:", size=AppSizes.FONT_SIZE_MEDIUM, color=AppColors.TEXT_SECONDARY),
                    ft.Container(
                        content=self.folder_text,
                        expand=True,
                        height=35,
                        padding=ft.Padding(left=10, top=0, right=10, bottom=0),
                        bgcolor=AppColors.BG_INPUT,
                        border_radius=AppSizes.BORDER_RADIUS_SMALL,
                        border=ft.border.all(1, AppColors.BORDER),
                    ),
                    make_button("Выбрать", self._pick_folder, AppColors.PRIMARY, expand=False, height=35),
                ],
                spacing=AppSizes.PADDING_MEDIUM,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(
                left=AppSizes.PADDING_MEDIUM,
                top=AppSizes.PADDING_SMALL,
                right=AppSizes.PADDING_MEDIUM,
                bottom=AppSizes.PADDING_SMALL,
            ),
            bgcolor=AppColors.BG_CARD,
            border_radius=AppSizes.BORDER_RADIUS_MEDIUM,
        )
        
        # === ПРОГРЕСС-БАР ===
        self.progress_widget = ProgressWidget()
        
        # === ЛОГ ===
        self.log_view = LogView()
        self.log_view.attach_page(self.page)
        
        # Сохраняем оригинальную log_func для перенаправления
        self._original_log_func = self.log_func
        
        # Переопределяем log_func для записи в виджет лога
        def new_log_func(message):
            self._original_log_func(message)
            self.log_view.add_message(message, self.page)
        
        self.log_func = new_log_func
        
        # === ВКЛАДКИ ===
        tabs_widget = self._get_tabs()
        
        # === СБОРКА ===
        main_container = ft.Column(
            [
                top_panel,
                ft.Container(height=AppSizes.PADDING_MEDIUM),
                tabs_widget,
                ft.Container(height=AppSizes.PADDING_MEDIUM),
                self.progress_widget,
                self.log_view,
            ],
            spacing=0,
            expand=True,
        )
        
        self.page.add(main_container)
        
        # Активируем первую вкладку
        self._select_tab(0, self._create_tab_create_project)
        
        # Обновляем отображение папки
        self._update_folder_display()
    
    def get_log(self):
        """Возвращает объект лога"""
        return self.log_view


def create_main_view(page: ft.Page, selected_path_ref, is_working_ref, log_func):
    """
    Создаёт главный вид приложения.
    
    Returns:
        LogView: объект лога для добавления сообщений из main.py
    """
    main_view = MainView(page, selected_path_ref, is_working_ref, log_func)
    return main_view.get_log()