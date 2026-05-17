"""
Блок "Создание проекта" - полная копия логики из Flet
"""

import os
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea, QFrame,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class PlatformRow(QWidget):
    """Строка с полем для площадки и кнопками +/–"""
    
    def __init__(self, value="Master", on_add=None, on_remove=None):
        super().__init__()
        self.on_add = on_add
        self.on_remove = on_remove
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        self.text_field = QLineEdit(value)
        self.text_field.setPlaceholderText("Название площадки")
        self.text_field.setMinimumHeight(40)
        layout.addWidget(self.text_field, 1)
        
        self.remove_btn = QPushButton("−")
        self.remove_btn.setFixedSize(36, 36)
        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.clicked.connect(self._on_remove)
        layout.addWidget(self.remove_btn)
        
        self.add_btn = QPushButton("+")
        self.add_btn.setFixedSize(36, 36)
        self.add_btn.setObjectName("add_btn")
        self.add_btn.clicked.connect(self._on_add)
        layout.addWidget(self.add_btn)
    
    def _on_add(self):
        if self.on_add:
            self.on_add()
    
    def _on_remove(self):
        if self.on_remove:
            self.on_remove(self)
    
    def get_value(self):
        return self.text_field.text().strip()
    
    def set_value(self, value):
        self.text_field.setText(value)


class CreativeRow(QWidget):
    """Строка с полем для креатива и кнопками +/–"""
    
    def __init__(self, value="creative", on_add=None, on_remove=None):
        super().__init__()
        self.on_add = on_add
        self.on_remove = on_remove
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        self.text_field = QLineEdit(value)
        self.text_field.setPlaceholderText("Название креатива")
        self.text_field.setMinimumHeight(40)
        layout.addWidget(self.text_field, 1)
        
        self.remove_btn = QPushButton("−")
        self.remove_btn.setFixedSize(36, 36)
        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.clicked.connect(self._on_remove)
        layout.addWidget(self.remove_btn)
        
        self.add_btn = QPushButton("+")
        self.add_btn.setFixedSize(36, 36)
        self.add_btn.setObjectName("add_btn")
        self.add_btn.clicked.connect(self._on_add)
        layout.addWidget(self.add_btn)
    
    def _on_add(self):
        if self.on_add:
            self.on_add()
    
    def _on_remove(self):
        if self.on_remove:
            self.on_remove(self)
    
    def get_value(self):
        return self.text_field.text().strip()
    
    def set_value(self, value):
        self.text_field.setText(value)


