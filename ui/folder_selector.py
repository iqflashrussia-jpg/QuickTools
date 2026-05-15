import flet as ft
import tkinter as tk
from tkinter import filedialog
import os
from modules.config import COLORS
from ui.components import make_button

def folder_selector_block(log_func, selected_path_ref, folder_text, page):
    """Создаёт блок 'Рабочая папка'"""
    
    def pick_folder(e):
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_selected = filedialog.askdirectory(title="Выберите рабочую папку")
        root.destroy()
        if folder_selected:
            selected_path_ref[0] = folder_selected
            folder_text.value = os.path.basename(selected_path_ref[0])
            folder_text.color = COLORS["PRIMARY"]
            folder_text.tooltip = selected_path_ref[0]
            log_func(f"Выбрана папка: {selected_path_ref[0]}")
        else:
            log_func("Выбор папки отменён")
    
    return ft.Container(
        content=ft.Column([
            ft.Text("Рабочая папка", size=12, color=COLORS["TEXT_SECONDARY"]),
            ft.Row([
                ft.Container(content=folder_text, expand=True, height=35),
                make_button("Выбрать", pick_folder, COLORS["PRIMARY"], expand=False, height=35),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ], spacing=8),
        padding=12,
        bgcolor=COLORS["BG_CARD"],
        border_radius=8,
    )