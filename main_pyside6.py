#!/usr/bin/env python3
"""
QuickTools - Главный файл запуска
"""

import os
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from ui_pyside6.icons_utils import TABLER_AVAILABLE
from ui_pyside6.main_tabs import MainTabs
from ui_pyside6.start_page import StartPage
from ui_pyside6.styles import apply_styles


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickTools")
        self.setGeometry(100, 100, 1200, 700)
        
        # Устанавливаем иконку окна
        if TABLER_AVAILABLE:
            from tablerqicon import TablerQIcon
            try:
                icon = TablerQIcon(color="#55c84f", size=32)
                app_icon = getattr(icon, 'tool', None)
                if app_icon:
                    self.setWindowIcon(app_icon)
            except Exception:
                pass
        
        # Показываем стартовую страницу
        self.start_page = StartPage(self.on_project_selected)
        self.setCentralWidget(self.start_page)
        
        # Применяем стили
        apply_styles(self)
    
    def on_project_selected(self, project_path, create_new=False):
        """Обработчик выбора проекта"""
        if create_new:
            # Создаём новый проект
            self.main_tabs = MainTabs(None, self.log_message)
            self.setCentralWidget(self.main_tabs)
            apply_styles(self)
        elif project_path:
            # Открываем существующий проект
            self.main_tabs = MainTabs(project_path, self.log_message)
            self.setCentralWidget(self.main_tabs)
            apply_styles(self)
            self.save_last_project(project_path)
    
    def save_last_project(self, path):
        """Сохраняет путь последнего проекта"""
        last_project_file = os.path.join(os.path.dirname(__file__), "last_project.txt")
        try:
            with open(last_project_file, 'w', encoding='utf-8') as f:
                f.write(path)
        except Exception:
            pass
    
    def load_last_project(self):
        """Загружает путь последнего открытого проекта"""
        last_project_file = os.path.join(os.path.dirname(__file__), "last_project.txt")
        if os.path.exists(last_project_file):
            try:
                with open(last_project_file, encoding='utf-8') as f:
                    path = f.read().strip()
                    if path and os.path.exists(path):
                        return path
            except Exception:
                pass
        return None
    
    def log_message(self, message):
        """Обработка логов из вкладок"""
        print(message)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()