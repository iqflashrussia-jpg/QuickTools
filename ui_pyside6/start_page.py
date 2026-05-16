"""
Стартовая страница на PySide6
"""

import sys
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QFileDialog
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QDragEnterEvent, QDropEvent


class StartPage(QWidget):
    """Стартовая страница приложения"""
    
    def __init__(self, on_project_selected):
        super().__init__()
        self.on_project_selected = on_project_selected  # callback при выборе проекта
        
        # Включаем Drag & Drop
        self.setAcceptDrops(True)
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Создаём интерфейс"""
        # Главный вертикальный слой
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        
        # Заголовок
        title = QLabel("QuickTools")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")
        
        subtitle = QLabel("Инструменты для работы с рекламными проектами")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitle")
        
        # Drag & Drop зона (карточка)
        self.drop_zone = QFrame()
        self.drop_zone.setObjectName("drop_zone")
        self.drop_zone.setMinimumWidth(400)
        self.drop_zone.setMinimumHeight(250)
        
        # Содержимое зоны перетаскивания
        drop_layout = QVBoxLayout(self.drop_zone)
        drop_layout.setAlignment(Qt.AlignCenter)
        drop_layout.setSpacing(15)
        
        # Иконка (эмодзи)
        icon_label = QLabel("📁")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setObjectName("icon")
        
        # Текст
        drop_text = QLabel("Перетащите папку проекта сюда")
        drop_text.setAlignment(Qt.AlignCenter)
        drop_text.setObjectName("drop_text")
        
        drop_hint = QLabel("или")
        drop_hint.setAlignment(Qt.AlignCenter)
        drop_hint.setObjectName("drop_hint")
        
        # Кнопка выбора папки
        self.open_btn = QPushButton("Выбрать папку")
        self.open_btn.setObjectName("open_btn")
        self.open_btn.clicked.connect(self.open_folder_dialog)
        
        # Кнопка создания проекта
        self.create_btn = QPushButton("Создать проект")
        self.create_btn.setObjectName("create_btn")
        self.create_btn.clicked.connect(self.create_project)
        
        # Собираем зону перетаскивания
        drop_layout.addWidget(icon_label)
        drop_layout.addWidget(drop_text)
        drop_layout.addWidget(drop_hint)
        drop_layout.addWidget(self.open_btn, alignment=Qt.AlignCenter)
        
        # Ряд с кнопкой создания
        button_row = QHBoxLayout()
        button_row.setAlignment(Qt.AlignCenter)
        button_row.addWidget(self.create_btn)
        
        # Собираем главную страницу
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(self.drop_zone, alignment=Qt.AlignCenter)
        main_layout.addLayout(button_row)
        
        self.setLayout(main_layout)
    
    def apply_styles(self):
        """Применяем CSS-стили"""
        self.setStyleSheet("""
            QWidget {
                background-color: #0A0A0A;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
            
            QLabel#title {
                color: #4CAF50;
                font-size: 48px;
                font-weight: bold;
            }
            
            QLabel#subtitle {
                color: #888888;
                font-size: 18px;
            }
            
            QFrame#drop_zone {
                background-color: #1E1E1E;
                border-radius: 16px;
                border: 2px solid #2A2A2A;
            }
            
            QFrame#drop_zone:hover {
                border: 2px solid #4CAF50;
                background-color: #2A2A2A;
            }
            
            QLabel#icon {
                font-size: 64px;
            }
            
            QLabel#drop_text {
                color: #FFFFFF;
                font-size: 20px;
                font-weight: 500;
            }
            
            QLabel#drop_hint {
                color: #666666;
                font-size: 14px;
            }
            
            QPushButton#open_btn {
                background-color: #2A2A2A;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
            }
            
            QPushButton#open_btn:hover {
                background-color: #3A3A3A;
            }
            
            QPushButton#create_btn {
                background-color: #4CAF50;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 14px 28px;
                font-size: 16px;
                font-weight: bold;
            }
            
            QPushButton#create_btn:hover {
                background-color: #45a049;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Когда файл перетаскивают в зону"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            # Меняем стиль при наведении
            self.drop_zone.setStyleSheet("""
                QFrame#drop_zone {
                    background-color: #2A2A2A;
                    border-radius: 16px;
                    border: 2px solid #4CAF50;
                }
            """)
    
    def dragLeaveEvent(self, event):
        """Когда файл убрали из зоны"""
        self.drop_zone.setStyleSheet("""
            QFrame#drop_zone {
                background-color: #1E1E1E;
                border-radius: 16px;
                border: 2px solid #2A2A2A;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """Когда файл бросили в зону"""
        self.drop_zone.setStyleSheet("""
            QFrame#drop_zone {
                background-color: #1E1E1E;
                border-radius: 16px;
                border: 2px solid #2A2A2A;
            }
        """)
        
        files = event.mimeData().urls()
        if files:
            # Получаем путь к файлу/папке
            path = files[0].toLocalFile()
            if os.path.isdir(path):
                self.on_project_selected(path)
            else:
                # Показываем уведомление об ошибке
                self.show_message("Пожалуйста, выберите папку, а не файл")
    
    def open_folder_dialog(self):
        """Открыть диалог выбора папки"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Выберите папку проекта",
            "",  # начальная директория
            QFileDialog.ShowDirsOnly
        )
        if folder:
            self.on_project_selected(folder)
    
    def create_project(self):
        """Создать новый проект"""
        self.on_project_selected(None, create_new=True)
    
    def show_message(self, text):
        """Показать временное сообщение"""
        # Создаём и показываем всплывающее сообщение
        msg = QLabel(text)
        msg.setStyleSheet("""
            QLabel {
                background-color: #FF453A;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
            }
        """)
        msg.setAlignment(Qt.AlignCenter)
        msg.setMinimumWidth(300)
        
        # Добавляем на 2 секунды
        msg.show()
        
        # Автоудаление через 2 секунды
        from PySide6.QtCore import QTimer
        QTimer.singleShot(2000, msg.deleteLater)