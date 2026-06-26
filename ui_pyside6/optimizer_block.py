"""
Блок "Оптимизация" - подбор качества сжатия изображений под целевой размер архива.
"""

import os
import sys

from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui_pyside6.styles import apply_styles

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modules import image_optimizer, settings_finder


class OptimizerThread(QThread):
    progress_update = Signal(int, str)
    log_signal = Signal(str)
    finished_signal = Signal(dict)
    
    def __init__(self, project_path, target_kb, log_callback):
        super().__init__()
        self.project_path = project_path
        self.target_kb = target_kb
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
    
    def run(self):
        try:
            self.log(f"\n{'='*60}")
            self.log(f"🎯 ОПТИМИЗАЦИЯ ПОД РАЗМЕР {self.target_kb} KB")
            self.log(f"📁 Папка: {self.project_path}")
            if image_optimizer.check_oxipng():
                self.log("✅ Oxipng найден (lossless для лимитов ≥250 KB)")
            self.log(f"{'='*60}")
            
            size_folders = self.find_size_folders(self.project_path)
            
            if not size_folders:
                self.log("❌ Папки с 'x' в имени не найдены")
                self.finished_signal.emit({'total': 0, 'processed': 0, 'skipped': 0})
                return
            
            total = len(size_folders)
            self.log(f"📁 Найдено папок: {total}")
            
            total_before = 0
            total_after = 0
            processed = 0
            skipped = 0
            
            for idx, folder_info in enumerate(size_folders):
                folder_path = folder_info['path']
                folder_name = f"{folder_info['platform']}/{folder_info['campaign']}/{folder_info['size']}"
                
                progress_value = int((idx / total) * 100)
                self.progress_update.emit(progress_value, f"Анализ: {folder_info['size']} ({idx+1}/{total})")
                
                self.log(f"\n[{idx+1}/{total}] {folder_name}")
                
                result = settings_finder.find_best_settings(folder_path, self.target_kb, self.log)
                
                if result[0] is None:
                    self.log(f"  {result[4]}")
                    skipped += 1
                    continue
                
                method, jpg_q, png_param, archive_size, msg = result
                self.log(f"  {msg}")
                self.log("  🔄 Применяем сжатие...")
                
                files_to_process = []
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path) and not file.endswith('.fla'):
                        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            files_to_process.append(file)
                
                folder_before = 0
                folder_after = 0
                
                for file_idx, file in enumerate(files_to_process):
                    file_path = os.path.join(folder_path, file)
                    old_size = os.path.getsize(file_path)
                    folder_before += old_size
                    
                    file_progress = int(((idx + file_idx / len(files_to_process)) / total) * 100)
                    self.progress_update.emit(file_progress, f"{folder_info['size']}: {file}")
                    
                    if file.lower().endswith(('.jpg', '.jpeg')):
                        reduction = image_optimizer.optimize_jpeg(file_path, jpg_q)
                        new_size = os.path.getsize(file_path)
                        folder_after += new_size
                        if reduction > 0:
                            self.log(f"    ✅ {file}: {old_size//1024} KB → {new_size//1024} KB (-{reduction:.0f}%)")
                        else:
                            self.log(f"    ✓ {file}: {old_size//1024} KB")
                    
                    elif file.lower().endswith('.png'):
                        if method == 'lossless':
                            success, reduction = image_optimizer.optimize_png_oxipng(file_path, png_param)
                        else:
                            success, reduction = image_optimizer.optimize_png_lossy(file_path, png_param)
                        new_size = os.path.getsize(file_path)
                        folder_after += new_size
                        if success and reduction > 0:
                            self.log(f"    ✅ {file}: {old_size//1024} KB → {new_size//1024} KB (-{reduction:.0f}%)")
                        else:
                            self.log(f"    ✓ {file}: {old_size//1024} KB")
                    
                    self.msleep(10)
                
                folder_reduction = (1 - folder_after/folder_before) * 100 if folder_before > 0 else 0
                total_before += folder_before
                total_after += folder_after
                processed += 1
                self.log(f"  📊 Итого папки: {folder_before//1024} KB → {folder_after//1024} KB (сжатие {folder_reduction:.0f}%)")
                
                self.msleep(50)
            
            total_reduction = (1 - total_after/total_before) * 100 if total_before > 0 else 0
            
            self.log(f"\n{'='*60}")
            self.log("✅ ОПТИМИЗАЦИЯ ЗАВЕРШЕНА!")
            self.log(f"📁 Обработано папок: {processed}")
            self.log(f"⏭️ Пропущено: {skipped}")
            if total_before > 0:
                self.log(f"📊 Общий размер: {total_before//1024} KB → {total_after//1024} KB")
                self.log(f"📊 Общее сжатие: {total_reduction:.0f}%")
            self.log("🎯 Теперь можно запустить архивацию!")
            self.log(f"{'='*60}\n")
            
            self.finished_signal.emit({
                'processed': processed,
                'skipped': skipped,
                'total_before': total_before,
                'total_after': total_after,
                'total_reduction': total_reduction
            })
            
        except Exception as e:
            self.log(f"❌ Ошибка оптимизации: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            self.finished_signal.emit({'error': str(e)})


class OptimizerBlock(QWidget):
    def __init__(self, project_path, log_callback=None):
        super().__init__()
        self.project_path = project_path
        self.log_callback = log_callback
        self.optimizer_thread = None
        
        self.setup_ui()
        apply_styles(self)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Оптимизация изображений")
        title.setObjectName("block_title")
        layout.addWidget(title)
        
        settings_group = QGroupBox("Настройки")
        settings_layout = QHBoxLayout(settings_group)
        
        settings_layout.addWidget(QLabel("Целевой размер архива:"))
        self.target_size = QLineEdit("300")
        self.target_size.setFixedWidth(80)
        settings_layout.addWidget(self.target_size)
        settings_layout.addWidget(QLabel("KB"))
        settings_layout.addStretch()
        
        layout.addWidget(settings_group)
        
        self.run_btn = QPushButton("ОПТИМИЗИРОВАТЬ ВСЕ")
        self.run_btn.setObjectName("run_btn")
        from ui_pyside6.icons_utils import set_icon
        set_icon(self.run_btn, 'zap', 18)  # добавляем иконку молнии
        self.run_btn.clicked.connect(self.start_optimization)
        layout.addWidget(self.run_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setObjectName("progress_bar")
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setVisible(False)
        self.progress_label.setObjectName("progress_label")
        layout.addWidget(self.progress_label)
        
        self.status_text = QLabel("Готов к оптимизации")
        self.status_text.setObjectName("status_text")
        layout.addWidget(self.status_text)
        
        hint_frame = QFrame()
        hint_frame.setObjectName("hint_frame")
        hint_layout = QVBoxLayout(hint_frame)
        
        hint_title = QLabel("💡 Алгоритм:")
        hint_title.setObjectName("hint_title")
        hint_layout.addWidget(hint_title)
        
        hints = [
            "   • Для лимита ≥250 KB используется lossless сжатие (Oxipng)",
            "   • Для лимита <250 KB используется lossy сжатие (pngquant)",
            "   • JPEG сжимается с качеством 85-45 в зависимости от лимита",
            "   • Работает с папками animate/.../размер (папки, содержащие 'x')"
        ]
        for hint in hints:
            hint_label = QLabel(hint)
            hint_label.setObjectName("hint_text")
            hint_layout.addWidget(hint_label)
        
        layout.addWidget(hint_frame)
    
    def start_optimization(self):
        if self.optimizer_thread and self.optimizer_thread.isRunning():
            self.log("Операция уже выполняется, подождите...")
            return
        
        if not self.project_path or not os.path.exists(self.project_path):
            self.log("❌ Сначала выберите рабочую папку!")
            return
        
        try:
            target_kb = int(self.target_size.text().strip())
            if target_kb < 50:
                target_kb = 50
                self.target_size.setText("50")
        except:
            target_kb = 300
            self.target_size.setText("300")
        
        self.run_btn.setEnabled(False)
        self.run_btn.setText("⏳ ОПТИМИЗАЦИЯ...")
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setVisible(True)
        
        self.optimizer_thread = OptimizerThread(self.project_path, target_kb, self.log_callback)
        self.optimizer_thread.progress_update.connect(self.update_progress)
        self.optimizer_thread.log_signal.connect(self.log)
        self.optimizer_thread.finished_signal.connect(self.on_finished)
        self.optimizer_thread.start()
    
    def update_progress(self, value, text):
        self.progress_bar.setValue(value)
        self.progress_label.setText(text)
    
    def on_finished(self, result):
        self.run_btn.setEnabled(True)
        self.run_btn.setText("ОПТИМИЗИРОВАТЬ ВСЕ")
        
        if 'error' in result:
            self.status_text.setText(f"Ошибка: {result['error']}")
        else:
            reduction = result.get('total_reduction', 0)
            self.status_text.setText(f"Оптимизация завершена: {result['processed']} папок, сжатие {reduction:.0f}%")
        
        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))
        QTimer.singleShot(2000, lambda: self.progress_label.setVisible(False))
    
    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
    
    def update_project_path(self, new_path):
        self.project_path = new_path
        self.log(f"📂 Путь проекта обновлён: {new_path}")