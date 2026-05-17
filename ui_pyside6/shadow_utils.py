# ui_pyside6/shadow_utils.py
"""
Утилита для добавления теней виджетам
Все параметры теней управляются из styles.py
"""

from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

# Импортируем настройки теней из styles.py
try:
    from ui_pyside6.styles import SHADOWS, COLORS
    SHADOWS_AVAILABLE = True
except ImportError:
    SHADOWS_AVAILABLE = False
    SHADOWS = {}
    COLORS = {}


def add_shadow(widget, blur=15, offset_x=0, offset_y=4, opacity=80):
    """
    Добавляет мягкую тень виджету
    
    Аргументы:
        widget: виджет, к которому применяется тень
        blur: размытие (пиксели)
        offset_x: смещение по X
        offset_y: смещение по Y
        opacity: прозрачность (0-255, 0 = прозрачная, 255 = непрозрачная)
    """
    if not widget:
        return
    
    # Очищаем старые эффекты, если есть
    old_effect = widget.graphicsEffect()
    if old_effect:
        old_effect.deleteLater()
    
    # Создаём эффект тени
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(offset_x)
    shadow.setYOffset(offset_y)
    
    # Парсим цвет из COLORS
    color_rgb = COLORS.get("shadow_color", "0, 0, 0")
    try:
        rgb_parts = color_rgb.split(',')
        r = int(rgb_parts[0].strip())
        g = int(rgb_parts[1].strip())
        b = int(rgb_parts[2].strip())
        shadow.setColor(QColor(r, g, b, opacity))
    except:
        shadow.setColor(QColor(0, 0, 0, opacity))
    
    widget.setGraphicsEffect(shadow)


def add_card_shadow(widget):
    """Добавляет тень для карточки (основной блок)"""
    if not SHADOWS_AVAILABLE:
        add_shadow(widget, blur=15, offset_y=4, opacity=80)
        return
    
    shadow = SHADOWS.get("card", {})
    add_shadow(
        widget,
        blur=shadow.get("blur", 15),
        offset_x=shadow.get("offset_x", 0),
        offset_y=shadow.get("offset_y", 4),
        opacity=shadow.get("opacity", COLORS.get("shadow_opacity", 80))
    )


def add_subchannel_shadow(widget):
    """Добавляет тень для карточки подканала"""
    if not SHADOWS_AVAILABLE:
        add_shadow(widget, blur=10, offset_y=2, opacity=60)
        return
    
    shadow = SHADOWS.get("subchannel", {})
    add_shadow(
        widget,
        blur=shadow.get("blur", 10),
        offset_x=shadow.get("offset_x", 0),
        offset_y=shadow.get("offset_y", 2),
        opacity=shadow.get("opacity", COLORS.get("shadow_opacity", 80))
    )