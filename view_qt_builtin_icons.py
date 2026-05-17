"""
Просмотр всех встроенных иконок Qt (QStyle.StandardPixmap)
Эти иконки точно есть на всех платформах
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QScrollArea, QLineEdit, QGridLayout,
    QStyle
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


class IconViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Встроенные иконки Qt (StandardPixmap)")
        self.resize(900, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Поле для поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Фильтр иконок...")
        self.search_input.textChanged.connect(self.filter_icons)
        layout.addWidget(self.search_input)
        
        # Область для иконок
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.icons_widget = QWidget()
        self.icons_layout = QGridLayout(self.icons_widget)
        self.icons_layout.setSpacing(15)
        scroll.setWidget(self.icons_widget)
        layout.addWidget(scroll)
        
        self.style = QApplication.instance().style()
        
        # Список всех доступных иконок из QStyle.StandardPixmap
        self.all_icons = []
        
        # Проходим по всем возможным иконкам
        for sp_enum in dir(QStyle.StandardPixmap):
            if sp_enum.startswith('SP_'):
                # Получаем иконку
                sp_value = getattr(QStyle.StandardPixmap, sp_enum)
                icon = self.style.standardIcon(sp_value)
                if not icon.isNull():
                    # Красивое имя для отображения
                    display_name = sp_enum.replace('SP_', '').replace('_', ' ')
                    self.all_icons.append((sp_enum, display_name, icon))
        
        self.show_icons(self.all_icons)
    
    def show_icons(self, icons_list):
        """Отображает список иконок"""
        # Очищаем layout
        for i in reversed(range(self.icons_layout.count())):
            widget = self.icons_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        row = 0
        col = 0
        max_cols = 4
        
        for sp_enum, display_name, icon in icons_list:
            # Создаём карточку иконки
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(8)
            
            # Показываем иконку
            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(QSize(48, 48)))
            icon_label.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(icon_label)
            
            # Название иконки (техническое)
            name_label = QLabel(sp_enum)
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("font-size: 9px; color: #666; font-family: monospace;")
            card_layout.addWidget(name_label)
            
            # Описание (человеческое)
            desc_label = QLabel(display_name)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setStyleSheet("font-size: 11px; color: #fff; font-weight: 500;")
            card_layout.addWidget(desc_label)
            
            # Стили карточки
            card.setStyleSheet("""
                QWidget {
                    background-color: #1E1E1E;
                    border-radius: 10px;
                    padding: 12px;
                }
                QWidget:hover {
                    background-color: #2A2A2A;
                }
            """)
            
            self.icons_layout.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def filter_icons(self, text):
        """Фильтрует иконки по тексту"""
        if not text.strip():
            self.show_icons(self.all_icons)
            return
        
        filtered = []
        text_lower = text.lower()
        for sp_enum, display_name, icon in self.all_icons:
            if text_lower in sp_enum.lower() or text_lower in display_name.lower():
                filtered.append((sp_enum, display_name, icon))
        
        self.show_icons(filtered)


def main():
    app = QApplication(sys.argv)
    
    # Применяем Fusion стиль (иконки будут белыми/серыми)
    app.setStyle("Fusion")
    
    # Тёмная палитра
    app.setStyleSheet("""
        QWidget {
            background-color: #0A0A0A;
            color: #FFFFFF;
        }
        QLineEdit {
            background-color: #1E1E1E;
            border: 1px solid #3A3A3A;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border-color: #55c84f;
        }
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        QScrollBar:vertical {
            background-color: #1E1E1E;
            width: 8px;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical {
            background-color: #3A3A3A;
            border-radius: 4px;
        }
    """)
    
    window = IconViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()