"""
Блок "Архивация" - создание ZIP архивов для папок с размерами
"""

import os
import shutil
import zipfile

from PySide6.QtCore import Qt, QThread, QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui_pyside6.styles import apply_styles


class ArchiverThread(QThread):
    progress_update = Signal(int, str)
    log_signal = Signal(str)
    finished_signal = Signal(dict)
    
    def __init__(self, project_path, log_callback):
        super().__init__()
        self.project_path = project_path
        self.log_callback = log_callback
    
    def log(self, message):
        self.log_signal.emit(message)
        if self.log_callback:
            self.log_callback(message)
    
    def find_size_folders(self, base_path):
        """Рекурсивно находит все папки с 'x' в имени внутри папки animate"""
        folders = []
        if not os.path.exists(base_path):
            return folders
        
        animate_path = os.path.join(base_path, "animate")
        if not os.path.exists(animate_path):
            self.log(f"⚠️ Папка animate не найдена: {animate_path}")
            return folders
        
        self.log(f"🔍 Рекурсивное сканирование: {animate_path}")
        
        for root, dirs, files in os.walk(animate_path):
            for dir_name in dirs:
                if 'x' in dir_name.lower():
                    folder_path = os.path.join(root, dir_name)
                    rel_path = os.path.relpath(root, animate_path)
                    parts = rel_path.split(os.sep) if rel_path != '.' else []
                    platform = parts[0] if len(parts) > 0 else "unknown"
                    campaign = parts[1] if len(parts) > 1 else "unknown"
                    
                    folders.append({
                        'path': folder_path,
                        'platform': platform,
                        'campaign': campaign,
                        'size': dir_name
                    })
                    self.log(f"   ✅ Найдена папка: {platform}/{campaign}/{dir_name}")
        
        self.log(f"📁 Всего найдено папок с 'x': {len(folders)}")
        return folders
    
    def create_archive(self, folder_path, output_path):
        """Создаёт ZIP архив из файлов в папке (исключая .fla)"""
        files_to_zip = []
        folder_size = 0
        
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path) and not file.endswith('.fla'):
                files_to_zip.append(file_path)
                folder_size += os.path.getsize(file_path)
        
        if not files_to_zip:
            return None, 0
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in files_to_zip:
                zf.write(file_path, os.path.basename(file_path))
        
        archive_size = os.path.getsize(output_path)
        return archive_size, folder_size
    
    def run(self):
        try:
            self.log(f"\n{'='*60}")
            self.log(f"📦 АРХИВАЦИЯ ВСЕХ ПАПОК С РАЗМЕРАМИ")
            self.log(f"📁 Папка: {self.project_path}")
            self.log(f"{'='*60}")
            
            size_folders = self.find_size_folders(self.project_path)
            
            if not size_folders:
                self.log("❌ Папки с 'x' в имени не найдены")
                self.finished_signal.emit({'archive_count': 0, 'total': 0})
                return
            
            total = len(size_folders)
            self.log(f"📁 Найдено папок: {total}")
            
            archive_count = 0
            total_before = 0
            total_after = 0
            
            for idx, folder_info in enumerate(size_folders):
                folder_path = folder_info['path']
                platform = folder_info['platform']
                campaign = folder_info['campaign']
                size_name = folder_info['size']
                
                progress_value = int((idx / total) * 100)
                self.progress_update.emit(progress_value, f"{platform}/{campaign}/{size_name} ({idx+1}/{total})")
                
                self.log(f"\n📦 [{idx+1}/{total}] {platform}/{campaign}/{size_name}")
                
                zip_name = f"{size_name}_{campaign}_{platform}.zip"
                zip_output_dir = os.path.join(os.path.dirname(folder_path), "zip")
                zip_path = os.path.join(zip_output_dir, zip_name)
                
                if os.path.exists(zip_path):
                    self.log(f"  ⚠️ Архив уже существует: {zip_name}")
                    continue
                
                archive_size, folder_size = self.create_archive(folder_path, zip_path)
                
                if archive_size:
                    total_before += folder_size
                    total_after += archive_size
                    reduction = (1 - archive_size/folder_size) * 100 if folder_size > 0 else 0
                    self.log(f"  ✅ Создан: {zip_name}")
                    self.log(f"     Размер: {archive_size // 1024} KB (сжатие {reduction:.0f}%)")
                    archive_count += 1
                else:
                    self.log(f"  ⚠️ Нет файлов для архивации (или только .fla)")
                
                self.msleep(50)
            
            total_reduction = (1 - total_after/total_before) * 100 if total_before > 0 else 0
            
            self.log(f"\n{'='*60}")
            self.log(f"✅ АРХИВАЦИЯ ЗАВЕРШЕНА!")
            self.log(f"✅ Создано архивов: {archive_count} из {total}")
            if archive_count > 0:
                self.log(f"📊 Общий размер: {total_before//1024} KB → {total_after//1024} KB")
                self.log(f"📊 Общее сжатие: {total_reduction:.0f}%")
            self.log(f"{'='*60}\n")
            
            self.finished_signal.emit({
                'archive_count': archive_count,
                'total': total,
                'total_before': total_before,
                'total_after': total_after,
                'total_reduction': total_reduction
            })
            
        except Exception as e:
            self.log(f"❌ Ошибка архивации: {str(e)}")
            self.finished_signal.emit({'error': str(e)})


