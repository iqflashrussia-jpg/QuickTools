# ui_pyside6/common_widgets.py
"""
ОБЩИЕ ВИДЖЕТЫ ДЛЯ ВСЕХ ВКЛАДОК
=================================
Здесь хранятся виджеты, которые переиспользуются в разных частях приложения.

Например:
- PlatformRow - строка с полем для площадки и кнопками +/-
- CreativeRow - строка с полем для креатива и кнопками +/-
"""

from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QWidget

from ui_pyside6.icons_utils import set_icon


class PlatformRow(QWidget):
    """
    Строка с полем для названия площадки.
    
    Используется в:
    - CreateProjectBlock (Создание проекта)
    - PublishBlock (Публикация)
    
    Как работает:
    - Кнопка "+" вызывает on_add (создаёт новую строку)
    - Кнопка "-" вызывает on_remove (удаляет эту строку)
    
    Параметры:
        value: str - начальное значение поля (по умолчанию "Master" или "Яндекс - Баннеры")
        on_add: function - вызывается при нажатии на "+"
        on_remove: function - вызывается при нажатии на "-"
    """
    
    def __init__(self, value="Master", on_add=None, on_remove=None):
        super().__init__()
        self.on_add = on_add
        self.on_remove = on_remove
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Текстовое поле для ввода названия площадки
        self.text_field = QLineEdit(value)
        self.text_field.setPlaceholderText("Название площадки")
        self.text_field.setMinimumHeight(32)
        layout.addWidget(self.text_field, 1)
        
        # Кнопка удаления (-)
        self.remove_btn = QPushButton()
        set_icon(self.remove_btn, 'minus', 16)
        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.setFixedSize(28, 28)
        self.remove_btn.clicked.connect(self._on_remove)
        layout.addWidget(self.remove_btn)
        
        # Кнопка добавления (+)
        self.add_btn = QPushButton()
        set_icon(self.add_btn, 'plus', 16)
        self.add_btn.setObjectName("add_btn")
        self.add_btn.setFixedSize(28, 28)
        self.add_btn.clicked.connect(self._on_add)
        layout.addWidget(self.add_btn)
    
    def _on_add(self):
        """Вызывается при нажатии на кнопку '+'"""
        if self.on_add:
            self.on_add()
    
    def _on_remove(self):
        """Вызывается при нажатии на кнопку '-'"""
        if self.on_remove:
            self.on_remove(self)
    
    def get_value(self):
        """Возвращает текст из поля ввода (без лишних пробелов)"""
        return self.text_field.text().strip()
    
    def set_value(self, value):
        """Устанавливает текст в поле ввода"""
        self.text_field.setText(value)


class CreativeRow(QWidget):
    """
    Строка с полем для названия креатива.
    
    Используется в:
    - CreateProjectBlock (Создание проекта)
    - PublishBlock (Публикация)
    
    Как работает:
    - Кнопка "+" вызывает on_add (создаёт новую строку)
    - Кнопка "-" вызывает on_remove (удаляет эту строку)
    
    Параметры:
        value: str - начальное значение поля (по умолчанию "creative")
        on_add: function - вызывается при нажатии на "+"
        on_remove: function - вызывается при нажатии на "-"
    """
    
    def __init__(self, value="creative", on_add=None, on_remove=None):
        super().__init__()
        self.on_add = on_add
        self.on_remove = on_remove
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Текстовое поле для ввода названия креатива
        self.text_field = QLineEdit(value)
        self.text_field.setPlaceholderText("Название креатива")
        self.text_field.setMinimumHeight(32)
        layout.addWidget(self.text_field, 1)
        
        # Кнопка удаления (-)
        self.remove_btn = QPushButton()
        set_icon(self.remove_btn, 'minus', 16)
        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.setFixedSize(28, 28)
        self.remove_btn.clicked.connect(self._on_remove)
        layout.addWidget(self.remove_btn)
        
        # Кнопка добавления (+)
        self.add_btn = QPushButton()
        set_icon(self.add_btn, 'plus', 16)
        self.add_btn.setObjectName("add_btn")
        self.add_btn.setFixedSize(28, 28)
        self.add_btn.clicked.connect(self._on_add)
        layout.addWidget(self.add_btn)
    
    def _on_add(self):
        """Вызывается при нажатии на кнопку '+'"""
        if self.on_add:
            self.on_add()
    
    def _on_remove(self):
        """Вызывается при нажатии на кнопку '-'"""
        if self.on_remove:
            self.on_remove(self)
    
    def get_value(self):
        """Возвращает текст из поля ввода (без лишних пробелов)"""
        return self.text_field.text().strip()
    
    def set_value(self, value):
        """Устанавливает текст в поле ввода"""
        self.text_field.setText(value)