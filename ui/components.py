"""
Базовые компоненты интерфейса.
Используют стили из styles.py для единообразия дизайна.
"""

import flet as ft
from ui.styles import AppColors, AppSizes, AppTextStyles, get_input_style, get_button_style


def make_button(text, on_click, bgcolor=None, expand=False, height=None):
    """
    Создаёт кнопку с единым стилем.
    
    Args:
        text: Текст кнопки
        on_click: Функция-обработчик
        bgcolor: Цвет фона (по умолчанию AppColors.PRIMARY)
        expand: Растягивать ли кнопку по ширине
        height: Высота кнопки (по умолчанию AppSizes.BUTTON_HEIGHT)
    """
    return ft.Container(
        content=ft.Text(
            text, 
            size=AppTextStyles.BUTTON["size"], 
            weight=AppTextStyles.BUTTON["weight"],
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=bgcolor if bgcolor else AppColors.PRIMARY,
        border_radius=AppSizes.BORDER_RADIUS_SMALL,
        padding=ft.Padding(
            left=AppSizes.PADDING_MEDIUM,
            top=AppSizes.PADDING_SMALL,
            right=AppSizes.PADDING_MEDIUM,
            bottom=AppSizes.PADDING_SMALL,
        ),
        ink=True,
        on_click=on_click,
        expand=expand,
        height=height or AppSizes.BUTTON_HEIGHT,
    )


def make_outlined_button(text, on_click, bgcolor=None, color=None, expand=False, height=None):
    """
    Создаёт кнопку с обводкой.
    
    Args:
        text: Текст кнопки
        on_click: Функция-обработчик
        bgcolor: Цвет фона
        color: Цвет текста (по умолчанию AppColors.PRIMARY)
        expand: Растягивать ли кнопку по ширине
        height: Высота кнопки
    """
    return ft.Container(
        content=ft.Text(
            text,
            size=AppTextStyles.BUTTON["size"],
            weight=AppTextStyles.BUTTON["weight"],
            color=color or AppColors.PRIMARY,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=bgcolor if bgcolor else AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_SMALL,
        border=ft.border.all(1, AppColors.BORDER),
        padding=ft.Padding(
            left=AppSizes.PADDING_MEDIUM,
            top=AppSizes.PADDING_SMALL,
            right=AppSizes.PADDING_MEDIUM,
            bottom=AppSizes.PADDING_SMALL,
        ),
        ink=True,
        on_click=on_click,
        expand=expand,
        height=height or AppSizes.BUTTON_HEIGHT,
    )


def make_text_field(value="", hint_text="", width=None, expand=False, multiline=False, min_lines=1, max_lines=10):
    """
    Создаёт текстовое поле с единым стилем.
    
    Args:
        value: Значение по умолчанию
        hint_text: Текст-подсказка
        width: Ширина поля
        expand: Растягивать ли по ширине
        multiline: Многострочный режим
        min_lines: Минимальное количество строк
        max_lines: Максимальное количество строк
    """
    return ft.TextField(
        value=value,
        hint_text=hint_text,
        width=width,
        expand=expand,
        multiline=multiline,
        min_lines=min_lines,
        max_lines=max_lines,
        **get_input_style(),
    )


def make_card(content, padding=None, margin=None):
    """
    Создаёт карточку-контейнер с тенью.
    
    Args:
        content: Содержимое карточки
        padding: Внутренние отступы
        margin: Внешние отступы
    """
    return ft.Container(
        content=content,
        bgcolor=AppColors.BG_CARD,
        border_radius=AppSizes.BORDER_RADIUS_MEDIUM,
        padding=padding or AppSizes.PADDING_MEDIUM,
        margin=margin or 0,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=AppColors.SHADOW_LIGHT,
            offset=ft.Offset(0, 2),
        ),
    )


def make_section_title(title):
    """
    Создаёт заголовок секции.
    
    Args:
        title: Текст заголовка
    """
    return ft.Text(
        title,
        size=AppTextStyles.HEADING["size"],
        weight=AppTextStyles.HEADING["weight"],
        color=AppColors.TEXT_PRIMARY,
    )