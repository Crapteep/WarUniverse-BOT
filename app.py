import flet as ft
from views.home import Home
from views.set_bot import SetBot
from views.settings import Settings
from views.stats import Stats
from functions import *
from setting import *
from random import randint
import keyboard




class WarUniverseApp(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.set_bot_view = SetBot(self.page)
        self.settings_view = Settings(self.page)
        self.stats_view = Stats(self.page)
        self.app_region = None
        self.minimap_pos = []
        self.selected_boxes = {}
        self.selected_aliens = {RGB_HYDRO: None}
        self.blocked_area = []
        self.shooting = False
        self.is_clicked = False

    def build(self):
        self.page.banner = ft.Banner(bgcolor=ft.colors.AMBER_100,
                                leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
                                content=ft.Text(""),
                                actions=[ft.TextButton("OK", on_click=self.close_notification_banner)])
        
        self.start_btn = ft.ElevatedButton(text='START',
                                      bgcolor=ft.colors.GREEN_200,
                                      icon=ft.icons.PLAY_ARROW,
                                      color=ft.colors.BLACK,
                                      on_click=self.on_click_start)
        
        self.home_view = ft.Container(content=ft.Column([self.start_btn]),
                                        bgcolor=ft.colors.BLUE_GREY_100,
                                        expand=True,
                                        width=530,
                                        alignment=ft.alignment.center,
                                        border_radius=20
                                        )
        
        self.nav_bar = ft.NavigationRail(
                    selected_index=0,
                    label_type=ft.NavigationRailLabelType.ALL,
                    # extended=False,
                    min_width=100,
                    min_extended_width=400,
                    leading=ft.FloatingActionButton(icon=ft.icons.INSERT_EMOTICON_OUTLINED, text="Welcome!"),
                    group_alignment=-0.9,
                    destinations=[
                        ft.NavigationRailDestination(
                            icon=ft.icons.HOME_OUTLINED,
                            selected_icon=ft.icons.HOME,
                            label="Home",
                        ),
                        ft.NavigationRailDestination(
                            icon=ft.icons.DISPLAY_SETTINGS_OUTLINED,
                            selected_icon=ft.icons.DISPLAY_SETTINGS,
                            label="Set Bot",
                        ),
                        ft.NavigationRailDestination(
                            icon=ft.icons.SETTINGS_OUTLINED,
                            selected_icon=ft.icons.SETTINGS,
                            label="Settings",
                        ),
                        ft.NavigationRailDestination(
                            icon=ft.icons.QUERY_STATS_OUTLINED,
                            selected_icon=ft.icons.QUERY_STATS,
                            label="Stats",
                        ),
                    ],
                    on_change=self.nav_ral_change

                    )


        return ft.Container()



    def nav_ral_change(self, e):
        self.page.views.clear()

        match e.control.selected_index:
            case 0:
                self.page.views.append(self.view_handler(self.page)['/'])
            case 1:
                self.page.views.append(self.view_handler(self.page)['/set_bot'])
            case 2:
                self.page.views.append(self.view_handler(self.page)['/settings'])
            case 3:
                self.page.views.append(self.view_handler(self.page)['/stats'])

        # index = e.control.selected_index
        # if index == 0:
        #     self.page.views.append(self.view_handler(self.page)['/'])
        # elif index == 1:
        #     self.page.views.append(self.view_handler(self.page)['/set_bot'])
        # elif index == 2:
        #     self.page.views.append(self.view_handler(self.page)['/settings'])
        # elif index == 3:
        #     self.page.views.append(self.view_handler(self.page)['/stats'])
        self.page.update()

    def view_handler(self, page):
        return {'/': ft.View(
                        route="/",
                        controls=[
                            ft.Row(
                                controls=[
                                    self.nav_bar,
                                    ft.VerticalDivider(width=1),
                                    self.home_view,
                                ],
                                expand=True
                            )
                        ]
                    ),

                '/set_bot': ft.View(
                        route="/set_bot",
                        controls=[
                            ft.Row(
                                controls=[
                                    self.nav_bar,
                                    ft.VerticalDivider(width=1),
                                    self.set_bot_view,
                                ],
                                expand=True
                            )
                        ]
                    ),
                '/settings': ft.View(
                        route="/settings",
                        controls=[
                            ft.Row(
                                controls=[
                                    self.nav_bar,
                                    ft.VerticalDivider(width=1),
                                    self.settings_view,
                                ],
                                expand=True
                            )
                        ]
                    ),
                '/stats': ft.View(
                        route="/stats",
                        controls=[
                            ft.Row(
                                controls=[
                                    self.nav_bar,
                                    ft.VerticalDivider(width=1),
                                    self.stats_view,
                                ],
                                expand=True
                            )
                        ]
                    ),
                }
    
    def route_change(self, route):
        print('test:', self.set_bot_view.kill_alien)
        self.page.views.clear()
        self.page.views.append(self.view_handler(self.page)['/'])
        self.page.update()

    def check_selected_boxes(self):
        if self.set_bot_view.BonusBox.value:
            self.selected_boxes[RGB_BONUS_BOX] = None

        if self.set_bot_view.Mercury.value:
            self.selected_boxes[RGB_MERCURY] = None

        if self.set_bot_view.Cargo.value:
            self.selected_boxes[RGB_CARGO] = None

        if self.set_bot_view.Cerium.value:
            self.selected_boxes[RGB_CERIUM] = None

        if self.set_bot_view.Erbium.value:
            self.selected_boxes[RGB_ERBIUM] = None

        if self.set_bot_view.Piritid.value:
            self.selected_boxes[RGB_PIRITID] = None


    def on_keyboard(self, e: ft.KeyboardEvent):
        if e.key == "Q":
            self.on_click_stop()
 

    def on_click_stop(self, e):
        self.start_btn.disabled = False
        self.page.update()


    def on_click_start(self, e):
        self.blocked_area.clear()       #zrobić tak, ze jak dane beda wczytanie to zeby wczytywała sie od razu blocked area
                                        #jesli bedzie miała elementy to zeby juz nie liczyło ich
        #zrobić zeby sprawdzało te rzeczy wszystkie
        print(self.set_bot_view.blocked_area_points)
        

        self.start_btn.disabled = True
        self.page.update()

        for item in self.set_bot_view.blocked_area_points:
            val = calcElementPosition(item[0], item[1])
            self.blocked_area.append(val)

        self.getAppRegion()
        self.check_selected_boxes()
        self.minimap_pos = calcElementPosition(self.set_bot_view.minimap_points[0][0], self.set_bot_view.minimap_points[0][1])

        time_start = time.time()
        while self.start_btn.disabled:
            minimap_interval = time.time() - time_start


            # playerPosition(setScreenRegion(self.minimap_pos))
            # is_enemy = searchEnemy(self.app_region)
            # if is_enemy:
            #     self.safeEscape()
            #     pass
                #zrobić uciekanie do portu
            # print(is_enemy)




            if self.selected_boxes:
                if self.page.banner.open:
                    self.page.banner.open = False
                    self.page.update()

                self.collectItems(minimap_interval)

            else:
                if not self.page.banner.open:
                    self.page.banner.content = ft.Text("Opps, please select the type of collection boxes in [Set bot]!")
                    self.page.banner.open = True
                    self.page.update()

            if self.set_bot_view.kill_alien:
                is_enemy = searchEnemy(self.app_region)
                if not is_enemy:
                    self.killAliens()


            if minimap_interval >= TIME_BETWEEN_MINIMAP_CLICK:
                time_start = time.time()
            if keyboard.is_pressed('q'):
                self.on_click_stop(e)

            # time.sleep(1/60)
            self.page.update()
            

    def close_notification_banner(self,e):
        self.page.banner.open = False
        self.page.update()


    def getAppRegion(self):
        color_sought={(0,0,0): [(0,0,0), (1,1,1)]}
 
        while not activateGameWindow():
            gui.sleep(0.5)
            self.app_window = gui.getActiveWindow()

            if self.app_window.title == 'WarUniverse':
                self.window_region = {'left': self.app_window.left, 'top': self.app_window.top, 'width': self.app_window.width, 'height': self.app_window.height}
                contours, _ = findContours(color_sought, self.window_region, retr_contours=cv2.RETR_EXTERNAL)
                self.app_region = setScreenRegion(calcContourPosition(max(contours, key=cv2.contourArea), self.window_region))

        



    def collectItems(self, minimap_interval):
        
        element_pos = None
        is_collected = False
        clicked = False

        shortest_distance = self.app_window.width

        contours, grabed_region_RGB = findContours(colors_sought=self.selected_boxes, region=self.app_region)
        element_pos, shortest_distance = getShortestDistance(contours, self.app_window, region=self.app_region, shortest_distance=shortest_distance)

        if element_pos is not None:
            gui.moveTo(element_pos)
            if isHandCursor():
                if not checkBlockedAreaColision(self.blocked_area, element_pos):
                    gui.click(element_pos)
                    print('klikam w skrzynke')
                    is_collected = checkDidCollected({RGB_COLLECTED_ITEM: None}, self.app_region)
            else:
                if not clicked and not is_collected:
                    is_colision = checkBlockedAreaColision(self.blocked_area, element_pos)
                    if not is_colision:
                        gui.click(element_pos)
                        clicked = True
        else:
            if minimap_interval >= TIME_BETWEEN_MINIMAP_CLICK:
                # print('klikam na mapie')
                (x, y, w, h) = self.minimap_pos
                gui.moveTo(randint(x, w+x), randint(y, h+y))
                gui.click()


    def killAliens(self):
        if not self.is_clicked:
            
            shortest_distance = self.app_window.width
            contours, _ = findContours(colors_sought=self.selected_aliens, region=self.app_region)
            alien_pos, shortest_distance = getShortestDistance(contours, self.app_window, region=self.app_region, shortest_distance=shortest_distance)

            # print(shortest_distance)
            if alien_pos is not None and shortest_distance <= 450:
                if not checkBlockedAreaColision(self.blocked_area, alien_pos):
                    gui.moveTo(alien_pos)
                    gui.click(alien_pos)
                    self.is_clicked = True

        else:
            contours, view = findContours(colors_sought={RGB_HP: None}, region=self.app_region, retr_contours=cv2.RETR_EXTERNAL)
            drawContours(view, contours)
            if len(contours) >= 2:
                if not self.shooting:
                    gui.press('ctrl')
                    self.shooting = True

            else:
                if self.shooting:
                    gui.press('ctrl')
                    self.shooting = False
                self.is_clicked = False

    def safeEscape(self):
        pass