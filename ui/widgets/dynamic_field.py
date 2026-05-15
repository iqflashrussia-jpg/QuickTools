"""
Виджет динамического поля с кнопками добавления и удаления.
Используется для создания списков полей (площадки, креативы, подканалы и т.д.).
"""

import flet as ft
from ui.styles import AppColors, AppSizes, AppTextStyles, get_input_style


class DynamicField(ft.Container):
    """
    Поле ввода с кнопками + и -.
    
    Пример использования:
        def on_add():
            # добавить новое поле
            pass
        
        def on_remove(field):
            # удалить поле
            pass
        
        field = DynamicField(
            value="Master",
            hint_text="Название площадки",
            on_add=on_add,
            on_remove=on_remove,
        )
    """
    
    def __init__(self, value="", hint_text="", on_add=None, on_remove=None, width=None):
        super().__init__()
        self.value = value
        self.hint_text = hint_text
        self.on_add_callback = on_add
        self.on_remove_callback = on_remove
        self.width = width
        
        # Создаём текстовое поле
        self.text_field = ft.TextField(
            value=value,
            hint_text=hint_text,
            width=width,
            expand=(width is None),
            height=AppSizes.INPUT_HEIGHT,
            text_size=AppSizes.FONT_SIZE_LARGE,
            bgcolor=AppColors.BG_INPUT,
            border_color=AppColors.BORDER,
            color=AppColors.TEXT_PRIMARY,
            border_radius=AppSizes.BORDER_RADIUS_SMALL,
        )
        
        # Кнопка удаления
        self.remove_btn = ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE,
            icon_color=AppColors.ERROR,
            icon_size=24,
            tooltip="Удалить",
            on_click=self._on_remove,
        )
        
        # Кнопка добавления
        self.add_btn = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=AppColors.SUCCESS,
            icon_size=24,
            tooltip="Добавить",
            on_click=self._on_add,
        )
        
        # Строка с полем и кнопками
        self.row = ft.Row(
            [self.text_field, self.remove_btn, self.add_btn],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        self.content = self.row
    
    def _on_add(self, e):
        """Обработчик кнопки добавления"""
        if self.on_add_callback:
            self.on_add_callback()
    
    def _on_remove(self, e):
        """Обработчик кнопки удаления"""
        if self.on_remove_callback:
            self.on_remove_callback(self)
    
    def get_value(self):
        """Возвращает значение текстового поля"""
        return self.text_field.value.strip() if self.text_field.value else ""
    
    def set_value(self, value):
        """Устанавливает значение текстового поля"""
        self.text_field.value = value