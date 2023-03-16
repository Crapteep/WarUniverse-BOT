from flet import *
from setup import *
import flet as ft
import pyautogui as gui
import keyboard

class SetBot(UserControl):
    def __init__(self,page):
        super().__init__()
        self.page = page
        self.BonusBox = ft.Checkbox(label='Bonus Box',value=False, on_change=self.checkbox_changed)
        self.Mercury = ft.Checkbox(label='Mercury', value=False, on_change=self.checkbox_changed)
        self.Cerium = ft.Checkbox(label='Cerium', value=False, on_change=self.checkbox_changed)
        self.Erbium = ft.Checkbox(label='Erbium', value=False, on_change=self.checkbox_changed)
        self.Piritid = ft.Checkbox(label='Piritid', value=False, on_change=self.checkbox_changed)
        self.Cargo = ft.Checkbox(label='Cargo', value=False, on_change=self.checkbox_changed)
        self.checkbox_items = [self.BonusBox, self.Mercury, self.Cerium, self.Erbium, self.Piritid, self.Cargo]
        self.kill_alien = False
        # self.kill_alien_switch = Switch(label=str(self.kill_alien), on_change=self.set_kill_aliens)
        self.kill_alien_switch = Switch(label='False', on_change=self.set_kill_aliens)
        self.minimap_points = []
        self.blocked_area_points = []
        
        
    
    
    def build(self):
        # self.area_num = ft.TextField(label="Podaj liczbe")
        # self.bs = ft.BottomSheet(
        #     ft.Container(
        #         ft.Column(
        #             [
        #                 ft.Text("Wybierz liczbe obszarów które chcesz zablokować!"),
        #                 self.area_num,
        #                 ft.ElevatedButton("Ok!", on_click=self.close_pop_up_window),
        #             ],
        #             tight=True,
        #         ),
        #         padding=10,
        #     ),
        #     open=False,
            
        # )
        # self.page.overlay.append(self.bs)

        self.set_minimap_btn = ElevatedButton('Set minmiap', on_click=self.get_points, bgcolor=colors.BLUE_GREY_200, height=25, width=140)
        self.set_blocked_area_btn = ElevatedButton('Set area', on_click=self.get_points, bgcolor=colors.BLUE_GREY_200, height=25, width=140)
        set_bot_container = Container(content=Row([Container(content=Container(Column([Text('Select items:'),
                                                                                       Row([Column([self.BonusBox, self.Mercury, self.Cerium]),
                                                                                            Column([self.Erbium, self.Piritid, self.Cargo])])]),
                                                                            # alignment=alignment.top_center,
                                                                            # bgcolor=colors.BROWN_400,
                                                                            height=200,
                                                                            margin=15,
                                                                            border_radius=10,
                                                                            padding=10,
                                                                            border=border.all(1, colors.BLACK),
                                                                            expand=True
                                                                               ),
                                                            #  bgcolor=colors.BLUE_100,
                                                             expand=True,
                                                             alignment=ft.alignment.top_center,
                                                            #  border=border.all(1, colors.BLACK),
                                                             border_radius=15),
                                                             
                                                   Column([Container(content=Container(Column([Text('Set kill aliens:'),
                                                                                       self.kill_alien_switch]),
                                                                            alignment=ft.alignment.top_center,
                                                                            # bgcolor=colors.BROWN_400,
                                                                            height=80,
                                                                            width=150,
                                                                            margin=15,
                                                                            border_radius=10,
                                                                            padding=10,
                                                                            border=border.all(1, colors.BLACK),
                                                                            expand=True
                                                                               ),
                                                            #  bgcolor=colors.BLUE_300,
                                                            #  expand=True,
                                                             alignment=ft.alignment.top_center,
                                                            #  border=border.all(1, colors.BLACK),
                                                             border_radius=15),
                                                            Container(content=Container(Column([self.set_minimap_btn, self.set_blocked_area_btn]),
                                                                                    alignment=ft.alignment.top_center,
                                                                                    # bgcolor=colors.BROWN_600,
                                                                                    height=80,
                                                                                    width=150,
                                                                                    margin=15,
                                                                                    border_radius=10,
                                                                                    padding=10,
                                                                                    border=border.all(1, colors.BLACK),
                                                                                    # expand=True
                                                                                    ),
                                                                    #  bgcolor=colors.BLUE_100,
                                                                    expand=True,
                                                                    alignment=ft.alignment.top_center,
                                                                    #  border=border.all(1, colors.BLACK),
                                                                    border_radius=15)])
                                                                    ]
                                                             
                                                             
                                                             
                                                             ),





                                        alignment=ft.alignment.center,
                                        )



        return Container(content=set_bot_container,
                        
                                        bgcolor=ft.colors.BLUE_GREY_100,
                                        expand=True,
                                        width=530,
                                        alignment=ft.alignment.center,
                                        border_radius=20
                                        )
    

    def set_kill_aliens(self, e):
        if self.kill_alien:
            self.kill_alien = False
            self.kill_alien_switch.label = 'False'
        else:
            self.kill_alien = True
            self.kill_alien_switch.label = 'True'
        
        self.update()
        

    # def close_pop_up_window(self, e):
    #     self.bs.open = False
    #     self.bs.update()
    
    # def open_pop_up_window(self, e):
    #     self.bs.open = True
    #     self.bs.update()
        

    def get_points(self, e):

        print(f"Rozpoczynam pobieranie punktów dla opcji: {e.control.text}")
        if e.control.text == self.set_minimap_btn.text:
            self.minimap_points.clear()
            num_of_points = 1
            point_list = self.minimap_points

        elif e.control.text == self.set_blocked_area_btn.text:
            self.blocked_area_points.clear()
            
            num_of_points = int(input('Ile obszarów chcesz zablokowac?'))
            # num_of_points = self.open_pop_up_window(e)
            # num_of_points = self.area_num.value
            print(num_of_points)
            point_list = self.blocked_area_points

        print('Aby anulować wciśnij "q"')
        print('Aby wybrać punkt, najedź na niego kursorem i wciśnij "g"')
        print(f"Wybierz po dwa punkty dla {num_of_points} obszaru/ów")
        
        x, y = None, None
        ctr = 0
        while True:
            if keyboard.is_pressed('q'):
                break
            elif keyboard.is_pressed('g'):
                if x is not None:
                    y = gui.position()
                    gui.sleep(0.5)
                    print('Punkt drugi został pobrany')
                else:
                    x = gui.position()
                    gui.sleep(0.5)
                    print('Punkt pierwszy został pobrany')

            if (x and y) is not None:
                ctr += 1
                point_list.append((x,y))
                x, y = None, None
                
                if ctr >= num_of_points:
                    break
                else:
                    print("Wybierz kolejny obszar: ")
            gui.sleep(1/30)
        print(f'Pomyślnie pobrano {num_of_points} obszar(y)')

    #------------------------------------------------------------------------------------

    def checkbox_changed(self,e):    #do poprawy
        # print(e.id)
        # for item in self.checkbox_items:
        #     if item.value:
        #         print('Zaznaczono checkbox')
        pass
        