class DeleteArchivesThread(QThread):
    progress_update = Signal(int, str)
    log_signal = Signal(str)
    finished_signal = Signal(dict)
    
    def __init__(self, project_path, log_callback):
        super().__init__()
        self.project_path = project_path
        self.log_callback = log_callback
    
    def log(self, message):
        self.log_signal.emit(message)
        if self.log_callback:
            self.log_callback(message)
    
    def run(self):
        try:
            self.log(f"\n{'='*60}")
            self.log(f"🗑️ УДАЛЕНИЕ ВСЕХ ZIP АРХИВОВ")
            self.log(f"📁 Папка: {self.project_path}")
            self.log(f"{'='*60}")
            
            self.progress_update.emit(0, "Поиск архивов...")
            
            all_zips = []
            all_zip_folders = []
            
            for root, dirs, files in os.walk(self.project_path):
                for file in files:
                    if file.endswith('.zip'):
                        all_zips.append(os.path.join(root, file))
                for dir_name in dirs:
                    if dir_name.lower() == "zip":
                        all_zip_folders.append(os.path.join(root, dir_name))
                self.msleep(10)
            
            total_zips = len(all_zips)
            total_folders = len(all_zip_folders)
            
            if total_zips == 0 and total_folders == 0:
                self.log("❌ Архивы и папки zip не найдены")
                self.finished_signal.emit({'deleted_zips': 0, 'deleted_folders': 0})
                return
            
            self.log(f"📁 Найдено ZIP: {total_zips}, папок zip: {total_folders}")
            
            deleted_zips = 0
            deleted_folders = 0
            
            for idx, file_path in enumerate(all_zips):
                progress_val = int((idx / max(total_zips, 1)) * 80)
                self.progress_update.emit(progress_val, f"Удаление: {os.path.basename(file_path)}")
                try:
                    os.remove(file_path)
                    deleted_zips += 1
                    self.log(f"  ✅ Удалён: {os.path.basename(file_path)}")
                except Exception as e:
                    self.log(f"  ❌ Ошибка: {os.path.basename(file_path)} - {str(e)}")
                self.msleep(10)
            
            for idx, folder_path in enumerate(all_zip_folders):
                progress_val = 80 + int((idx / max(total_folders, 1)) * 20)
                self.progress_update.emit(progress_val, f"Удаление папки: {os.path.basename(folder_path)}")
                try:
                    shutil.rmtree(folder_path)
                    deleted_folders += 1
                    self.log(f"  ✅ Удалена папка: {os.path.basename(folder_path)}")
                except Exception as e:
                    self.log(f"  ❌ Ошибка: {os.path.basename(folder_path)} - {str(e)}")
                self.msleep(10)
            
            self.log(f"\n{'='*60}")
            self.log(f"✅ УДАЛЕНИЕ ЗАВЕРШЕНО!")
            self.log(f"✅ Удалено ZIP: {deleted_zips}, папок zip: {deleted_folders}")
            self.log(f"{'='*60}\n")
            
            self.finished_signal.emit({
                'deleted_zips': deleted_zips,
                'deleted_folders': deleted_folders
            })
            
        except Exception as e:
            self.log(f"❌ Ошибка удаления: {str(e)}")
            self.finished_signal.emit({'error': str(e)})


