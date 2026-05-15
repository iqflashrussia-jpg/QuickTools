import flet as ft
from modules.config import COLORS

def make_button(text, on_click, bgcolor=None, expand=False, height=40):
    """Кнопка без иконки, только текст"""
    return ft.Container(
        content=ft.Text(text, size=13, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
        bgcolor=bgcolor if bgcolor else COLORS["BG_CARD"],
        border_radius=6,
        padding=12,
        ink=True,
        on_click=on_click,
        expand=expand,
        height=height,
    )

def make_outlined_button(text, on_click, bgcolor=None, color=COLORS["PRIMARY"], expand=False, height=40):
    """Кнопка с контуром без иконки"""
    return ft.Container(
        content=ft.Text(text, size=13, color=color, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
        bgcolor=bgcolor if bgcolor else COLORS["BG_CARD"],
        border_radius=6,
        border=ft.border.all(1, "#4a4a4a"),
        padding=12,
        ink=True,
        on_click=on_click,
        expand=expand,
        height=height,
    )