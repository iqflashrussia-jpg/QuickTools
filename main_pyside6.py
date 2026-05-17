"""
QuickTools - главное окно приложения на PySide6
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import Qt

# Импортируем Qt-Material
from qt_material import apply_stylesheet

sys.path.insert(0, os.path.dirname(__file__))

from ui_pyside6.start_page import StartPage
from ui_pyside6.main_tabs import MainTabs


class QuickTools(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QuickTools")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Стартовая страница
        self.start_page = StartPage(self.on_project_selected)
        self.stack.addWidget(self.start_page)
        
        # Стили (дополнительные, поверх темы)
        self.apply_styles()
    
    def apply_styles(self):
        """Дополнительные стили поверх темы"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0A0A0A;
            }
        """)
    
    def on_project_selected(self, path=None, create_new=False):
        """Обработчик выбора проекта"""
        if create_new:
            self.log("🆕 Создание нового проекта...")
            self.main_tabs = MainTabs(None, self.log)
            self.stack.addWidget(self.main_tabs)
            self.stack.setCurrentWidget(self.main_tabs)
            self.main_tabs.tabs.setCurrentIndex(0)
        elif path:
            self.log(f"📂 Открыт проект: {path}")
            self.main_tabs = MainTabs(path, self.log)
            self.stack.addWidget(self.main_tabs)
            self.stack.setCurrentWidget(self.main_tabs)
        else:
            self.log("❌ Проект не выбран")
    
    def log(self, message):
        """Вывод сообщения в консоль"""
        print(message)


def main():
    app = QApplication(sys.argv)
    
    # ========== ПРИМЕНЯЕМ ТЕМУ MATERIAL DESIGN ==========
    # Можно выбрать любую из 19 тем:
    # dark_teal, dark_blue, dark_cyan, dark_purple, dark_red, 
    # dark_amber, dark_pink, dark_yellow, dark_lightgreen,
    # light_blue, light_teal, light_purple, light_red, 
    # light_amber, light_cyan, light_lightgreen, light_pink, light_yellow
    
    apply_stylesheet(app, theme='dark_teal.xml')
    # ====================================================
    
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
    
    window = QuickTools()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()