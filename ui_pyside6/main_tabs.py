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

from ui_pyside6.styles import apply_styles


class MainTabs(QWidget):
    """Главный экран с вкладками"""
    
    def __init__(self, project_path, log_callback=None):
        super().__init__()
        self.project_path = project_path
        self.log_callback = log_callback
        
        self.setup_ui()
        apply_styles(self)
        
        if project_path is None:
            self.add_log("🆕 Режим создания нового проекта")
    
    def add_log(self, message):
        """Добавить сообщение в лог"""
        print(message)
        if hasattr(self, 'log'):
            self.log.append(message)
        if self.log_callback:
            self.log_callback(message)
    
    def update_status(self, text):
        """Обновляет статус (заглушка)"""
        pass
    
    def update_project_path(self, new_path):
        """Обновляет путь текущего проекта"""
        self.project_path = new_path
        self.project_label.setText(new_path)
        self.add_log(f"📂 Текущий проект обновлён: {new_path}")
        
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
        
        top_panel = QHBoxLayout()
        top_panel.addWidget(QLabel("📂 Текущий проект:"))
        
        project_text = self.project_path if self.project_path else "(новый проект)"
        self.project_label = QLabel(project_text)
        self.project_label.setObjectName("project_path")
        self.project_label.setWordWrap(True)
        top_panel.addWidget(self.project_label, 1)
        
        self.change_btn = QPushButton("Сменить проект")
        self.change_btn.setObjectName("change_btn")
        top_panel.addWidget(self.change_btn)
        
        layout.addLayout(top_panel)
        
        self.tabs = QTabWidget()
        self.tabs.setObjectName("main_tabs")
        
        self.tabs.addTab(self.create_project_tab(), "📁 Создание проекта")
        self.tabs.addTab(self.create_publish_tab(), "📤 Публикация")
        self.tabs.addTab(self.create_optimizer_tab(), "📦 Оптимизация")
        self.tabs.addTab(self.create_archiver_tab(), "🗜 Архивация")
        self.tabs.addTab(self.create_fla_tab(), "🎬 FLA операции")
        self.tabs.addTab(self.create_rename_tab(), "✏️ Переименование")
        
        layout.addWidget(self.tabs, 1)
        
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(150)
        self.log.setObjectName("log")
        layout.addWidget(self.log)
    
    def create_project_tab(self):
        from ui_pyside6.create_project_block import CreateProjectBlock
        self.create_project_block = CreateProjectBlock(
            self.project_path, self.add_log, self.update_project_path
        )
        return self.create_project_block
    
    def create_publish_tab(self):
        from ui_pyside6.publish_block import PublishBlock
        self.publish_block = PublishBlock(self.project_path, self.add_log)
        return self.publish_block
    
    def create_optimizer_tab(self):
        from ui_pyside6.optimizer_block import OptimizerBlock
        self.optimizer_block = OptimizerBlock(self.project_path, self.add_log)
        return self.optimizer_block
    
    def create_archiver_tab(self):
        from ui_pyside6.archiver_block import ArchiverBlock
        self.archiver_block = ArchiverBlock(self.project_path, self.add_log)
        return self.archiver_block
    
    def create_fla_tab(self):
        from ui_pyside6.fla_block import FlaBlock
        self.fla_block = FlaBlock(self.project_path, self.add_log, self.update_status)
        return self.fla_block
    
    def create_rename_tab(self):
        from ui_pyside6.rename_block import RenameBlock
        self.rename_block = RenameBlock(self.project_path, self.add_log)
        return self.rename_block