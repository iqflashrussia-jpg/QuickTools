import flet as ft
import os

class DragDropZone(ft.Container):
    def __init__(self, on_project_selected, page: ft.Page):
        super().__init__()
        self.project_callback = on_project_selected
        self.page_ref = page
        
        # Настройки внешнего вида
        self.expand = True
        self.bgcolor = "#1E1E1E"
        self.border_radius = 16
        self.padding = 50
        self.height = 250
        
        # Текст внутри зоны (без использования констант иконок)
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text("📁", size=80),  # Используем эмодзи вместо иконки
                ft.Text(
                    "Перетащите папку проекта сюда",
                    size=20,
                    weight=ft.FontWeight.W_500,
                    color="#FFFFFF"
                ),
                ft.Text(
                    "или нажмите для выбора",
                    size=14,
                    color="#888888"
                ),
                ft.ElevatedButton(
                    "Выбрать папку",
                    on_click=self.pick_folder,
                )
            ]
        )
        
        # Включаем Drag & Drop
        self.drag_target = self.content  # Делаем содержимое целью для перетаскивания
        
        # Подписываемся на события
        self.on_drag_enter = self._on_drag_enter
        self.on_drag_leave = self._on_drag_leave
        self.on_drop = self._on_drop
        
    def _on_drag_enter(self, e):
        """При наведении файла"""
        self.border = ft.border.all(3, "#4CAF50")
        self.bgcolor = "#2A2A2A"
        self.update()
        
    def _on_drag_leave(self, e):
        """Когда убрали файл"""
        self.border = None
        self.bgcolor = "#1E1E1E"
        self.update()
        
    def _on_drop(self, e):
        """Когда бросили файл"""
        self.border = None
        self.bgcolor = "#1E1E1E"
        self.update()
        
        # Проверяем данные
        if e.data and hasattr(e.data, 'files') and e.data.files:
            path = e.data.files[0].path
            if os.path.isdir(path):
                self.project_callback(path)
            else:
                self.page_ref.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Пожалуйста, выберите папку, а не файл"),
                        bgcolor="#FF453A"
                    )
                )
        
    def pick_folder(self, e):
        """Выбор папки через диалог"""
        def on_dialog_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.project_callback(e.path)
        
        # Создаем и показываем диалог выбора папки
        file_picker = ft.FilePicker(on_result=on_dialog_result)
        self.page_ref.overlay.append(file_picker)
        self.page_ref.update()
        file_picker.get_directory_path()