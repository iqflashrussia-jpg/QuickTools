"""
Блок "Пакетное переименование" - замена текста в именах файлов и папок
"""

import os

from PySide6.QtCore import Qt, QThread, QTimer, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui_pyside6.styles import apply_styles


class RenameThread(QThread):
    """Поток для выполнения пакетного переименования"""
    
    log_signal = Signal(str)
    progress_signal = Signal(int, str)
    finished_signal = Signal(dict)
    
    def __init__(self, folder_path, find_text, replace_text, case_sensitive, rename_folders, log_callback=None):
        super().__init__()
        self.folder_path = folder_path
        self.find_text = find_text
        self.replace_text = replace_text
        self.case_sensitive = case_sensitive
        self.rename_folders = rename_folders
        self.log_callback = log_callback
    
    def log(self, message):
        self.log_signal.emit(message)
        if self.log_callback:
            self.log_callback(message)
    
    def find_items_to_rename(self, folder_path):
        """Рекурсивно находит все элементы для переименования"""
        items = []
        
        for root, dirs, files in os.walk(folder_path):
            # Проверяем папки
            if self.rename_folders:
                for dir_name in dirs:
                    if self.case_sensitive:
                        if self.find_text in dir_name:
                            items.append({
                                'path': os.path.join(root, dir_name),
                                'name': dir_name,
                                'is_folder': True
                            })
                    else:
                        if self.find_text.lower() in dir_name.lower():
                            items.append({
                                'path': os.path.join(root, dir_name),
                                'name': dir_name,
                                'is_folder': True
                            })
            
            # Проверяем файлы
            for file_name in files:
                if self.case_sensitive:
                    if self.find_text in file_name:
                        items.append({
                            'path': os.path.join(root, file_name),
                            'name': file_name,
                            'is_folder': False
                        })
                else:
                    if self.find_text.lower() in file_name.lower():
                        items.append({
                            'path': os.path.join(root, file_name),
                            'name': file_name,
                            'is_folder': False
                        })
        
        return items
    
    def run(self):
        try:
            self.log(f"\n{'='*50}")
            self.log(f"📝 ПАКЕТНОЕ ПЕРЕИМЕНОВАНИЕ")
            self.log(f"📁 Папка: {self.folder_path}")
            self.log(f"🔍 Поиск: '{self.find_text}' → Замена: '{self.replace_text}'")
            self.log(f"🔠 Учитывать регистр: {'Да' if self.case_sensitive else 'Нет'}")
            self.log(f"📂 Переименовывать папки: {'Да' if self.rename_folders else 'Нет'}")
            self.log(f"{'='*50}")
            
            items_to_rename = self.find_items_to_rename(self.folder_path)
            total = len(items_to_rename)
            
            if total == 0:
                self.log("⚠️ Нет файлов/папок для переименования")
                self.finished_signal.emit({'renamed': 0, 'errors': 0, 'total': 0})
                return
            
            self.log(f"📁 Найдено элементов для переименования: {total}")
            
            # Сортируем по глубине (сначала обрабатываем глубокие)
            items_to_rename.sort(key=lambda x: x['path'].count(os.sep), reverse=True)
            
            renamed_count = 0
            errors = 0
            
            for idx, item in enumerate(items_to_rename):
                old_path = item['path']
                name = item['name']
                
                if self.case_sensitive:
                    new_name = name.replace(self.find_text, self.replace_text)
                else:
                    new_name = name
                    lower_name = name.lower()
                    lower_find = self.find_text.lower()
                    idx_pos = lower_name.find(lower_find)
                    if idx_pos != -1:
                        new_name = name[:idx_pos] + self.replace_text + name[idx_pos + len(self.find_text):]
                
                if new_name == name:
                    continue
                
                parent_dir = os.path.dirname(old_path)
                new_path = os.path.join(parent_dir, new_name)
                
                progress = int((idx / total) * 100)
                self.progress_signal.emit(progress, f"Переименование: {name}")
                
                if os.path.exists(new_path):
                    self.log(f"  ⚠️ Пропущен: {new_name} уже существует")
                    errors += 1
                    continue
                
                try:
                    os.rename(old_path, new_path)
                    renamed_count += 1
                    self.log(f"  ✅ {name} → {new_name}")
                except Exception as e:
                    self.log(f"  ❌ Ошибка: {name} → {str(e)}")
                    errors += 1
                
                self.msleep(10)
            
            self.log(f"\n{'='*50}")
            self.log(f"✅ ПЕРЕИМЕНОВАНИЕ ЗАВЕРШЕНО!")
            self.log(f"✅ Успешно: {renamed_count}")
            self.log(f"❌ Ошибок: {errors}")
            self.log(f"{'='*50}\n")
            
            self.finished_signal.emit({
                'renamed': renamed_count,
                'errors': errors,
                'total': total
            })
            
        except Exception as e:
            self.log(f"❌ Ошибка: {str(e)}")
            self.finished_signal.emit({'error': str(e)})


