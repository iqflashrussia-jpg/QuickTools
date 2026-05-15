import flet as ft
from modules.config import COLORS
from ui.components import make_button
from ui.progress_ui import create_progress_ui
from ui.create_project import create_project_block
from ui.publish import publish_block
from ui.folder_selector import folder_selector_block
from ui.archiver import archiver_block
from ui.fla_operations import fla_operations_block
from ui.rename_operations import rename_operations_block

def create_main_view(page: ft.Page, selected_path_ref, is_working_ref, log_func):
    """Создаёт основной интерфейс - сборщик всех блоков"""
    
    folder_text = ft.Text(value="Папка не выбрана", size=14, color=COLORS["TEXT_SECONDARY"])
    output_text = ft.TextField(
        multiline=True,
        min_lines=20,
        max_lines=25,
        read_only=True,
        value="Готов к работе...\n",
        text_size=11,
        bgcolor=COLORS["BG_INPUT"],
        border_color="#3d3d3d",
        color=COLORS["TEXT"],
    )
    
    # Создаём прогресс-бар
    progress_bar, progress_text = create_progress_ui()
    
    # Создаём блоки с передачей прогресс-бара
    archiver_container, set_archiver_progress = archiver_block(log_func, selected_path_ref, is_working_ref, page)
    fla_container, set_fla_progress = fla_operations_block(log_func, selected_path_ref, is_working_ref, page)
    rename_container, set_rename_progress = rename_operations_block(log_func, selected_path_ref, is_working_ref, page)
    
    # Устанавливаем ссылки на прогресс-бар для блоков
    set_archiver_progress(progress_bar, progress_text)
    set_fla_progress(progress_bar, progress_text)
    set_rename_progress(progress_bar, progress_text)
    
    # Собираем левую панель
    left_panel = ft.Container(
        content=ft.Column([
            create_project_block(log_func, selected_path_ref, folder_text, page),
            publish_block(log_func, selected_path_ref, folder_text, page),
            folder_selector_block(log_func, selected_path_ref, folder_text, page),
            archiver_container,
            fla_container,
            rename_container,
        ], spacing=12),
        width=480,
    )
    
    def clear_output(e):
        output_text.value = "Лог очищен\n"
        page.update()
    
    # Правая панель
    right_panel = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Лог операций", size=12, color=COLORS["TEXT_SECONDARY"]),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.CLEAR_ALL, on_click=clear_output, 
                             tooltip="Очистить лог", icon_color=COLORS["TEXT_SECONDARY"], icon_size=18),
            ], spacing=10),
            ft.Column([progress_bar, progress_text], spacing=5),
            ft.Container(content=output_text, expand=True, height=450),
        ], spacing=5, expand=True),
        expand=True,
        padding=12,
        bgcolor=COLORS["BG_CARD"],
        border_radius=8,
    )
    
    main_container = ft.Row([left_panel, ft.Container(width=15), right_panel], 
                            spacing=0, expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
    page.add(main_container)
    
    return output_text