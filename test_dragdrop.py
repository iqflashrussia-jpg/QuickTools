import flet as ft

def main(page: ft.Page):
    page.title = "Тест Drag & Drop"
    page.drag_to_scroll = True
    page.window.width = 500
    page.window.height = 400
    
    drop_zone = ft.Container(
        content=ft.Text("Перетащите файл/папку сюда", size=20),
        bgcolor="#1E1E1E",
        border_radius=16,
        padding=50,
        width=400,
        height=300,
    )
    
    def on_drag_enter(e):
        print("DRAG ENTER")
        drop_zone.border = ft.border.all(3, "green")
        drop_zone.update()
    
    def on_drag_leave(e):
        print("DRAG LEAVE")
        drop_zone.border = None
        drop_zone.update()
    
    def on_drop(e):
        print("DROP!")
        print(f"Event data: {e.data}")
        if e.data and e.data.files:
            for f in e.data.files:
                print(f"File path: {f.path}")
        drop_zone.border = None
        drop_zone.update()
    
    drop_zone.on_drag_enter = on_drag_enter
    drop_zone.on_drag_leave = on_drag_leave
    drop_zone.on_drop = on_drop
    
    page.add(drop_zone)

if __name__ == "__main__":
    ft.app(target=main)