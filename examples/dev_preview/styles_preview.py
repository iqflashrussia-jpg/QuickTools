import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QComboBox,
    QStyleFactory, QTabWidget
)
from PySide6.QtCore import Qt


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Тест стилей PySide6")
        self.setMinimumSize(500, 400)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Кнопка
        layout.addWidget(QLabel("Обычная кнопка:"))
        layout.addWidget(QPushButton("Нажми меня"))
        
        # Поле ввода
        layout.addWidget(QLabel("Поле ввода:"))
        layout.addWidget(QLineEdit("Пример текста"))
        
        # Выпадающий список
        layout.addWidget(QLabel("Выпадающий список:"))
        combo = QComboBox()
        combo.addItems(["Пункт 1", "Пункт 2", "Пункт 3"])
        layout.addWidget(combo)
        
        # Вкладки
        tabs = QTabWidget()
        tabs.addTab(QWidget(), "Вкладка 1")
        tabs.addTab(QWidget(), "Вкладка 2")
        layout.addWidget(tabs)
        
        layout.addStretch()


def main():
    app = QApplication(sys.argv)
    
    # Показываем доступные стили
    print("Доступные стили:", QStyleFactory.keys())
    
    # Применяем стиль Fusion (современный)
    app.setStyle(QStyleFactory.create("Fusion"))
    
    window = TestWindow()
    window.show()
    
    print("\nСовет: в консоли измени стиль на Windows или windowsvista")
    print("Открой новое окно и пиши: python -c \"from PySide6.QtWidgets import QApplication; app = QApplication.instance(); app.setStyle('Windows')\"")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()