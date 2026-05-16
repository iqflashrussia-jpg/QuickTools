"""
QuickTools - главное окно приложения на PySide6
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import Qt

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем нашу стартовую страницу
from ui_pyside6.start_page import StartPage


class QuickTools(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Настройки окна
        self.setWindowTitle("QuickTools")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)
        
        # Центральный виджет с переключаемыми страницами
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Создаём стартовую страницу
        self.start_page = StartPage(self.on_project_selected)
        self.stack.addWidget(self.start_page)
        
        # Применяем стили
        self.apply_styles()
    
    def apply_styles(self):
        """Общие стили для окна"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0A0A0A;
            }
        """)
    
    def on_project_selected(self, path=None, create_new=False):
        """Обработчик выбора проекта"""
        if create_new:
            print("🆕 Создание нового проекта...")
            # TODO: открыть страницу создания проекта
        elif path:
            print(f"📂 Открыт проект: {path}")
            # TODO: открыть главный экран с инструментами
        else:
            print("❌ Проект не выбран")


def main():
    app = QApplication(sys.argv)
    
    # Включаем поддержку Drag & Drop на уровне приложения
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
    
    window = QuickTools()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()