class CreateProjectBlock(QWidget):
    """Вкладка создания структуры проекта"""
    
    # Сигнал для обновления текущего проекта
    project_created = Signal(str)
    
    def __init__(self, project_path, log_callback=None, update_project_callback=None):
        super().__init__()
        self.project_path = project_path
        self.log_callback = log_callback
        self.update_project_callback = update_project_callback
        
        self.platform_rows = []
        self.creative_rows = []
        
        self.setup_ui()
        self.apply_styles()
        
        # Добавляем начальные поля
        self.add_platform_row("Master")
        self.add_creative_row("creative")
    
    def setup_ui(self):
        """Создаём интерфейс"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Создаём скролл-зону
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        
        # Карточка 1: Название проекта
        project_card = QFrame()
        project_card.setObjectName("card")
        project_layout = QVBoxLayout(project_card)
        
        project_title = QLabel("Название проекта")
        project_title.setObjectName("card_title")
        project_layout.addWidget(project_title)
        
        self.project_name_field = QLineEdit("PROD")
        self.project_name_field.setPlaceholderText("Введите название проекта")
        self.project_name_field.setMinimumHeight(45)
        project_layout.addWidget(self.project_name_field)
        
        scroll_layout.addWidget(project_card)
        
        # Карточка 2: Площадки
        platforms_card = QFrame()
        platforms_card.setObjectName("card")
        platforms_layout = QVBoxLayout(platforms_card)
        
        platforms_title = QLabel("Площадки")
        platforms_title.setObjectName("card_title")
        platforms_layout.addWidget(platforms_title)
        
        self.platforms_container = QVBoxLayout()
        self.platforms_container.setSpacing(10)
        platforms_layout.addLayout(self.platforms_container)
        
        scroll_layout.addWidget(platforms_card)
        
        # Карточка 3: Названия креативов
        creatives_card = QFrame()
        creatives_card.setObjectName("card")
        creatives_layout = QVBoxLayout(creatives_card)
        
        creatives_title = QLabel("Названия креативов")
        creatives_title.setObjectName("card_title")
        creatives_layout.addWidget(creatives_title)
        
        self.creatives_container = QVBoxLayout()
        self.creatives_container.setSpacing(10)
        creatives_layout.addLayout(self.creatives_container)
        
        scroll_layout.addWidget(creatives_card)
        
        # Кнопка создания
        self.create_btn = QPushButton("СОЗДАТЬ")
        self.create_btn.setObjectName("create_btn")
        self.create_btn.setMinimumHeight(50)
        self.create_btn.clicked.connect(self.create_structure)
        scroll_layout.addWidget(self.create_btn)
        
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
    
    def add_platform_row(self, value="Master"):
        """Добавляет новую строку для площадки"""
        row = PlatformRow(value, self.add_platform_row, self.remove_platform_row)
        self.platforms_container.addWidget(row)
        self.platform_rows.append(row)
    
    def remove_platform_row(self, row):
        """Удаляет строку площадки"""
        row.deleteLater()
        self.platform_rows.remove(row)
    
    def add_creative_row(self, value="creative"):
        """Добавляет новую строку для креатива"""
        row = CreativeRow(value, self.add_creative_row, self.remove_creative_row)
        self.creatives_container.addWidget(row)
        self.creative_rows.append(row)
    
    def remove_creative_row(self, row):
        """Удаляет строку креатива"""
        row.deleteLater()
        self.creative_rows.remove(row)
    
    def get_platforms(self):
        """Получает список всех площадок"""
        platforms = []
        for row in self.platform_rows:
            val = row.get_value()
            if val:
                platforms.append(val)
        return platforms
    
    def get_creatives(self):
        """Получает список всех креативов"""
        creatives = []
        for row in self.creative_rows:
            val = row.get_value()
            if val:
                creatives.append(val)
        return creatives
    
    def log(self, message):
        """Добавляет сообщение в лог"""
        if self.log_callback:
            self.log_callback(message)
    
    def create_structure(self):
        """Создаёт структуру папок"""
        project_name = self.project_name_field.text().strip()
        if not project_name:
            self.log("❌ Введите название проекта!")
            return
        
        platforms = self.get_platforms()
        if not platforms:
            self.log("❌ Добавьте хотя бы одну площадку!")
            return
        
        creatives = self.get_creatives()
        if not creatives:
            self.log("❌ Добавьте хотя бы одно название креатива!")
            return
        
        # Диалог выбора папки
        base_folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для создания проекта",
            "",
            QFileDialog.ShowDirsOnly
        )
        
        if not base_folder:
            self.log("Выбор папки отменён")
            return
        
        project_path = os.path.join(base_folder, project_name)
        
        # Папки, в которых нужно создать креативы
        folders_with_creatives = ["animate", "ai", "img", "opt_img", "psd", "screen"]
        publish_folder = "publish"
        
        try:
            os.makedirs(project_path, exist_ok=True)
            
            # Создаём папки с креативами
            for main_folder in folders_with_creatives:
                main_folder_path = os.path.join(project_path, main_folder)
                
                if main_folder == "animate":
                    # Для animate: animate/Площадка/Креатив
                    for platform in platforms:
                        platform_path = os.path.join(main_folder_path, platform)
                        for creative in creatives:
                            creative_path = os.path.join(platform_path, creative)
                            os.makedirs(creative_path, exist_ok=True)
                else:
                    # Для остальных папок: папка/Креатив
                    for creative in creatives:
                        creative_path = os.path.join(main_folder_path, creative)
                        os.makedirs(creative_path, exist_ok=True)
            
            # Создаём пустую папку publish
            publish_path = os.path.join(project_path, publish_folder)
            os.makedirs(publish_path, exist_ok=True)
            
            self.log(f"\n✅ Проект '{project_name}' успешно создан!")
            self.log(f"📍 Путь: {project_path}")
            self.log(f"📁 Площадки ({len(platforms)}): {', '.join(platforms)}")
            self.log(f"📁 Креативы ({len(creatives)}): {', '.join(creatives)}")
            self.log(f"📁 Папка 'publish' создана и оставлена пустой")
            
            # Обновляем текущий проект в главном окне
            if self.update_project_callback:
                self.update_project_callback(project_path)
            
            # Показываем сообщение об успехе
            QMessageBox.information(self, "Успех", f"Проект '{project_name}' успешно создан!\n\nПуть: {project_path}")
            
        except Exception as e:
            self.log(f"❌ Ошибка создания проекта: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка создания проекта:\n{str(e)}")
    
    def apply_styles(self):
        """Применяем стили для карточек и кнопок"""
        self.setStyleSheet("""
            QFrame#card {
                background-color: #1E1E1E;
                border-radius: 12px;
                padding: 15px;
            }
            
            QLabel#card_title {
                color: #4CAF50;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            QLineEdit {
                background-color: #2A2A2A;
                color: #FFFFFF;
                border: 1px solid #3A3A3A;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
            }
            
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
            
            QPushButton#add_btn {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 18px;
                font-size: 20px;
                font-weight: bold;
            }
            
            QPushButton#add_btn:hover {
                background-color: #45a049;
            }
            
            QPushButton#remove_btn {
                background-color: #FF453A;
                color: white;
                border: none;
                border-radius: 18px;
                font-size: 20px;
                font-weight: bold;
            }
            
            QPushButton#remove_btn:hover {
                background-color: #E03A2E;
            }
            
            QPushButton#create_btn {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            
            QPushButton#create_btn:hover {
                background-color: #45a049;
            }
        """)