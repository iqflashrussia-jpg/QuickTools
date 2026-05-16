import flet as ft
import sys
import os
import time

# Добавляем modules в путь
sys.path.insert(0, os.path.dirname(__file__))

from modules.config import COLORS, get_oxipng_path
from modules import image_optimizer
from ui.main_view import create_main_view


def main(page: ft.Page):
    # НАСТРОЙКИ ДЛЯ DRAG & DROP
    page.drag_to_scroll = True  # Включаем поддержку Drag & Drop
    
    # Состояние (используем list для изменяемости внутри вложенных функций)
    selected_path = [None]
    is_working = [False]
    
    # Функция для логирования (будет перенаправлена в LogView)
    def log(message):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        # Сообщение будет добавлено в LogView через callback
        if hasattr(log, 'callback') and log.callback:
            log.callback(message)
    
    # Создаём UI и получаем LogView
    log_view = create_main_view(page, selected_path, is_working, log)
    
    # Устанавливаем callback для логирования
    def add_to_log(message):
        log_view.add_message(message, page)
    
    log.callback = add_to_log
    
    # Стартовые сообщения
    log("🚀 QuickTools запущена!")
    log("💡 Перетащите папку проекта в окно или создайте новый проект")


if __name__ == "__main__":
    ft.app(target=main)