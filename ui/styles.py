"""
Модуль стилей приложения.
Здесь определяются все цвета, размеры, отступы и стили текста.
Изменяя значения в этом файле, можно легко менять внешний вид всего приложения.
"""

import flet as ft

class AppColors:
    """Цветовая схема приложения"""
    
    # Основные цвета
    PRIMARY = "#4a90d9"
    SUCCESS = "#6b8c5c"
    ERROR = "#c65d5d"
    WARNING = "#d4a55e"
    
    # Фоновые цвета
    BG_MAIN = "#1e1e1e"
    BG_CARD = "#2d2d2d"
    BG_INPUT = "#252525"
    BG_HOVER = "#353535"
    
    # Текст
    TEXT_PRIMARY = "#e0e0e0"
    TEXT_SECONDARY = "#a0a0a0"
    TEXT_HINT = "#707070"
    TEXT_DISABLED = "#505050"
    
    # Границы
    BORDER = "#3d3d3d"
    BORDER_FOCUS = "#4a90d9"
    BORDER_ERROR = "#c65d5d"
    
    # Тени
    SHADOW_LIGHT = "#0000001a"
    SHADOW_MEDIUM = "#00000033"
    SHADOW_DARK = "#0000004d"
    
    # Акцентные цвета
    ACCENT_SUCCESS = "#8bc34a"
    ACCENT_ERROR = "#ef5350"
    ACCENT_WARNING = "#ffb74d"
    ACCENT_INFO = "#64b5f6"


class AppSizes:
    """Размеры элементов интерфейса"""
    
    # Размеры окна
    WINDOW_WIDTH = 1050
    WINDOW_HEIGHT = 750
    WINDOW_MIN_WIDTH = 900
    WINDOW_MIN_HEIGHT = 600
    
    # Панели
    TOP_PANEL_HEIGHT = 60
    TAB_PANEL_HEIGHT = 45
    PROGRESS_PANEL_HEIGHT = 60
    LOG_PANEL_HEIGHT = 150
    LOG_PANEL_COLLAPSED_HEIGHT = 35
    
    # Ширина левой панели (для вкладок, которые используют вертикальную структуру)
    LEFT_PANEL_WIDTH = 480
    
    # Поля ввода
    INPUT_HEIGHT = 40
    INPUT_WIDTH_SMALL = 120
    INPUT_WIDTH_MEDIUM = 200
    INPUT_WIDTH_LARGE = 250
    INPUT_WIDTH_FULL = 400
    
    # Кнопки
    BUTTON_HEIGHT = 40
    BUTTON_HEIGHT_LARGE = 45
    BUTTON_WIDTH_SMALL = 80
    BUTTON_WIDTH_MEDIUM = 120
    BUTTON_WIDTH_LARGE = 200
    
    # Отступы
    PADDING_TINY = 4
    PADDING_SMALL = 8
    PADDING_MEDIUM = 12
    PADDING_LARGE = 16
    PADDING_XLARGE = 25
    
    # Скругления
    BORDER_RADIUS_TINY = 4
    BORDER_RADIUS_SMALL = 6
    BORDER_RADIUS_MEDIUM = 8
    BORDER_RADIUS_LARGE = 10
    BORDER_RADIUS_XLARGE = 15
    
    # Шрифты
    FONT_SIZE_TINY = 10
    FONT_SIZE_SMALL = 11
    FONT_SIZE_MEDIUM = 12
    FONT_SIZE_LARGE = 13
    FONT_SIZE_XLARGE = 14
    FONT_SIZE_XXLARGE = 16
    FONT_SIZE_TITLE = 20


class AppTextStyles:
    """Стили текста"""
    
    TITLE = {"size": AppSizes.FONT_SIZE_TITLE, "weight": ft.FontWeight.BOLD}
    HEADING = {"size": AppSizes.FONT_SIZE_MEDIUM, "weight": ft.FontWeight.BOLD}
    SUBHEADING = {"size": AppSizes.FONT_SIZE_LARGE, "weight": ft.FontWeight.W_500}
    BODY = {"size": AppSizes.FONT_SIZE_LARGE}
    BODY_BOLD = {"size": AppSizes.FONT_SIZE_LARGE, "weight": ft.FontWeight.W_500}
    SMALL = {"size": AppSizes.FONT_SIZE_SMALL}
    SMALL_BOLD = {"size": AppSizes.FONT_SIZE_SMALL, "weight": ft.FontWeight.W_500}
    HINT = {"size": AppSizes.FONT_SIZE_MEDIUM}
    BUTTON = {"size": AppSizes.FONT_SIZE_LARGE, "weight": ft.FontWeight.W_500}


def get_container_style(bgcolor=None, border_radius=None, padding=None, shadow=False):
    """Возвращает стиль контейнера"""
    style = {}
    if bgcolor:
        style["bgcolor"] = bgcolor
    if border_radius:
        style["border_radius"] = border_radius
    if padding:
        style["padding"] = padding
    if shadow:
        style["shadow"] = ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=AppColors.SHADOW_MEDIUM,
            offset=ft.Offset(0, 2),
        )
    return style


def get_input_style():
    """Возвращает стиль для текстовых полей ввода"""
    return {
        "text_size": AppSizes.FONT_SIZE_LARGE,
        "bgcolor": AppColors.BG_INPUT,
        "border_color": AppColors.BORDER,
        "color": AppColors.TEXT_PRIMARY,
        "border_radius": AppSizes.BORDER_RADIUS_SMALL,
    }


def get_button_style(bgcolor=None, text_color=ft.Colors.WHITE):
    """Возвращает стиль для кнопок"""
    style = ft.ButtonStyle(
        color=text_color,
        bgcolor=bgcolor or AppColors.PRIMARY,
        padding=ft.Padding(
            left=AppSizes.PADDING_MEDIUM,
            top=AppSizes.PADDING_SMALL,
            right=AppSizes.PADDING_MEDIUM,
            bottom=AppSizes.PADDING_SMALL,
        ),
        shape=ft.RoundedRectangleBorder(radius=AppSizes.BORDER_RADIUS_SMALL),
    )
    return style