class ArchiverBlock(QWidget):
    def __init__(self, project_path, log_callback=None):
        super().__init__()
        self.project_path = project_path
        self.log_callback = log_callback
        self.archive_thread = None
        self.delete_thread = None
        
        self.setup_ui()
        apply_styles(self)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Архивация")
        title.setObjectName("block_title")
        layout.addWidget(title)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.archive_btn = QPushButton("АРХИВИРОВАТЬ ВСЕ")
        self.archive_btn.setObjectName("archive_btn")
        from ui_pyside6.icons_utils import set_icon
        set_icon(self.archive_btn, 'archive', 18)
        self.archive_btn.clicked.connect(self.start_archive)
        buttons_layout.addWidget(self.archive_btn, 1)
        
        self.delete_btn = QPushButton("УДАЛИТЬ ВСЕ АРХИВЫ")
        self.delete_btn.setObjectName("delete_btn")
        set_icon(self.delete_btn, 'trash', 18)
        self.delete_btn.clicked.connect(self.start_delete)
        buttons_layout.addWidget(self.delete_btn, 1)
        
        layout.addLayout(buttons_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setObjectName("progress_bar")
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        self.progress_label.setObjectName("progress_label")
        layout.addWidget(self.progress_label)
        
        self.status_text = QLabel("Готов к архивации")
        self.status_text.setObjectName("status_text")
        layout.addWidget(self.status_text)
        
        hint_frame = QFrame()
        hint_frame.setObjectName("hint_frame")
        hint_layout = QVBoxLayout(hint_frame)
        
        hint_title = QLabel("💡 Информация:")
        hint_title.setObjectName("hint_title")
        hint_layout.addWidget(hint_title)
        
        hints = [
            "   • Архивы создаются для папок, содержащих 'x' в имени (размеры)",
            "   • Файлы .fla исключаются из архивов",
            "   • Архивы сохраняются в папку 'zip' рядом с исходной папкой"
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
    
    def start_archive(self):
        if self.archive_thread and self.archive_thread.isRunning():
            self.log("Операция уже выполняется, подождите...")
            return
        
        if not self.project_path or not os.path.exists(self.project_path):
            self.log("❌ Сначала выберите рабочую папку!")
            return
        
        self.archive_btn.setEnabled(False)
        self.archive_btn.setText("⏳ АРХИВАЦИЯ...")
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setVisible(True)
        
        self.archive_thread = ArchiverThread(self.project_path, self.log_callback)
        self.archive_thread.progress_update.connect(self.update_progress)
        self.archive_thread.log_signal.connect(self.log)
        self.archive_thread.finished_signal.connect(self.on_archive_finished)
        self.archive_thread.start()
    
    def on_archive_finished(self, result):
        self.archive_btn.setEnabled(True)
        self.archive_btn.setText("АРХИВИРОВАТЬ ВСЕ")
        
        if 'error' in result:
            self.status_text.setText(f"Ошибка: {result['error']}")
        else:
            archive_count = result.get('archive_count', 0)
            reduction = result.get('total_reduction', 0)
            self.status_text.setText(f"Архивация завершена: {archive_count} архивов, сжатие {reduction:.0f}%")
        
        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))
        QTimer.singleShot(2000, lambda: self.progress_label.setVisible(False))
    
    def start_delete(self):
        if self.delete_thread and self.delete_thread.isRunning():
            self.log("Операция уже выполняется, подождите...")
            return
        
        if not self.project_path or not os.path.exists(self.project_path):
            self.log("❌ Сначала выберите рабочую папку!")
            return
        
        self.delete_btn.setEnabled(False)
        self.delete_btn.setText("⏳ УДАЛЕНИЕ...")
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setVisible(True)
        
        self.delete_thread = DeleteArchivesThread(self.project_path, self.log_callback)
        self.delete_thread.progress_update.connect(self.update_progress)
        self.delete_thread.log_signal.connect(self.log)
        self.delete_thread.finished_signal.connect(self.on_delete_finished)
        self.delete_thread.start()
    
    def on_delete_finished(self, result):
        self.delete_btn.setEnabled(True)
        self.delete_btn.setText("УДАЛИТЬ ВСЕ АРХИВЫ")
        
        if 'error' in result:
            self.status_text.setText(f"Ошибка: {result['error']}")
        else:
            deleted_zips = result.get('deleted_zips', 0)
            deleted_folders = result.get('deleted_folders', 0)
            self.status_text.setText(f"Удалено архивов: {deleted_zips}, папок: {deleted_folders}")
        
        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))
        QTimer.singleShot(2000, lambda: self.progress_label.setVisible(False))
    
    def update_progress(self, value, text):
        self.progress_bar.setValue(value)
        self.progress_label.setText(text)
    
    def update_project_path(self, new_path):
        self.project_path = new_path
        self.log(f"📂 Путь проекта обновлён: {new_path}")