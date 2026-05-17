"""
Блок оптимизации для PySide6 (точная копия логики из Flet)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QGroupBox, QProgressBar,
    QFrame
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modules import settings_finder, image_optimizer


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
        """Находит все папки с 'x' в имени (размеры) внутри папки animate"""
        folders = []
        if not os.path.exists(base_path):
            return folders
        
        animate_path = os.path.join(base_path, "animate")
        if not os.path.exists(animate_path):
            self.log(f"⚠️ Папка animate не найдена: {animate_path}")
            return folders
        
        for platform in os.listdir(animate_path):
            platform_path = os.path.join(animate_path, platform)
            if not os.path.isdir(platform_path):
                continue
            
            for campaign in os.listdir(platform_path):
                campaign_path = os.path.join(platform_path, campaign)
                if not os.path.isdir(campaign_path):
                    continue
                
                for size_folder in os.listdir(campaign_path):
                    size_path = os.path.join(campaign_path, size_folder)
                    if os.path.isdir(size_path) and 'x' in size_folder.lower():
                        folders.append({
                            'path': size_path,
                            'platform': platform,
                            'campaign': campaign,
                            'size': size_folder
                        })
        return folders
    
    def run(self):
        try:
            self.log(f"\n{'='*60}")
            self.log(f"🎯 ОПТИМИЗАЦИЯ ПОД РАЗМЕР {self.target_kb} KB")
            self.log(f"📁 Папка: {self.project_path}")
            if image_optimizer.check_oxipng():
                self.log(f"✅ Oxipng найден (lossless для лимитов ≥250 KB)")
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
                self.log(f"  🔄 Применяем сжатие...")
                
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
            self.log(f"✅ ОПТИМИЗАЦИЯ ЗАВЕРШЕНА!")
            self.log(f"📁 Обработано папок: {processed}")
            self.log(f"⏭️ Пропущено: {skipped}")
            if total_before > 0:
                self.log(f"📊 Общий размер: {total_before//1024} KB → {total_after//1024} KB")
                self.log(f"📊 Общее сжатие: {total_reduction:.0f}%")
            self.log(f"🎯 Теперь можно запустить архивацию!")
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
        self.apply_styles()
    
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
            "   • Работает только с папками animate/Платформа/Кампания/Размер"
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
        
        from PySide6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))
        QTimer.singleShot(2000, lambda: self.progress_label.setVisible(False))
    
    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QLabel#block_title {
                font-size: 18px;
                font-weight: bold;
                color: #4CAF50;
            }
            
            QGroupBox {
                color: #FFFFFF;
                border: 1px solid #3A3A3A;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            
            QLineEdit {
                background-color: #2A2A2A;
                color: white;
                border: 1px solid #3A3A3A;
                border-radius: 4px;
                padding: 5px;
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
            
            QPushButton#run_btn:disabled {
                background-color: #666;
            }
            
            QProgressBar {
                border: 1px solid #3A3A3A;
                border-radius: 4px;
                text-align: center;
                color: white;
            }
            
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
            
            QLabel#status_text {
                color: #888888;
                font-size: 12px;
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