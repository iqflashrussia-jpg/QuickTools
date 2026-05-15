import flet as ft
import os
import sys

# Добавляем modules в путь
sys.path.insert(0, os.path.dirname(__file__))

from modules.config import COLORS, get_oxipng_path
from modules import image_optimizer
from ui.main_view import create_main_view

def main(page: ft.Page):
    page.title = "QuickTools"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 25
    page.bgcolor = "#1e1e1e"
    
    page.window.width = 1600
    page.window.height = 1200
    page.window.min_width = 1200
    page.window.min_height = 800
    page.window.resizable = True
    page.update()
    
    # Состояние (используем list для изменяемости внутри вложенных функций)
    selected_path = [None]
    is_working = [False]
    
    # Функция для логирования
    output_text_ref = [None]
    
    def log(message):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        if output_text_ref[0]:
            output_text_ref[0].value += f"[{timestamp}] {message}\n"
            lines = output_text_ref[0].value.split('\n')
            if len(lines) > 500:
                output_text_ref[0].value = '\n'.join(lines[-400:])
            page.update()
    
    # Создаём UI
    output_text = create_main_view(page, selected_path, is_working, log)
    output_text_ref[0] = output_text
    
    # Стартовые сообщения
    log("🚀 QuickTools запущена!")
    log("💡 Выберите рабочую папку")
    log("📦 Схема работы:")
    log("   1. Задайте целевой размер архива в KB")
    log("   2. Нажмите 'ОПТИМИЗИРОВАТЬ ВСЕ ПОД РАЗМЕР' — подбор параметров и сжатие")
    log("   3. Нажмите 'АРХИВИРОВАТЬ ВСЕ' — создание архивов")
    log("   .fla файлы игнорируются при архивации")
    
    oxipng_path = get_oxipng_path()
    if oxipng_path:
        log(f"✅ Oxipng найден (lossless сжатие для PNG при лимитах ≥250KB)")
    else:
        log(f"⚠️ Oxipng не найден. Положите oxipng.exe в папку с программой для lossless сжатия PNG")

if __name__ == "__main__":
    import time
    ft.app(target=main)