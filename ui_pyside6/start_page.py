"""
Стартовая страница приложения (в едином стиле с вкладками)
"""

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui_pyside6.icons_utils import get_icon, set_icon
from ui_pyside6.styles import COLORS, SIZES


class StartPage(QWidget):
    """Стартовая страница приложения в едином стиле"""
    
    def __init__(self, on_project_selected):
        super().__init__()
        self.on_project_selected = on_project_selected
        
        # Включаем Drag & Drop
        self.setAcceptDrops(True)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Создаём интерфейс"""
        # Главный layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        # Центральный контейнер
        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setSpacing(20)
        
        # Карточка (как в других вкладках) - даёт фон
        self.card = QFrame()
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(0)
        
        # Дропзона с пунктирной рамкой (внутри карточки)
        self.drop_zone = QFrame()
        self.drop_zone.setObjectName("drop_zone")
        self.drop_zone.setMinimumSize(400, 260)
        self.drop_zone.setAcceptDrops(True)
        
        drop_layout = QVBoxLayout(self.drop_zone)
        drop_layout.setAlignment(Qt.AlignCenter)
        drop_layout.setSpacing(12)
        
        # Иконка папки
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setObjectName("start_icon")
        icon = get_icon('folder_open', color=COLORS.get("text_muted", "#787E89"), size=48)
        if icon and not icon.isNull():
            self.icon_label.setPixmap(icon.pixmap(48, 48))
        else:
            self.icon_label.setText("📁")
            self.icon_label.setStyleSheet(f"font-size: 48px; color: {COLORS.get('text_muted', '#787E89')};")
        drop_layout.addWidget(self.icon_label)
        
        # Текст
        drop_title = QLabel("Drag & Drop to Upload File")
        drop_title.setAlignment(Qt.AlignCenter)
        drop_title.setObjectName("drop_title")
        drop_layout.addWidget(drop_title)
        
        # Текст OR
        or_label = QLabel("OR")
        or_label.setAlignment(Qt.AlignCenter)
        or_label.setObjectName("or_label")
        drop_layout.addWidget(or_label)
        
        # Кнопка Browse File
        self.browse_btn = QPushButton("Browse File")
        self.browse_btn.setObjectName("browse_btn")
        set_icon(self.browse_btn, 'folder', 16, color=COLORS.get("btn_primary_text", "#071107"))
        self.browse_btn.clicked.connect(self.open_folder_dialog)
        drop_layout.addWidget(self.browse_btn, alignment=Qt.AlignCenter)
        
        card_layout.addWidget(self.drop_zone)
        center_layout.addWidget(self.card, alignment=Qt.AlignCenter)
        
        # Кнопка создания проекта (под карточкой)
        self.create_btn = QPushButton("Создать новый проект")
        self.create_btn.setObjectName("create_btn")
        set_icon(self.create_btn, 'plus', 16, color=COLORS.get("accent", "#4CAF50"))
        self.create_btn.clicked.connect(self.create_project)
        center_layout.addWidget(self.create_btn, alignment=Qt.AlignCenter)
        
        main_layout.addWidget(center_container, 1)
        
        # Применяем стили
        self.apply_styles()
    
    def apply_styles(self):
        """Применяем стили в единой дизайн-системе"""
        c = COLORS
        s = SIZES
        
        self.setStyleSheet(f"""
            /* Карточка как в других вкладках */
            QFrame#card {{
                background-color: {c["bg_card"]};
                border: none;
                border-radius: {s["radius_xl"]};
                padding: 20px;
            }}
            
            /* Дропзона с пунктирной рамкой */
            QFrame#drop_zone {{
                background-color: transparent;
                border: 2px dashed {c["border_default"]};
                border-radius: {s["radius_large"]};
            }}
            
            QFrame#drop_zone:hover {{
                border-color: {c["accent"]};
            }}
            
            /* Заголовок дропзоны */
            QLabel#drop_title {{
                color: {c["text_primary"]};
                font-size: 16px;
                font-weight: 500;
            }}
            
            /* Текст OR */
            QLabel#or_label {{
                color: {c["text_muted"]};
                font-size: 12px;
                font-weight: 400;
            }}
            
            /* Кнопка Browse File */
            QPushButton#browse_btn {{
                background-color: {c["btn_secondary_bg"]};
                color: {c["btn_secondary_text"]};
                border: 1px solid {c["border_default"]};
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 13px;
                font-weight: 500;
                min-width: 120px;
                min-height: 36px;
            }}
            
            QPushButton#browse_btn:hover {{
                background-color: {c["btn_secondary_hover"]};
                border-color: {c["accent"]};
            }}
            
            /* Кнопка создания проекта */
            QPushButton#create_btn {{
                background-color: transparent;
                color: {c["accent"]};
                border: 1px solid {c["border_default"]};
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 13px;
                font-weight: 500;
                min-width: 160px;
                min-height: 36px;
                margin-top: 10px;
            }}
            
            QPushButton#create_btn:hover {{
                background-color: {c["accent"]};
                color: {c["text_on_accent"]};
                border-color: {c["accent"]};
            }}
            
            /* Иконка */
            QLabel#start_icon {{
                margin-bottom: 8px;
            }}
        """)
        
        # Применяем глобальные стили к виджету
        from ui_pyside6.styles import apply_styles
        apply_styles(self)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Когда файл перетаскивают в зону"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drop_zone.setStyleSheet(f"""
                QFrame#drop_zone {{
                    background-color: transparent;
                    border: 2px dashed {COLORS.get("accent", "#4CAF50")};
                    border-radius: {SIZES.get("radius_large", "10px")};
                }}
            """)
    
    def dragLeaveEvent(self, event):
        """Когда файл убрали из зоны"""
        self.drop_zone.setStyleSheet(f"""
            QFrame#drop_zone {{
                background-color: transparent;
                border: 2px dashed {COLORS.get("border_default", "#787E89")};
                border-radius: {SIZES.get("radius_large", "10px")};
            }}
        """)
    
    def dropEvent(self, event: QDropEvent):
        """Когда файл бросили в зону"""
        # Возвращаем обычный стиль
        self.drop_zone.setStyleSheet(f"""
            QFrame#drop_zone {{
                background-color: transparent;
                border: 2px dashed {COLORS.get("border_default", "#787E89")};
                border-radius: {SIZES.get("radius_large", "10px")};
            }}
        """)
        
        files = event.mimeData().urls()
        if files:
            path = files[0].toLocalFile()
            if os.path.isdir(path):
                self.on_project_selected(path)
    
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