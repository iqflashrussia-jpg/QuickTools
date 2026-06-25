#!/usr/bin/env python3
"""
Минимальный тест для проверки работы теней в Qt/PySide6
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Тест теней Qt")
        self.setGeometry(200, 200, 600, 400)
        
        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # === ТЕСТ 1: Простая тень на QFrame ===
        frame1 = QFrame()
        frame1.setFrameShape(QFrame.Box)
        frame1.setStyleSheet("""
            QFrame {
                background-color: #181B20;
                border-radius: 10px;
                min-height: 80px;
            }
        """)
        
        # Добавляем тень
        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(20)
        shadow1.setXOffset(5)
        shadow1.setYOffset(5)
        shadow1.setColor(QColor(255, 0, 0, 200))  # Красная тень
        frame1.setGraphicsEffect(shadow1)
        
        label1 = QLabel("КРАСНАЯ ТЕНЬ (должна быть видна)")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("color: white; font-size: 14px;")
        
        frame_layout = QVBoxLayout(frame1)
        frame_layout.addWidget(label1)
        layout.addWidget(frame1)
        
        # === ТЕСТ 2: Тень на кнопке ===
        btn = QPushButton("Кнопка с тенью")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                min-height: 50px;
            }
        """)
        
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(15)
        shadow2.setXOffset(3)
        shadow2.setYOffset(3)
        shadow2.setColor(QColor(0, 255, 0, 200))  # Зелёная тень
        btn.setGraphicsEffect(shadow2)
        
        layout.addWidget(btn)
        
        # === ТЕСТ 3: Тень на главном окне ===
        self.setStyleSheet("background-color: #16191D;")
        
        # Добавляем тень на всё окно (должна быть снаружи)
        window_shadow = QGraphicsDropShadowEffect()
        window_shadow.setBlurRadius(25)
        window_shadow.setXOffset(8)
        window_shadow.setYOffset(8)
        window_shadow.setColor(QColor(0, 0, 255, 200))  # Синяя тень
        self.setGraphicsEffect(window_shadow)
        
        # Инструкция
        info = QLabel(
            "Если вы видите:\n"
            "• Красную тень вокруг верхнего прямоугольника\n"
            "• Зелёную тень вокруг кнопки\n"
            "• Синюю тень вокруг всего окна\n\n"
            "→ ТЕНИ РАБОТАЮТ!\n\n"
            "Если теней нет → проблема в системе/Qt"
        )
        info.setStyleSheet("color: #787E89; font-size: 12px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Пробуем разные настройки для совместимости
    # Раскомментируй по очереди, если тени не работают
    
    # Вариант 1: Программный рендеринг
    app.setAttribute(Qt.AA_UseSoftwareOpenGL, True)
    
    # Вариант 2: Отключаем аппаратное ускорение
    import os
    os.environ["QT_QUICK_BACKEND"] = "software"
    
    window = TestWindow()
    window.show()
    
    print("=== ТЕСТ ТЕНЕЙ ===")
    print("Должны появиться три тени: красная, зелёная и синяя")
    print("Если теней нет - пробуй раскомментировать настройки в коде")
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()