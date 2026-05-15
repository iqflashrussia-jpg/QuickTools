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

def create_dynamic_field_row(text_field, add_callback, remove_callback):
    """Создаёт строку с полем ввода и кнопками +/-
       Возвращает row и ссылки на кнопки"""
    row = ft.Row([text_field], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    
    remove_btn = ft.IconButton(
        icon=ft.Icons.REMOVE_CIRCLE,
        icon_color=COLORS["ERROR"],
        icon_size=20,
    )
    add_btn = ft.IconButton(
        icon=ft.Icons.ADD_CIRCLE,
        icon_color=COLORS["SUCCESS"],
        icon_size=20,
    )
    
    remove_btn.on_click = remove_callback
    add_btn.on_click = add_callback
    
    row.controls.append(remove_btn)
    row.controls.append(add_btn)
    
    return row