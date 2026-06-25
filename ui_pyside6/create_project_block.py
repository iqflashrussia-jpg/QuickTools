# ui_pyside6/create_project_block.py
"""
Блок "Создание проекта" - создание структуры проекта с динамическими списками
"""

import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ui_pyside6.common_widgets import CreativeRow, PlatformRow
from ui_pyside6.icons_utils import set_icon
from ui_pyside6.shadow_utils import add_card_shadow
from ui_pyside6.styles import apply_styles


class CreateProjectBlock(QWidget):
    """Вкладка создания структуры проекта"""
    
    def __init__(self, project_path, log_callback=None, update_project_callback=None):
        super().__init__()
        self.project_path = project_path
        self.log_callback = log_callback
        self.update_project_callback = update_project_callback
        
        self.platform_rows = []
        self.creative_rows = []
        
        self.setup_ui()
        apply_styles(self)
        
        # Добавляем тени карточкам
        for card in self.cards:
            add_card_shadow(card)
        
        # Добавляем начальные строки
        self.add_platform_row("Master")
        self.add_creative_row("creative")
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Список для хранения карточек (чтобы добавить тени)
        self.cards = []
        
        # Область с прокруткой
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        
        # === ДОБАВЛЯЕМ ТЕНЬ НА КОНТЕНТ ===
        from PySide6.QtGui import QColor
        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)           # Мягкость тени
        shadow.setXOffset(0)                # Смещение по X
        shadow.setYOffset(6)                # Смещение по Y (вниз)
        shadow.setColor(QColor(0, 0, 0, 100))  # Чёрный с прозрачностью
        scroll_content.setGraphicsEffect(shadow)
        scroll_content.setAttribute(Qt.WA_StyledBackground, True)
        # === КОНЕЦ ===
        
        # ========== КАРТОЧКА 1: Название проекта ==========
        project_card = QFrame()
        project_card.setObjectName("card")
        project_card.setAttribute(Qt.WA_StyledBackground, True)  # ВАЖНО
        self.cards.append(project_card)

        # === ПРИНУДИТЕЛЬНАЯ ТЕНЬ ===
        from PySide6.QtGui import QColor
        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        test_shadow = QGraphicsDropShadowEffect()
        test_shadow.setBlurRadius(20)
        test_shadow.setXOffset(0)
        test_shadow.setYOffset(8)
        test_shadow.setColor(QColor(0, 255, 0, 200))  # Ярко-зелёная
        project_card.setGraphicsEffect(test_shadow)
        # Не забываем отключить авто-заполнение фона
        project_card.setAutoFillBackground(False)
        # === КОНЕЦ ТЕСТА ===

        project_layout = QVBoxLayout(project_card)
        project_layout.setSpacing(8)
        
        project_title = QLabel("Название проекта")
        project_title.setObjectName("card_title")
        project_layout.addWidget(project_title)
        
        self.project_name_field = QLineEdit("PROD")
        self.project_name_field.setPlaceholderText("Введите название проекта")
        self.project_name_field.setMinimumHeight(36)
        project_layout.addWidget(self.project_name_field)
        
        scroll_layout.addWidget(project_card)
        
        # ========== КАРТОЧКА 2: Площадки ==========
        platforms_card = QFrame()
        platforms_card.setObjectName("card")
        self.cards.append(platforms_card)
        platforms_layout = QVBoxLayout(platforms_card)
        platforms_layout.setSpacing(8)
        
        platforms_title = QLabel("Площадки")
        platforms_title.setObjectName("card_title")
        platforms_layout.addWidget(platforms_title)
        
        self.platforms_container = QVBoxLayout()
        self.platforms_container.setSpacing(8)
        platforms_layout.addLayout(self.platforms_container)
        
        scroll_layout.addWidget(platforms_card)
        
        # ========== КАРТОЧКА 3: Названия креативов ==========
        creatives_card = QFrame()
        creatives_card.setObjectName("card")
        self.cards.append(creatives_card)
        creatives_layout = QVBoxLayout(creatives_card)
        creatives_layout.setSpacing(8)
        
        creatives_title = QLabel("Названия креативов")
        creatives_title.setObjectName("card_title")
        creatives_layout.addWidget(creatives_title)
        
        self.creatives_container = QVBoxLayout()
        self.creatives_container.setSpacing(8)
        creatives_layout.addLayout(self.creatives_container)
        
        scroll_layout.addWidget(creatives_card)
        
        # ========== КНОПКА СОЗДАНИЯ ==========
        self.create_btn = QPushButton("СОЗДАТЬ")
        self.create_btn.setObjectName("create_btn")
        set_icon(self.create_btn, 'plus', 16)
        self.create_btn.setMinimumHeight(40)
        self.create_btn.clicked.connect(self.create_structure)
        scroll_layout.addWidget(self.create_btn)
        
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
    
    def add_platform_row(self, value="Master"):
        """Добавляет новую строку для ввода площадки"""
        row = PlatformRow(value, self.add_platform_row, self.remove_platform_row)
        self.platforms_container.addWidget(row)
        self.platform_rows.append(row)
    
    def remove_platform_row(self, row):
        """Удаляет строку площадки"""
        row.deleteLater()
        self.platform_rows.remove(row)
    
    def add_creative_row(self, value="creative"):
        """Добавляет новую строку для ввода креатива"""
        row = CreativeRow(value, self.add_creative_row, self.remove_creative_row)
        self.creatives_container.addWidget(row)
        self.creative_rows.append(row)
    
    def remove_creative_row(self, row):
        """Удаляет строку креатива"""
        row.deleteLater()
        self.creative_rows.remove(row)
    
    def get_platforms(self):
        """Возвращает список всех площадок"""
        platforms = []
        for row in self.platform_rows:
            val = row.get_value()
            if val:
                platforms.append(val)
        return platforms
    
    def get_creatives(self):
        """Возвращает список всех креативов"""
        creatives = []
        for row in self.creative_rows:
            val = row.get_value()
            if val:
                creatives.append(val)
        return creatives
    
    def log(self, message):
        """Отправляет сообщение в лог"""
        if self.log_callback:
            self.log_callback(message)
    
    def create_structure(self):
        """Создаёт структуру папок проекта"""
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
        
        folders_with_creatives = ["animate", "ai", "img", "opt_img", "psd", "screen"]
        publish_folder = "publish"
        
        try:
            os.makedirs(project_path, exist_ok=True)
            
            for main_folder in folders_with_creatives:
                main_folder_path = os.path.join(project_path, main_folder)
                
                if main_folder == "animate":
                    for platform in platforms:
                        platform_path = os.path.join(main_folder_path, platform)
                        for creative in creatives:
                            creative_path = os.path.join(platform_path, creative)
                            os.makedirs(creative_path, exist_ok=True)
                else:
                    for creative in creatives:
                        creative_path = os.path.join(main_folder_path, creative)
                        os.makedirs(creative_path, exist_ok=True)
            
            publish_path = os.path.join(project_path, publish_folder)
            os.makedirs(publish_path, exist_ok=True)
            
            self.log(f"\n✅ Проект '{project_name}' успешно создан!")
            self.log(f"📍 Путь: {project_path}")
            self.log(f"📁 Площадки ({len(platforms)}): {', '.join(platforms)}")
            self.log(f"📁 Креативы ({len(creatives)}): {', '.join(creatives)}")
            self.log(f"📁 Папка 'publish' создана и оставлена пустой")
            
            if self.update_project_callback:
                self.update_project_callback(project_path)
            
            QMessageBox.information(self, "Успех", f"Проект '{project_name}' успешно создан!\n\nПуть: {project_path}")
            
        except Exception as e:
            self.log(f"❌ Ошибка создания проекта: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка создания проекта:\n{str(e)}")