class RenameBlock(QWidget):
    """Вкладка пакетного переименования"""
    
    def __init__(self, project_path, log_callback=None):
        super().__init__()
        self.project_path = project_path
        self.log_callback = log_callback
        self.rename_thread = None
        
        self.setup_ui()
        apply_styles(self)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Пакетное переименование")
        title.setObjectName("block_title")
        layout.addWidget(title)
        
        find_layout = QHBoxLayout()
        find_layout.setSpacing(10)
        find_layout.addWidget(QLabel("Искать:"))
        
        self.find_field = QLineEdit()
        self.find_field.setPlaceholderText("Что ищем")
        find_layout.addWidget(self.find_field, 1)
        
        layout.addLayout(find_layout)
        
        replace_layout = QHBoxLayout()
        replace_layout.setSpacing(10)
        replace_layout.addWidget(QLabel("Заменить:"))
        
        self.replace_field = QLineEdit()
        self.replace_field.setPlaceholderText("На что заменяем")
        replace_layout.addWidget(self.replace_field, 1)
        
        layout.addLayout(replace_layout)
        
        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.setSpacing(20)
        
        self.case_sensitive_checkbox = QCheckBox("Учитывать регистр")
        self.case_sensitive_checkbox.setObjectName("checkbox")
        
        self.rename_folders_checkbox = QCheckBox("Переименовывать папки")
        self.rename_folders_checkbox.setObjectName("checkbox")
        
        checkboxes_layout.addWidget(self.case_sensitive_checkbox)
        checkboxes_layout.addWidget(self.rename_folders_checkbox)
        checkboxes_layout.addStretch()
        
        layout.addLayout(checkboxes_layout)
        
        self.rename_btn = QPushButton("ЗАМЕНИТЬ ВСЁ")
        self.rename_btn.setObjectName("rename_btn")
        from ui_pyside6.icons_utils import set_icon
        set_icon(self.rename_btn, 'pencil', 18)
        self.rename_btn.clicked.connect(self.start_rename)
        layout.addWidget(self.rename_btn)
        
        self.progress_bar = QPushButton()
        self.progress_bar.setVisible(False)
        self.progress_bar.setObjectName("progress_bar")
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        self.progress_label.setObjectName("progress_label")
        layout.addWidget(self.progress_label)
        
        self.status_text = QLabel("Готов к переименованию")
        self.status_text.setObjectName("status_text")
        layout.addWidget(self.status_text)
        
        hint_frame = QFrame()
        hint_frame.setObjectName("hint_frame")
        hint_layout = QVBoxLayout(hint_frame)
        
        hint_title = QLabel("💡 Информация:")
        hint_title.setObjectName("hint_title")
        hint_layout.addWidget(hint_title)
        
        hints = [
            "   • Пакетная замена текста в именах файлов и папок (рекурсивно)",
            "   • При замене без учёта регистра сохраняется оригинальный регистр букв"
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
    
    def start_rename(self):
        if self.rename_thread and self.rename_thread.isRunning():
            self.log("Операция уже выполняется, подождите...")
            return
        
        if not self.project_path or not os.path.exists(self.project_path):
            self.log("❌ Сначала выберите рабочую папку!")
            return
        
        find_text = self.find_field.text().strip()
        replace_text = self.replace_field.text().strip()
        
        if not find_text:
            self.log("Введите текст для поиска!")
            return
        
        case_sensitive = self.case_sensitive_checkbox.isChecked()
        rename_folders = self.rename_folders_checkbox.isChecked()
        
        self.rename_btn.setEnabled(False)
        self.rename_btn.setText("⏳ ЗАМЕНА...")
        
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_label.setText("Подготовка...")
        
        self.rename_thread = RenameThread(
            self.project_path,
            find_text,
            replace_text,
            case_sensitive,
            rename_folders,
            self.log_callback
        )
        self.rename_thread.log_signal.connect(self.log)
        self.rename_thread.progress_signal.connect(self.update_progress)
        self.rename_thread.finished_signal.connect(self.on_rename_finished)
        self.rename_thread.start()
    
    def update_progress(self, value, text):
        self.progress_label.setText(text)
    
    def on_rename_finished(self, result):
        self.rename_btn.setEnabled(True)
        self.rename_btn.setText("ЗАМЕНИТЬ ВСЁ")
        
        if 'error' in result:
            self.update_status(f"Ошибка: {result['error']}")
        else:
            renamed = result.get('renamed', 0)
            errors = result.get('errors', 0)
            self.update_status(f"Переименовано: {renamed}, ошибок: {errors}")
        
        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))
        QTimer.singleShot(2000, lambda: self.progress_label.setVisible(False))
    
    def update_project_path(self, new_path):
        self.project_path = new_path
        self.log(f"📂 Путь проекта обновлён: {new_path}")