"""
Утилита для работы с иконками Tabler
"""

from PySide6.QtWidgets import QPushButton, QTabWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

try:
    # Правильный импорт из документации: имя пакета 'tablerqicon', класс 'TablerQIcon'
    from tablerqicon import TablerQIcon
    TABLER_AVAILABLE = True
    print("✅ TablerQIcon загружен успешно")
except ImportError as e:
    TABLER_AVAILABLE = False
    print(f"⚠️ tablerqicon не найден. Ошибка: {e}")
    print("Установите: pip install tabler-qicon")


def get_icon(icon_name, color=None, size=24, stroke_width=2):
    """
    Возвращает иконку Tabler
    
    Аргументы:
        icon_name: название иконки (например, 'plus', 'minus', 'folder')
        color: цвет иконки (опционально, по умолчанию None - используется тема)
        size: размер иконки в пикселях
        stroke_width: толщина линии
    """
    if not TABLER_AVAILABLE:
        return QIcon()
    
    try:
        # Создаём экземпляр с настройками
        if color:
            tabler_icon = TablerQIcon(color=color, size=size, stroke_width=stroke_width)
        else:
            tabler_icon = TablerQIcon(size=size, stroke_width=stroke_width)
        
        # Получаем иконку по имени
        icon = getattr(tabler_icon, icon_name, None)
        if icon is None:
            # Пробуем вариант с преобразованием имени
            icon_name_fixed = icon_name.replace('-', '_')
            icon = getattr(tabler_icon, icon_name_fixed, None)
        
        return icon if icon else QIcon()
    except Exception as e:
        print(f"⚠️ Ошибка получения иконки {icon_name}: {e}")
        return QIcon()


def set_icon(button, icon_name, size=18, color=None):
    """Устанавливает иконку на кнопку"""
    icon = get_icon(icon_name, color=color, size=size)
    if icon and not icon.isNull():
        button.setIcon(icon)
        button.setIconSize(QSize(size, size))


def set_icon_with_text(button, icon_name, text, size=18, color=None):
    """Устанавливает иконку и текст на кнопку"""
    set_icon(button, icon_name, size, color)
    button.setText(f"  {text}")


def set_tab_icon(tab_widget, index, icon_name, size=16, color='#ffffff'):
    """Устанавливает иконку на вкладку"""
    print(f"Устанавливаю иконку {icon_name} на вкладку {index}")  # Отладка
    icon = get_icon(icon_name, color=color, size=size)
    if icon and not icon.isNull():
        tab_widget.setTabIcon(index, icon)
        tab_widget.setIconSize(QSize(size, size))
    else:
        print(f"⚠️ Иконка {icon_name} не загружена")


# Словарь соответствия функций и названий иконок
ICON_MAP = {
    'add': 'plus',           # плюс
    'remove': 'minus',       # минус
    'delete': 'trash',       # корзина
    'play': 'player-play',   # запуск
    'search': 'search',      # поиск
    'folder': 'folder',      # папка
    'folder_open': 'folder-open',  # открытая папка
    'settings': 'settings',  # настройки
    'archive': 'archive',    # архив
    'file': 'file',          # файл
    'fla': 'file-code',      # FLA (файл с кодом)
    'rename': 'edit',        # переименование
    'save': 'save',          # сохранить
    'cancel': 'x',           # отмена/закрыть
    'apply': 'check',        # применить/галочка
    'refresh': 'refresh',    # обновить
    'info': 'info-circle',   # информация
    'warning': 'alert-triangle',  # предупреждение
    'error': 'alert-circle',      # ошибка
    'project': 'briefcase',       # проект
    'publish': 'send',            # публикация
    'optimize': 'zap',            # оптимизация/молния
    'rename_icon': 'pencil',      # переименование/карандаш
}