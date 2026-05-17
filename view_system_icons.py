"""
Просмотр всех доступных системных иконок (QIcon.fromTheme)
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QScrollArea, QLineEdit, QGridLayout
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


class IconViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Системные иконки (QIcon.fromTheme)")
        self.resize(800, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Поле для поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Фильтр иконок...")
        self.search_input.textChanged.connect(self.filter_icons)
        layout.addWidget(self.search_input)
        
        # Область для иконок
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.icons_widget = QWidget()
        self.icons_layout = QGridLayout(self.icons_widget)
        self.icons_layout.setSpacing(20)
        scroll.setWidget(self.icons_widget)
        layout.addWidget(scroll)
        
        # Список всех возможных иконок
        self.all_icons = [
            # Навигация и действия
            ('list-add', '➕ Добавить / Плюс'),
            ('list-remove', '➖ Удалить / Минус'),
            ('edit-delete', '🗑 Удалить / Корзина'),
            ('edit-copy', '📋 Копировать'),
            ('edit-paste', '📌 Вставить'),
            ('edit-cut', '✂ Вырезать'),
            ('edit-rename', '✏ Переименовать'),
            ('edit-clear', '🧹 Очистить'),
            
            # Запуск и управление
            ('media-playback-start', '▶ Запустить / Play'),
            ('media-playback-stop', '⏹ Стоп'),
            ('media-playback-pause', '⏸ Пауза'),
            ('system-run', '⚡ Выполнить'),
            ('system-shutdown', '🔌 Выключение'),
            ('system-lock-screen', '🔒 Блокировка'),
            
            # Файлы и папки
            ('folder', '📁 Папка'),
            ('folder-open', '📂 Открытая папка'),
            ('document-new', '📄 Новый документ'),
            ('document-open', '📂 Открыть документ'),
            ('document-save', '💾 Сохранить'),
            ('document-save-as', '💿 Сохранить как'),
            ('document-print', '🖨 Печать'),
            
            # Поиск
            ('system-search', '🔍 Поиск / Увеличительное стекло'),
            ('find-location', '📍 Найти местоположение'),
            
            # Настройки и инструменты
            ('applications-system', '⚙ Настройки / Система'),
            ('preferences-system', '🔧 Предпочтения'),
            ('configure', '🛠 Настройка'),
            ('tools-check-spelling', '✅ Проверка орфографии'),
            
            # Медиа и графика
            ('image-loading', '🖼 Изображение'),
            ('video-display', '🎬 Видео'),
            ('audio-card', '🎵 Аудио'),
            
            # Сеть
            ('network-connect', '🌐 Сеть / Подключение'),
            ('network-wireless', '📡 Wi-Fi'),
            ('network-workgroup', '🏢 Рабочая группа'),
            
            # Устройства
            ('drive-harddisk', '💽 Жёсткий диск'),
            ('drive-removable-media', '💾 USB / Съёмный диск'),
            ('computer', '🖥 Компьютер'),
            ('printer', '🖨 Принтер'),
            ('camera-photo', '📷 Камера'),
            
            # Интерфейс
            ('window-close', '❌ Закрыть окно'),
            ('window-maximize', '🖥 Развернуть'),
            ('window-minimize', '─ Свернуть'),
            ('dialog-ok', '✅ ОК / Принять'),
            ('dialog-cancel', '❌ Отмена / Закрыть'),
            ('dialog-apply', '✓ Применить'),
            
            # Статусы
            ('task-complete', '✔ Завершено'),
            ('task-attempt', '⚠ Попытка'),
            ('task-reject', '✖ Отклонено'),
            
            # Разное
            ('help-contents', '❓ Справка / Помощь'),
            ('help-about', 'ℹ О программе'),
            ('accessories-calculator', '🔢 Калькулятор'),
            ('accessories-text-editor', '📝 Текстовый редактор'),
            ('office-calendar', '📅 Календарь'),
            ('user-home', '🏠 Домашняя папка'),
            ('user-desktop', '🖥 Рабочий стол'),
            ('user-trash', '🗑 Корзина'),
            ('emblem-favorite', '⭐ Избранное'),
            ('emblem-important', '❗ Важное'),
            ('emblem-danger', '⚠ Опасность'),
            ('emblem-new', '✨ Новое'),
            ('view-refresh', '🔄 Обновить'),
            ('view-fullscreen', '⛶ Полный экран'),
            ('view-restore', '☐ Восстановить'),
        ]
        
        self.show_icons(self.all_icons)
    
    def show_icons(self, icons_list):
        """Отображает список иконок"""
        # Очищаем layout
        for i in reversed(range(self.icons_layout.count())):
            widget = self.icons_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        row = 0
        col = 0
        max_cols = 3
        
        for icon_name, description in icons_list:
            # Создаём карточку иконки
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(8)
            
            # Показываем иконку
            icon_label = QLabel()
            icon = QIcon.fromTheme(icon_name)
            if icon.isNull():
                # Если иконка не найдена, показываем название
                icon_label.setText("❓")
                icon_label.setStyleSheet("font-size: 32px;")
            else:
                icon_label.setPixmap(icon.pixmap(QSize(48, 48)))
            icon_label.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(icon_label)
            
            # Название иконки
            name_label = QLabel(icon_name)
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("font-size: 10px; color: #888; font-family: monospace;")
            card_layout.addWidget(name_label)
            
            # Описание
            desc_label = QLabel(description)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setStyleSheet("font-size: 11px; color: #fff;")
            card_layout.addWidget(desc_label)
            
            # Стили карточки
            card.setStyleSheet("""
                QWidget {
                    background-color: #1E1E1E;
                    border-radius: 8px;
                    padding: 12px;
                }
            """)
            
            self.icons_layout.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def filter_icons(self, text):
        """Фильтрует иконки по тексту"""
        if not text.strip():
            self.show_icons(self.all_icons)
            return
        
        filtered = []
        text_lower = text.lower()
        for icon_name, description in self.all_icons:
            if text_lower in icon_name.lower() or text_lower in description.lower():
                filtered.append((icon_name, description))
        
        self.show_icons(filtered)


def main():
    app = QApplication(sys.argv)
    
    # Применяем тёмную тему для наглядности
    app.setStyle("Fusion")
    
    # Тёмная палитра
    app.setStyleSheet("""
        QWidget {
            background-color: #0A0A0A;
            color: #FFFFFF;
        }
        QLineEdit {
            background-color: #1E1E1E;
            border: 1px solid #3A3A3A;
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
        }
        QScrollArea {
            border: none;
            background-color: transparent;
        }
    """)
    
    window = IconViewer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()