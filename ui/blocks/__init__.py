"""
Блоки интерфейса для каждой вкладки.
"""

from .create_project import create_project_block
from .publish import publish_block
from .fla_operations import fla_operations_block
from .rename_operations import rename_operations_block

# Временные заглушки для остальных блоков
def archiver_block(*args, **kwargs):
    import flet as ft
    from ui.styles import AppColors
    return ft.Text("Оптимизация и архивация (в разработке)", color=AppColors.TEXT_SECONDARY)