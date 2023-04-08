import flet as ft
from app import WarUniverseApp



def main(page: ft.Page):
    page.title = "WarUniverse BOT"
    page.horizontal_alignment = "center" 
    page.window_width = 720        # window's width is 200 px
    page.window_height = 600       # window's height is 200 px
    page.window_resizable = False
    page.window_maximizable = False  # window is not resizable
    page.update()

    app = WarUniverseApp(page)
    page.add(app)

    page.on_route_change = app.route_change
    page.on_keyboard_event = app.on_keyboard
    page.go(page.route)
    page.update()
    
ft.app(target=main) 