"""
Главный экран с вкладками инструментов
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QFileDialog, QTextEdit,
    QSlider, QLineEdit, QCheckBox, QGroupBox, QGridLayout
)
from PySide6.QtCore import Qt


class MainTabs(QWidget):
    """Главный экран с вкладками"""
    
    def __init__(self, project_path, log_callback=None):
        super().__init__()
        self.project_path = project_path  # может быть None для нового проекта
        self.log_callback = log_callback
        
        self.setup_ui()
        self.apply_styles()
        
        # Если это создание нового проекта (project_path = None)
        if project_path is None:
            self.add_log("🆕 Режим создания нового проекта")
    
    def add_log(self, message):
        """Добавить сообщение в лог"""
        # Выводим в консоль (для отладки)
        print(message)
        
        # Выводим в GUI-лог
        if hasattr(self, 'log'):
            self.log.append(message)
        
        # Также вызываем внешний callback если есть
        if self.log_callback:
            self.log_callback(message)
    
    def update_status(self, text):
        """Обновляет статус (заглушка для совместимости)"""
        pass
    
    def update_project_path(self, new_path):
        """Обновляет путь текущего проекта"""
        self.project_path = new_path
        self.project_label.setText(new_path)
        self.add_log(f"📂 Текущий проект обновлён: {new_path}")
        
        # Обновляем путь во всех блоках
        if hasattr(self, 'optimizer_block'):
            self.optimizer_block.project_path = new_path
        if hasattr(self, 'archiver_block'):
            self.archiver_block.update_project_path(new_path)
        if hasattr(self, 'fla_block'):
            self.fla_block.update_project_path(new_path)
        if hasattr(self, 'rename_block'):
            self.rename_block.update_project_path(new_path)
        if hasattr(self, 'publish_block'):
            self.publish_block.update_project_path(new_path)
    
    def setup_ui(self):
        """Создаём интерфейс с вкладками"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Верхняя панель с названием проекта
        top_panel = QHBoxLayout()
        top_panel.addWidget(QLabel("📂 Текущий проект:"))
        
        project_text = self.project_path if self.project_path else "(новый проект)"
        self.project_label = QLabel(project_text)
        self.project_label.setObjectName("project_path")
        self.project_label.setWordWrap(True)
        top_panel.addWidget(self.project_label, 1)
        
        # Кнопка смены проекта
        self.change_btn = QPushButton("Сменить проект")
        self.change_btn.setObjectName("change_btn")
        top_panel.addWidget(self.change_btn)
        
        layout.addLayout(top_panel)
        
        # Создаём вкладки
        self.tabs = QTabWidget()
        self.tabs.setObjectName("main_tabs")
        
        # Добавляем все 6 вкладок
        self.tabs.addTab(self.create_project_tab(), "📁 Создание проекта")
        self.tabs.addTab(self.create_publish_tab(), "📤 Публикация")
        self.tabs.addTab(self.create_optimizer_tab(), "📦 Оптимизация")
        self.tabs.addTab(self.create_archiver_tab(), "🗜 Архивация")
        self.tabs.addTab(self.create_fla_tab(), "🎬 FLA операции")
        self.tabs.addTab(self.create_rename_tab(), "✏️ Переименование")
        
        layout.addWidget(self.tabs, 1)
        
        # Нижняя панель с логом
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(150)
        self.log.setObjectName("log")
        layout.addWidget(self.log)
    
    def create_project_tab(self):
        """Вкладка создания структуры проекта"""
        from ui_pyside6.create_project_block import CreateProjectBlock
        
        self.create_project_block = CreateProjectBlock(
            self.project_path, 
            self.add_log,
            self.update_project_path
        )
        return self.create_project_block
    
    def create_publish_tab(self):
        """Вкладка публикации"""
        from ui_pyside6.publish_block import PublishBlock
        
        self.publish_block = PublishBlock(self.project_path, self.add_log)
        return self.publish_block
    
    def create_optimizer_tab(self):
        """Вкладка оптимизации изображений"""
        from ui_pyside6.optimizer_block import OptimizerBlock
        
        self.optimizer_block = OptimizerBlock(self.project_path, self.add_log)
        return self.optimizer_block
    
    def create_archiver_tab(self):
        """Вкладка архивации"""
        from ui_pyside6.archiver_block import ArchiverBlock
        
        self.archiver_block = ArchiverBlock(self.project_path, self.add_log)
        return self.archiver_block
    
    def create_fla_tab(self):
        """Вкладка FLA операций"""
        from ui_pyside6.fla_block import FlaBlock
        
        self.fla_block = FlaBlock(self.project_path, self.add_log, self.update_status)
        return self.fla_block
    
    def create_rename_tab(self):
        """Вкладка пакетного переименования"""
        from ui_pyside6.rename_block import RenameBlock
        
        self.rename_block = RenameBlock(self.project_path, self.add_log)
        return self.rename_block
    
    def apply_styles(self):
        """CSS стили"""
        self.setStyleSheet("""
            QTabWidget::pane {
                background-color: #1E1E1E;
                border-radius: 8px;
                border: 1px solid #2A2A2A;
            }
            
            QTabBar::tab {
                background-color: #2A2A2A;
                color: #FFFFFF;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            
            QTabBar::tab:selected {
                background-color: #4CAF50;
            }
            
            QTabBar::tab:hover {
                background-color: #3A3A3A;
            }
            
            QGroupBox {
                color: #FFFFFF;
                border: 1px solid #3A3A3A;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            
            QPushButton#run_btn {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton#run_btn:hover {
                background-color: #45a049;
            }
            
            QPushButton#change_btn {
                background-color: #3A3A3A;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
            }
            
            QLineEdit, QSlider {
                background-color: #2A2A2A;
                color: white;
                border: 1px solid #3A3A3A;
                border-radius: 4px;
                padding: 5px;
            }
            
            QTextEdit#log {
                background-color: #1A1A1A;
                color: #00FF00;
                border: 1px solid #3A3A3A;
                border-radius: 6px;
                font-family: monospace;
            }
            
            QCheckBox {
                color: #FFFFFF;
            }
            
            QLabel#project_path {
                color: #4CAF50;
                font-family: monospace;
            }
        """)