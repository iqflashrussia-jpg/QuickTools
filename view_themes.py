"""
Просмотр всех доступных тем Qt-Material
"""

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTabWidget, QCheckBox, QSlider
from PySide6.QtCore import Qt
from qt_material import apply_stylesheet, list_themes
import sys

class ThemeViewer(QWidget):
    def __init__(self, theme_name):
        super().__init__()
        self.setWindowTitle(f"Тема: {theme_name}")
        self.resize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Разные виджеты для демонстрации
        layout.addWidget(QLabel(f"Текущая тема: {theme_name}"))
        
        layout.addWidget(QPushButton("Обычная кнопка"))
        
        btn_success = QPushButton("Кнопка успеха")
        btn_success.setObjectName("success")
        layout.addWidget(btn_success)
        
        layout.addWidget(QLabel("Поле ввода:"))
        layout.addWidget(QLineEdit())
        
        layout.addWidget(QCheckBox("Чекбокс"))
        
        layout.addWidget(QLabel("Слайдер:"))
        slider = QSlider(Qt.Horizontal)
        layout.addWidget(slider)

def main():
    themes = list_themes()
    print("Доступные темы:")
    for i, theme in enumerate(themes):
        print(f"  {i+1}. {theme}")
    
    if len(sys.argv) > 1:
        theme_name = sys.argv[1]
    else:
        theme_name = themes[0]
    
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme=theme_name)
    
    viewer = ThemeViewer(theme_name)
    viewer.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()