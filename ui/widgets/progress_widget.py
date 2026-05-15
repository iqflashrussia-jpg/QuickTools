"""
Виджет прогресс-бара с текстовым индикатором.
"""

import flet as ft
from ui.styles import AppColors, AppSizes, AppTextStyles


class ProgressWidget(ft.Column):
    """
    Виджет прогресс-бара.
    
    Состоит из горизонтальной полосы прогресса и текстового поля
    с информацией о текущей операции.
    
    Пример использования:
        progress = ProgressWidget()
        progress.update_progress(0.5, "Обработка файла 5/10", page)
    """
    
    def __init__(self):
        super().__init__(spacing=AppSizes.PADDING_SMALL, visible=False)
        
        # Полоса прогресса
        self.progress_bar = ft.ProgressBar(
            width=None,
            height=6,
            color=AppColors.SUCCESS,
            bgcolor=AppColors.BORDER,
            value=0,
        )
        
        # Текстовый индикатор
        self.progress_text = ft.Text(
            value="",
            size=AppTextStyles.SMALL["size"],
            color=AppColors.TEXT_SECONDARY,
        )
        
        self.controls = [self.progress_bar, self.progress_text]
    
    def update_progress(self, value, text, page, visible=True):
        """
        Обновляет состояние прогресс-бара.
        
        Args:
            value: Значение прогресса (0.0 - 1.0)
            text: Текст, описывающий текущую операцию
            page: Страница Flet для обновления
            visible: Видимость виджета
        """
        self.progress_bar.value = value
        self.progress_text.value = text
        self.visible = visible
        page.update()
    
    def hide(self, page):
        """Скрывает виджет прогресс-бара"""
        self.visible = False
        page.update()
    
    def show(self, page, text="Подготовка..."):
        """Показывает виджет прогресс-бара с начальным состоянием"""
        self.visible = True
        self.progress_bar.value = 0
        self.progress_text.value = text
        page.update()