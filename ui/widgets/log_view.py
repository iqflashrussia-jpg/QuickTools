"""
Виджет сворачиваемого лога операций с возможностью копирования и очистки.
"""

import flet as ft
from ui.styles import AppColors, AppSizes, AppTextStyles


class LogView(ft.Container):
    """
    Сворачиваемый виджет лога операций.
    
    Состоит из заголовка с иконкой разворота и текстового поля
    с прокруткой для отображения сообщений.
    """
    
    def __init__(self):
        super().__init__()
        
        self._is_expanded = True
        self._messages = []
        self._page = None
        
        # Текстовое поле для отображения лога
        self.log_field = ft.TextField(
            multiline=True,
            min_lines=5,
            max_lines=12,
            read_only=True,
            value="Готов к работе...\n",
            text_size=AppSizes.FONT_SIZE_SMALL,
            bgcolor=AppColors.BG_INPUT,
            border_color=AppColors.BORDER,
            color=AppColors.TEXT_PRIMARY,
            border_radius=AppSizes.BORDER_RADIUS_SMALL,
        )
        
        # Иконка для сворачивания/разворачивания
        self.expand_icon = ft.IconButton(
            icon=ft.Icons.KEYBOARD_ARROW_DOWN,
            icon_color=AppColors.TEXT_SECONDARY,
            icon_size=18,
            tooltip="Свернуть лог",
            on_click=self._toggle_expand,
        )
        
        # Кнопка очистки лога
        self.clear_btn = ft.IconButton(
            icon=ft.Icons.CLEAR_ALL,
            icon_color=AppColors.TEXT_SECONDARY,
            icon_size=18,
            tooltip="Очистить лог",
            on_click=self._clear_log,
        )
        
        # Кнопка копирования лога
        self.copy_btn = ft.IconButton(
            icon=ft.Icons.CONTENT_COPY,
            icon_color=AppColors.TEXT_SECONDARY,
            icon_size=18,
            tooltip="Копировать лог",
            on_click=self._copy_log,
        )
        
        # Заголовок лога
        self.title_text = ft.Text(
            "Лог операций",
            size=AppTextStyles.SMALL["size"],
            color=AppColors.TEXT_SECONDARY,
        )
        
        # Верхняя панель с заголовком и кнопками
        self.header = ft.Row(
            [
                ft.Container(width=AppSizes.PADDING_SMALL),
                self.expand_icon,
                ft.Container(width=AppSizes.PADDING_TINY),
                self.title_text,
                ft.Container(expand=True),
                self.copy_btn,
                ft.Container(width=AppSizes.PADDING_TINY),
                self.clear_btn,
                ft.Container(width=AppSizes.PADDING_SMALL),
            ],
            spacing=0,
            height=AppSizes.LOG_PANEL_COLLAPSED_HEIGHT,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Основное содержимое лога
        self.content_column = ft.Column(
            [self.header, self.log_field],
            spacing=AppSizes.PADDING_SMALL,
            expand=True,
        )
        
        self.content = self.content_column
        self.bgcolor = AppColors.BG_CARD
        self.border_radius = AppSizes.BORDER_RADIUS_MEDIUM
        self.padding = ft.Padding(
            left=0,
            top=AppSizes.PADDING_TINY,
            right=0,
            bottom=AppSizes.PADDING_TINY,
        )
        
        # Устанавливаем начальную высоту
        self._update_height()
    
    def _update_height(self):
        """Обновляет высоту виджета в зависимости от состояния"""
        if self._is_expanded:
            self.height = AppSizes.LOG_PANEL_HEIGHT
            self.expand_icon.icon = ft.Icons.KEYBOARD_ARROW_DOWN
            self.expand_icon.tooltip = "Свернуть лог"
            self.log_field.visible = True
        else:
            self.height = AppSizes.LOG_PANEL_COLLAPSED_HEIGHT
            self.expand_icon.icon = ft.Icons.KEYBOARD_ARROW_UP
            self.expand_icon.tooltip = "Развернуть лог"
            self.log_field.visible = False
    
    def _toggle_expand(self, e):
        """Переключает состояние развёрнутости лога"""
        self._is_expanded = not self._is_expanded
        self._update_height()
        if self._page:
            self._page.update()
    
    def _clear_log(self, e):
        """Очищает лог"""
        self._messages = []
        self.log_field.value = "Лог очищен\n"
        if self._page:
            self._page.update()
    
    def _copy_log(self, e):
        """Копирует содержимое лога в буфер обмена"""
        if self._page:
            self._page.set_clipboard(self.log_field.value)
            print("Лог скопирован в буфер обмена")
    
    def add_message(self, message, page):
        """
        Добавляет сообщение в лог.
        
        Args:
            message: Текст сообщения
            page: Страница Flet для обновления
        """
        import time
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self._messages.append(formatted_message)
        
        # Ограничиваем количество сообщений (последние 500)
        if len(self._messages) > 500:
            self._messages = self._messages[-400:]
        
        self.log_field.value = ''.join(self._messages[-400:])
        
        # Автопрокрутка вниз (установка курсора в конец)
        self.log_field.focus()
        page.update()
    
    def attach_page(self, page):
        """Сохраняет ссылку на страницу для последующих обновлений"""
        self._page = page