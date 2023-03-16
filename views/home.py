import flet as ft




        

class Home(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.page = page


    def build(self):
        return ft.Container(content=ft.Column([ft.ElevatedButton(text='START', bgcolor=ft.colors.GREEN_200, on_click=self.on_click_start, icon=ft.icons.PLAY_ARROW, color=ft.colors.BLACK)]),
                                        bgcolor=ft.colors.BLUE_GREY_100,
                                        expand=True,
                                        width=530,
                                        alignment=ft.alignment.center,
                                        border_radius=20
                                        )
    

    def on_click_start(self, e):
        print('wcisnieto start')
        pass
