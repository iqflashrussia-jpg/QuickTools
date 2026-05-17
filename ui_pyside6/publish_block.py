# ui_pyside6/publish_block.py
"""
Блок "Publish" - создание структуры внутри папки publish.
Структура: проект/подканал/площадка/креатив
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea, QFrame,
    QMessageBox
)
from PySide6.QtCore import Qt

from ui_pyside6.styles import apply_styles
from ui_pyside6.icons_utils import set_icon
from ui_pyside6.common_widgets import PlatformRow, CreativeRow


class SubchannelCard(QWidget):
    """
    Карточка подканала с его площадками.
    Уникальный виджет для вкладки "Публикация"
    """
    
    def __init__(self, subchannel_name="5_Context_Media", on_add_subchannel=None, on_remove_subchannel=None):
        super().__init__()
        self.on_add_subchannel = on_add_subchannel
        self.on_remove_subchannel = on_remove_subchannel
        self.platform_rows = []
        
        self.setup_ui(subchannel_name)
    
    def setup_ui(self, subchannel_name):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.card_frame = QFrame()
        self.card_frame.setObjectName("subchannel_card")
        layout = QVBoxLayout(self.card_frame)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Верхняя строка: название подканала и кнопки
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        self.name_field = QLineEdit(subchannel_name)
        self.name_field.setPlaceholderText("Название подканала")
        self.name_field.setMinimumHeight(32)
        header_layout.addWidget(self.name_field, 1)
        
        self.remove_card_btn = QPushButton()
        set_icon(self.remove_card_btn, 'minus', 16)
        self.remove_card_btn.setObjectName("remove_btn")
        self.remove_card_btn.setFixedSize(28, 28)
        self.remove_card_btn.clicked.connect(self._on_remove_card)
        header_layout.addWidget(self.remove_card_btn)
        
        self.add_card_btn = QPushButton()
        set_icon(self.add_card_btn, 'plus', 16)
        self.add_card_btn.setObjectName("add_btn")
        self.add_card_btn.setFixedSize(28, 28)
        self.add_card_btn.clicked.connect(self._on_add_card)
        header_layout.addWidget(self.add_card_btn)
        
        layout.addLayout(header_layout)
        
        # Метка "Площадки"
        platforms_label = QLabel("Площадки:")
        platforms_label.setObjectName("platforms_label")
        layout.addWidget(platforms_label)
        
        # Контейнер для строк площадок
        self.platforms_container = QVBoxLayout()
        self.platforms_container.setSpacing(5)
        layout.addLayout(self.platforms_container)
        
        main_layout.addWidget(self.card_frame)
        
        # Добавляем первую площадку по умолчанию
        self.add_platform_row("Яндекс - Баннеры")
    
    def add_platform_row(self, value="Яндекс - Баннеры"):
        """Добавляет новую строку площадки в этот подканал"""
        row = PlatformRow(value, self.add_platform_row, self.remove_platform_row)
        self.platforms_container.addWidget(row)
        self.platform_rows.append(row)
    
    def remove_platform_row(self, row):
        """Удаляет строку площадки из этого подканала"""
        row.deleteLater()
        self.platform_rows.remove(row)
    
    def get_platforms(self):
        """Возвращает список всех площадок в этом подканале"""
        platforms = []
        for row in self.platform_rows:
            val = row.get_value()
            if val:
                platforms.append(val)
        return platforms
    
    def get_name(self):
        """Возвращает название подканала"""
        return self.name_field.text().strip()
    
    def _on_remove_card(self):
        """Удаляет эту карточку подканала"""
        if self.on_remove_subchannel:
            self.on_remove_subchannel(self)
    
    def _on_add_card(self):
        """Добавляет новый подканал"""
        if self.on_add_subchannel:
            self.on_add_subchannel()


class PublishBlock(QWidget):
    """Вкладка публикации - создание структуры в папке publish"""
    
    def __init__(self, project_path, log_callback=None):
        super().__init__()
        self.project_path = project_path
        self.log_callback = log_callback
        self.subchannel_cards = []
        self.creative_rows = []
        
        self.setup_ui()
        apply_styles(self)
        
        # Добавляем начальные элементы
        self.add_subchannel_card("5_Context_Media")
        self.add_creative_row("creative")
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Область с прокруткой (стили берутся из styles.py)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        
        # ========== КАРТОЧКА 1: Название проекта ==========
        project_card = QFrame()
        project_card.setObjectName("card")
        project_layout = QVBoxLayout(project_card)
        project_layout.setSpacing(8)
        
        project_title = QLabel("Название проекта")
        project_title.setObjectName("card_title")
        project_layout.addWidget(project_title)
        
        self.project_name_field = QLineEdit("PROD")
        self.project_name_field.setPlaceholderText("Название проекта")
        self.project_name_field.setMinimumHeight(36)
        project_layout.addWidget(self.project_name_field)
        
        scroll_layout.addWidget(project_card)
        
        # ========== КАРТОЧКА 2: Подканалы и площадки ==========
        subchannels_card = QFrame()
        subchannels_card.setObjectName("card")
        subchannels_layout = QVBoxLayout(subchannels_card)
        subchannels_layout.setSpacing(8)
        
        subchannels_title = QLabel("Подканалы и площадки")
        subchannels_title.setObjectName("card_title")
        subchannels_layout.addWidget(subchannels_title)
        
        # Кнопка добавления подканала
        add_subchannel_layout = QHBoxLayout()
        add_subchannel_layout.addStretch()
        self.add_subchannel_btn = QPushButton("+ Добавить подканал")
        self.add_subchannel_btn.setObjectName("add_subchannel_btn")
        self.add_subchannel_btn.clicked.connect(lambda: self.add_subchannel_card())
        add_subchannel_layout.addWidget(self.add_subchannel_btn)
        subchannels_layout.addLayout(add_subchannel_layout)
        
        # Контейнер для карточек подканалов
        self.subchannels_container = QVBoxLayout()
        self.subchannels_container.setSpacing(8)
        subchannels_layout.addLayout(self.subchannels_container)
        
        scroll_layout.addWidget(subchannels_card)
        
        # ========== КАРТОЧКА 3: Названия креативов ==========
        creatives_card = QFrame()
        creatives_card.setObjectName("card")
        creatives_layout = QVBoxLayout(creatives_card)
        creatives_layout.setSpacing(8)
        
        creatives_title = QLabel("Названия креативов")
        creatives_title.setObjectName("card_title")
        creatives_layout.addWidget(creatives_title)
        
        # Кнопка добавления креатива
        add_creative_layout = QHBoxLayout()
        add_creative_layout.addStretch()
        self.add_creative_btn = QPushButton("+ Добавить креатив")
        self.add_creative_btn.setObjectName("add_creative_btn")
        self.add_creative_btn.clicked.connect(lambda: self.add_creative_row())
        add_creative_layout.addWidget(self.add_creative_btn)
        creatives_layout.addLayout(add_creative_layout)
        
        # Контейнер для строк креативов
        self.creatives_container = QVBoxLayout()
        self.creatives_container.setSpacing(5)
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
        layout.addWidget(scroll)
    
    def add_subchannel_card(self, value="5_Context_Media"):
        """Добавляет новую карточку подканала"""
        card = SubchannelCard(value, self.add_subchannel_card, self.remove_subchannel_card)
        self.subchannels_container.addWidget(card)
        self.subchannel_cards.append(card)
    
    def remove_subchannel_card(self, card):
        """Удаляет карточку подканала"""
        card.deleteLater()
        self.subchannel_cards.remove(card)
    
    def add_creative_row(self, value="creative"):
        """Добавляет новую строку креатива"""
        row = CreativeRow(value, self.add_creative_row, self.remove_creative_row)
        self.creatives_container.addWidget(row)
        self.creative_rows.append(row)
    
    def remove_creative_row(self, row):
        """Удаляет строку креатива"""
        row.deleteLater()
        self.creative_rows.remove(row)
    
    def log(self, message):
        """Отправляет сообщение в лог"""
        if self.log_callback:
            self.log_callback(message)
    
    def create_structure(self):
        """Создаёт структуру папок публикации внутри проекта"""
        # Проверяем, выбран ли проект
        if not self.project_path or not os.path.exists(self.project_path):
            self.log("❌ Сначала выберите рабочую папку с проектом или создайте проект!")
            QMessageBox.warning(self, "Ошибка", "Сначала выберите рабочую папку с проектом или создайте проект!")
            return
        
        # Проверяем название проекта
        project_name = self.project_name_field.text().strip()
        if not project_name:
            self.log("❌ Введите название проекта!")
            QMessageBox.warning(self, "Ошибка", "Введите название проекта!")
            return
        
        # Собираем данные по подканалам
        subchannels = []
        for card in self.subchannel_cards:
            subchannel_name = card.get_name()
            if not subchannel_name:
                self.log("❌ Название подканала не может быть пустым!")
                QMessageBox.warning(self, "Ошибка", "Название подканала не может быть пустым!")
                return
            
            platforms = card.get_platforms()
            if not platforms:
                self.log(f"❌ Для подканала '{subchannel_name}' добавьте хотя бы одну площадку!")
                QMessageBox.warning(self, "Ошибка", f"Для подканала '{subchannel_name}' добавьте хотя бы одну площадку!")
                return
            
            subchannels.append({
                "name": subchannel_name,
                "platforms": platforms
            })
        
        if not subchannels:
            self.log("❌ Добавьте хотя бы один подканал!")
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один подканал!")
            return
        
        # Собираем названия креативов
        creatives = []
        for row in self.creative_rows:
            val = row.get_value()
            if val:
                creatives.append(val)
        
        if not creatives:
            self.log("❌ Добавьте хотя бы одно название креатива!")
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы одно название креатива!")
            return
        
        # Создаём структуру папок
        try:
            publish_path = os.path.join(self.project_path, "publish", project_name)
            os.makedirs(publish_path, exist_ok=True)
            
            created_count = 0
            for subchannel in subchannels:
                subchannel_path = os.path.join(publish_path, subchannel["name"])
                for platform in subchannel["platforms"]:
                    platform_path = os.path.join(subchannel_path, platform)
                    for creative in creatives:
                        creative_path = os.path.join(platform_path, creative)
                        os.makedirs(creative_path, exist_ok=True)
                        created_count += 1
            
            self.log(f"\n✅ Структура публикации успешно создана!")
            self.log(f"📍 Путь: {publish_path}")
            self.log(f"📁 Проект: {project_name}")
            self.log(f"📁 Подканалы ({len(subchannels)}):")
            for sub in subchannels:
                self.log(f"     - {sub['name']} → площадки: {', '.join(sub['platforms'])}")
            self.log(f"📁 Креативы ({len(creatives)}): {', '.join(creatives)}")
            self.log(f"📁 Создано папок: {created_count}")
            
            QMessageBox.information(self, "Успех", f"Структура публикации успешно создана!\n\nПуть: {publish_path}")
            
        except Exception as e:
            self.log(f"❌ Ошибка создания структуры: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка создания структуры:\n{str(e)}")
    
    def update_project_path(self, new_path):
        """Обновляет путь текущего проекта (вызывается из главного окна)"""
        self.project_path = new_path
        self.log(f"📂 Путь проекта обновлён: {new_path}")