"""
Базовый класс для всех блоков интерфейса.
"""

import flet as ft
from ui.styles import AppColors, AppSizes, AppTextStyles
from ui.components import make_card, make_section_title


class BaseBlock:
    """
    Базовый класс для блока интерфейса.
    Предоставляет общие методы для создания карточек, секций и т.д.
    """
    
    def __init__(self, log_func, selected_path_ref, is_working_ref, page, progress_widget=None):
        self.log_func = log_func
        self.selected_path_ref = selected_path_ref
        self.is_working_ref = is_working_ref
        self._page = page
        self.progress_widget = progress_widget
    
    def make_card(self, title, content):
        """Создаёт карточку с заголовком и содержимым"""
        return make_card(
            ft.Column([
                make_section_title(title),
                ft.Container(height=AppSizes.PADDING_MEDIUM),
                content,
            ], spacing=0),
            padding=AppSizes.PADDING_MEDIUM,
        )
    
    def make_section(self, title, controls):
        """Создаёт секцию с заголовком и элементами"""
        return ft.Column([
            ft.Text(title, size=AppTextStyles.SUBHEADING["size"], weight=AppTextStyles.SUBHEADING["weight"]),
            ft.Container(height=AppSizes.PADDING_SMALL),
            *controls,
        ], spacing=0)
    
    def log(self, message):
        """Добавляет сообщение в лог"""
        self.log_func(message)
    
    def update_progress(self, value, text, visible=True):
        """Обновляет прогресс-бар"""
        if self.progress_widget:
            self.progress_widget.update_progress(value, text, self._page, visible)
    
    def hide_progress(self):
        """Скрывает прогресс-бар"""
        if self.progress_widget:
            self.progress_widget.hide(self._page)
    
    def is_working(self):
        """Проверяет, выполняется ли операция"""
        return self.is_working_ref[0]
    
    def set_working(self, value):
        """Устанавливает флаг выполнения операции"""
        self.is_working_ref[0] = value