import flet as ft
from modules.config import COLORS

def create_progress_ui():
    """Создаёт прогресс-бар и текст к нему"""
    progress_bar = ft.ProgressBar(
        width=None,
        height=6,
        color=COLORS["SUCCESS"],
        bgcolor="#3d3d3d",
        value=0,
        visible=False,
    )
    progress_text = ft.Text(
        value="",
        size=11,
        color=COLORS["TEXT_SECONDARY"],
        visible=False,
    )
    return progress_bar, progress_text

def update_progress(progress_bar, progress_text, progress, status, page, visible=True):
    """Обновляет прогресс-бар и текст"""
    progress_bar.value = progress
    progress_text.value = status
    progress_bar.visible = visible
    progress_text.visible = visible
    page.update()

def hide_progress(progress_bar, progress_text, page):
    """Скрывает прогресс-бар"""
    progress_bar.visible = False
    progress_text.visible = False
    page.update()