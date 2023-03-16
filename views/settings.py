from flet import *
from setup import *

class Settings(UserControl):
    def __init__(self,page):
        super().__init__()
        self.page = page

    def build(self):
        return Container(content=Column([Text('Settings', bgcolor=colors.GREEN_200)]),
                                        bgcolor=ft.colors.BLUE_GREY_100,
                                        expand=True,
                                        width=530,
                                        alignment=ft.alignment.center,
                                        border_radius=20
                                        )