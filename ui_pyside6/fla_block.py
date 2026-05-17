"""
Блок "FLA операции" - поиск и открытие .fla файлов (полная копия логики из Flet)
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QFileDialog
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer


class FlaSearchThread(QThread):
    """Поток для поиска и открытия .fla файлов"""
    
    log_signal = Signal(str)
    progress_signal = Signal(int, str)
    finished_signal = Signal(dict)
    
    def __init__(self, folder_path, size=None, open_all=False, log_callback=None):
        super().__init__()
        self.folder_path = folder_path
        self.size = size
        self.open_all = open_all
        self.log_callback = log_callback
    
    def log(self, message):
        self.log_signal.emit(message)
        if self.log_callback:
            self.log_callback(message)
    
    def find_fla_files(self, folder_path, size=None):
        """Поиск .fla файлов в папке"""
        found_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if size:
                    if file == f"{size}.fla":
                        found_files.append(os.path.join(root, file))
                elif file.endswith('.fla'):
                    found_files.append(os.path.join(root, file))
        return found_files
    
    def run(self):
        try:
            if self.open_all:
                self.log(f"\n🔍 ПОИСК ВСЕХ .fla в папке: {self.folder_path}")
            else:
                self.log(f"\n🔍 ПОИСК {self.size}.fla в папке: {self.folder_path}")
            
            # Поиск файлов
            found_files = self.find_fla_files(self.folder_path, self.size if not self.open_all else None)
            total_found = len(found_files)
            
            if total_found == 0:
                if self.open_all:
                    self.log("❌ .fla файлы не найдены")
                else:
                    self.log(f"❌ Файл {self.size}.fla не найден")
                self.finished_signal.emit({'total': 0, 'opened': 0})
                return
            
            self.log(f"📁 Найдено файлов: {total_found}")
            
            # Открываем файлы
            opened = 0
            for idx, file_path in enumerate(found_files):
                progress = int((idx / total_found) * 100)
                self.progress_signal.emit(progress, f"Открытие: {os.path.basename(file_path)}")
                
                try:
                    os.startfile(file_path)
                    self.log(f"  ✅ Открыт: {os.path.basename(file_path)}")
                    opened += 1
                except Exception as e:
                    self.log(f"  ❌ Ошибка: {os.path.basename(file_path)} - {str(e)}")
                
                self.msleep(50)
            
            self.log(f"\n✅ Открыто файлов: {opened} из {total_found}")
            
            self.finished_signal.emit({
                'total': total_found,
                'opened': opened
            })
            
        except Exception as e:
            self.log(f"❌ Ошибка: {str(e)}")
            self.finished_signal.emit({'error': str(e)})


class FlaBlock(QWidget):
    """Вкладка FLA операций"""
    
    def __init__(self, project_path, log_callback=None, update_status_callback=None):
        super().__init__()
        self.project_path = project_path
        self.log_callback = log_callback
        self.update_status_callback = update_status_callback
        self.search_thread = None
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок
        title = QLabel("FLA операции")
        title.setObjectName("block_title")
        layout.addWidget(title)
        
        # Поле для размера
        size_layout = QHBoxLayout()
        size_layout.setSpacing(10)
        size_layout.addWidget(QLabel("Размер файла:"))
        
        self.size_input = QLineEdit("240x400")
        self.size_input.setPlaceholderText("например, 240x400")
        self.size_input.setFixedWidth(200)
        size_layout.addWidget(self.size_input)
        size_layout.addStretch()
        
        layout.addLayout(size_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.search_by_size_btn = QPushButton("Открыть .fla по размеру")
        self.search_by_size_btn.setObjectName("search_btn")
        self.search_by_size_btn.clicked.connect(self.search_by_size)
        buttons_layout.addWidget(self.search_by_size_btn, 1)
        
        self.search_all_btn = QPushButton("Открыть все .fla")
        self.search_all_btn.setObjectName("search_all_btn")
        self.search_all_btn.clicked.connect(self.search_all)
        buttons_layout.addWidget(self.search_all_btn, 1)
        
        layout.addLayout(buttons_layout)
        
        # Прогресс-бар
        self.progress_bar = QPushButton()
        self.progress_bar.setVisible(False)
        self.progress_bar.setObjectName("progress_bar")
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        self.progress_label.setObjectName("progress_label")
        layout.addWidget(self.progress_label)
        
        # Статус
        self.status_text = QLabel("Готов к поиску")
        self.status_text.setObjectName("status_text")
        layout.addWidget(self.status_text)
        
        # Подсказка
        hint_frame = QFrame()
        hint_frame.setObjectName("hint_frame")
        hint_layout = QVBoxLayout(hint_frame)
        
        hint_title = QLabel("💡 Информация:")
        hint_title.setObjectName("hint_title")
        hint_layout.addWidget(hint_title)
        
        hints = [
            "   • 'Открыть .fla по размеру' — ищет файл с точным названием (например, 240x400.fla)",
            "   • 'Открыть все .fla' — открывает все .fla файлы в выбранной папке",
            "   • Файлы открываются в программе, ассоциированной с .fla (обычно Adobe Animate)"
        ]
        for hint in hints:
            hint_label = QLabel(hint)
            hint_label.setObjectName("hint_text")
            hint_layout.addWidget(hint_label)
        
        layout.addWidget(hint_frame)
        layout.addStretch()
    
    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
    
    def update_status(self, text):
        self.status_text.setText(text)
        if self.update_status_callback:
            self.update_status_callback(text)
    
    def select_folder(self):
        """Открывает диалог выбора папки"""
        initial_dir = self.project_path if self.project_path and os.path.exists(self.project_path) else ""
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для поиска",
            initial_dir,
            QFileDialog.ShowDirsOnly
        )
        
        if folder:
            return folder
        else:
            self.log("Выбор папки отменён")
            return None
    
    def search_by_size(self):
        """Поиск и открытие .fla по размеру"""
        size = self.size_input.text().strip()
        if not size:
            self.log("Введите размер файла!")
            return
        
        if not self.project_path or not os.path.exists(self.project_path):
            self.log("❌ Сначала выберите рабочую папку!")
            return
        
        # Предлагаем выбрать папку для поиска
        folder = self.select_folder()
        if not folder:
            return
        
        self.start_search(folder, size=size, open_all=False)
    
    def search_all(self):
        """Поиск и открытие всех .fla файлов"""
        if not self.project_path or not os.path.exists(self.project_path):
            self.log("❌ Сначала выберите рабочую папку!")
            return
        
        # Предлагаем выбрать папку для поиска
        folder = self.select_folder()
        if not folder:
            return
        
        self.start_search(folder, open_all=True)
    
    def start_search(self, folder, size=None, open_all=False):
        """Запускает поиск в отдельном потоке"""
        if self.search_thread and self.search_thread.isRunning():
            self.log("Операция уже выполняется, подождите...")
            return
        
        # Блокируем кнопки
        self.search_by_size_btn.setEnabled(False)
        self.search_all_btn.setEnabled(False)
        
        # Показываем прогресс
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_label.setText("Поиск файлов...")
        
        # Запускаем поток
        self.search_thread = FlaSearchThread(folder, size, open_all, self.log_callback)
        self.search_thread.log_signal.connect(self.log)
        self.search_thread.progress_signal.connect(self.update_progress)
        self.search_thread.finished_signal.connect(self.on_search_finished)
        self.search_thread.start()
    
    def update_progress(self, value, text):
        self.progress_label.setText(text)
    
    def on_search_finished(self, result):
        # Разблокируем кнопки
        self.search_by_size_btn.setEnabled(True)
        self.search_all_btn.setEnabled(True)
        
        if 'error' in result:
            self.update_status(f"Ошибка: {result['error']}")
        else:
            opened = result.get('opened', 0)
            total = result.get('total', 0)
            self.update_status(f"Открыто {opened} из {total} файлов")
        
        # Скрываем прогресс через 2 секунды
        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))
        QTimer.singleShot(2000, lambda: self.progress_label.setVisible(False))
    
    def update_project_path(self, new_path):
        """Обновляет путь проекта"""
        self.project_path = new_path
        self.log(f"📂 Путь проекта обновлён: {new_path}")
    
    def apply_styles(self):
        self.setStyleSheet("""
            QLabel#block_title {
                font-size: 18px;
                font-weight: bold;
                color: #4CAF50;
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
            
            QPushButton#search_btn {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton#search_btn:hover {
                background-color: #45a049;
            }
            
            QPushButton#search_all_btn {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton#search_all_btn:hover {
                background-color: #1976D2;
            }
            
            QPushButton#search_btn:disabled, QPushButton#search_all_btn:disabled {
                background-color: #666;
            }
            
            QPushButton#progress_bar {
                background-color: #2A2A2A;
                border: 1px solid #3A3A3A;
                border-radius: 4px;
                text-align: center;
                color: white;
                min-height: 20px;
            }
            
            QLabel#status_text {
                color: #888888;
                font-size: 12px;
                margin-top: 10px;
            }
            
            QFrame#hint_frame {
                background-color: #1A1A1A;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
            }
            
            QLabel#hint_title {
                color: #FFA500;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            QLabel#hint_text {
                color: #666666;
                font-size: 11px;
            }
            
            QLabel#progress_label {
                color: #4CAF50;
                font-size: 11px;
            }
        """)