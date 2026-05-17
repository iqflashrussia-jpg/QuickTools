"""
Стартовая страница приложения (современный дизайн)
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont

from ui_pyside6.icons_utils import set_icon


class StartPage(QWidget):
    """Стартовая страница приложения в современном стиле"""
    
    def __init__(self, on_project_selected):
        super().__init__()
        self.on_project_selected = on_project_selected
        
        # Включаем Drag & Drop
        self.setAcceptDrops(True)
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Создаём интерфейс"""
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(0)
        
        # Центральный контейнер
        self.center_widget = QWidget()
        center_layout = QVBoxLayout(self.center_widget)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setSpacing(0)
        
        # Логотип
        logo = QLabel("QuickTools")
        logo.setAlignment(Qt.AlignCenter)
        logo.setObjectName("logo")
        center_layout.addWidget(logo)
        
        # Подзаголовок
        subtitle = QLabel("Инструменты для работы с рекламными проектами")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitle")
        center_layout.addWidget(subtitle)
        
        # Отступ
        center_layout.addSpacing(30)
        
        # Карточка с дропзоной
        self.card = QFrame()
        self.card.setObjectName("upload_card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        
        # Drop zone
        self.drop_zone = QFrame()
        self.drop_zone.setObjectName("dropzone")
        self.drop_zone.setMinimumHeight(380)
        drop_layout = QVBoxLayout(self.drop_zone)
        drop_layout.setAlignment(Qt.AlignCenter)
        drop_layout.setSpacing(15)
        
        # Сетка (эффект)
        self.grid = QFrame()
        self.grid.setObjectName("grid")
        self.grid.setFixedSize(400, 380)
        
        # Иконка
        icon_wrap = QFrame()
        icon_wrap.setObjectName("icon_wrap")
        icon_wrap.setFixedSize(130, 130)
        icon_layout = QVBoxLayout(icon_wrap)
        icon_layout.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel("📁")
        icon_label.setObjectName("icon")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        # Текст
        drop_title = QLabel("Перетащите папку проекта сюда")
        drop_title.setObjectName("drop_title")
        drop_title.setAlignment(Qt.AlignCenter)
        
        drop_text = QLabel("или выберите директорию вручную")
        drop_text.setObjectName("drop_text")
        drop_text.setAlignment(Qt.AlignCenter)
        
        # Кнопка выбора папки
        self.browse_btn = QPushButton("Выбрать папку")
        self.browse_btn.setObjectName("browse_btn")
        self.browse_btn.clicked.connect(self.open_folder_dialog)
        
        # Собираем dropzone
        drop_layout.addWidget(icon_wrap)
        drop_layout.addWidget(drop_title)
        drop_layout.addWidget(drop_text)
        drop_layout.addWidget(self.browse_btn)
        
        # Добавляем грид поверх (но под содержимым)
        # Просто добавляем в отдельный layout
        card_layout.addWidget(self.drop_zone)
        
        center_layout.addWidget(self.card)
        
        # Отступ
        center_layout.addSpacing(30)
        
        # Кнопка создания проекта
        self.create_btn = QPushButton("Создать проект")
        self.create_btn.setObjectName("create_btn")
        self.create_btn.clicked.connect(self.create_project)
        center_layout.addWidget(self.create_btn, alignment=Qt.AlignCenter)
        
        # Отступ
        center_layout.addSpacing(20)
        
        # Футер
        footer = QLabel("QUICKTOOLS • CREATIVE PRODUCTION SYSTEM")
        footer.setAlignment(Qt.AlignCenter)
        footer.setObjectName("footer")
        center_layout.addWidget(footer)
        
        main_layout.addWidget(self.center_widget)
    
    def apply_styles(self):
        """Применяем современные стили"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #05070b,
                    stop:1 #060a12);
                font-family: 'Inter', 'Segoe UI', sans-serif;
            }
            
            QLabel#logo {
                font-size: 72px;
                font-weight: 800;
                color: #55c84f;
                letter-spacing: -2px;
                margin-bottom: 8px;
            }
            
            QLabel#subtitle {
                color: #7f8b9b;
                font-size: 18px;
            }
            
            QFrame#upload_card {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(15,20,29,0.96),
                    stop:1 rgba(9,13,20,0.98));
                border: 1px solid #1a2230;
                border-radius: 34px;
                padding: 28px;
                min-width: 500px;
            }
            
            QFrame#dropzone {
                background: #070b12;
                border: 2px dashed rgba(85,200,79,0.22);
                border-radius: 26px;
                min-height: 380px;
            }
            
            QFrame#dropzone:hover {
                border-color: rgba(85,200,79,0.45);
            }
            
            QFrame#icon_wrap {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(85,200,79,0.18),
                    stop:1 rgba(85,200,79,0.05));
                border: 1px solid rgba(85,200,79,0.18);
                border-radius: 32px;
            }
            
            QLabel#icon {
                font-size: 62px;
            }
            
            QLabel#drop_title {
                font-size: 34px;
                font-weight: 700;
                color: #ffffff;
                letter-spacing: -1px;
                margin-top: 10px;
            }
            
            QLabel#drop_text {
                color: #7f8b9b;
                font-size: 16px;
            }
            
            QPushButton#browse_btn {
                background-color: #1b2330;
                color: #ffffff;
                border: none;
                border-radius: 18px;
                font-size: 16px;
                font-weight: 600;
                padding: 16px 34px;
                margin-top: 10px;
            }
            
            QPushButton#browse_btn:hover {
                background-color: #243041;
            }
            
            QPushButton#create_btn {
                background-color: #55c84f;
                color: #071107;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: 700;
                padding: 20px 50px;
                min-width: 260px;
            }
            
            QPushButton#create_btn:hover {
                background-color: #4db947;
            }
            
            QLabel#footer {
                color: #566171;
                font-size: 13px;
                letter-spacing: 1px;
                margin-top: 20px;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Когда файл перетаскивают в зону"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drop_zone.setStyleSheet("""
                QFrame#dropzone {
                    background: #070b12;
                    border: 2px dashed rgba(85,200,79,0.45);
                    border-radius: 26px;
                    min-height: 380px;
                }
            """)
    
    def dragLeaveEvent(self, event):
        """Когда файл убрали из зоны"""
        self.drop_zone.setStyleSheet("""
            QFrame#dropzone {
                background: #070b12;
                border: 2px dashed rgba(85,200,79,0.22);
                border-radius: 26px;
                min-height: 380px;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """Когда файл бросили в зону"""
        self.drop_zone.setStyleSheet("""
            QFrame#dropzone {
                background: #070b12;
                border: 2px dashed rgba(85,200,79,0.22);
                border-radius: 26px;
                min-height: 380px;
            }
        """)
        
        files = event.mimeData().urls()
        if files:
            path = files[0].toLocalFile()
            if os.path.isdir(path):
                self.on_project_selected(path)
            else:
                self.show_message("Пожалуйста, выберите папку, а не файл")
    
    def open_folder_dialog(self):
        """Открыть диалог выбора папки"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Выберите папку проекта",
            "",
            QFileDialog.ShowDirsOnly
        )
        if folder:
            self.on_project_selected(folder)
    
    def create_project(self):
        """Создать новый проект"""
        self.on_project_selected(None, create_new=True)
    
    def show_message(self, text):
        """Показать временное сообщение"""
        msg = QLabel(text)
        msg.setStyleSheet("""
            QLabel {
                background-color: #FF453A;
                color: white;
                padding: 12px 20px;
                border-radius: 12px;
                font-size: 14px;
            }
        """)
        msg.setAlignment(Qt.AlignCenter)
        msg.setFixedWidth(350)
        
        # Позиционируем в центре
        msg.show()
        
        QTimer.singleShot(2000, msg.deleteLater)