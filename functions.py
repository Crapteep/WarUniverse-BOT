import pyautogui as gui
import win32gui
import win32ui
import numpy as np
import cv2
import mss
from math import sqrt
import time
from setup import *


def activateGameWindow():
    try:
        hwnd = win32gui.FindWindow(None, 'Waruniverse')
        win32gui.SetForegroundWindow(hwnd)
        return True
    except:
        print('Please, run the game first')
        return False


def findContours(colors_sought: dict, region: tuple, retr_contours=cv2.RETR_TREE) -> tuple:
    """
    Given a dictionary of colors to be searched and a region to search within, this function
    captures a screenshot of the region and converts it from RGB to BGR. Then, it searches for
    the given colors within the region and creates masks for each color. Finally, it combines
    the masks and finds the contours and hierarchy of the resulting image.
    
    Args:
    - colors_sought (dict): A dictionary where each key is a color to be searched for and the value is either a list of lower and upper color bounds, or None.
    - region (tuple): A tuple of the form (x, y, width, height) representing the region to search.
    
    Returns:
    - contours (list): A list of contours found in the image.
    - grabed_region_RGB (numpy.ndarray): An RGB image of the grabbed region.
    """

    with mss.mss() as sct:
        grabed_region = np.array(sct.grab(region))
        grabed_region_RGB = cv2.cvtColor(grabed_region, cv2.COLOR_RGB2BGR)

        masks = []
        for color, bounders in colors_sought.items():
            if bounders is not None:
                lower_bound = np.array(bounders[0])
                upper_bound = np.array(bounders[1])
            else:
                lower_bound = np.array(color)
                upper_bound = np.array(color)

            masks.append(cv2.inRange(grabed_region_RGB, lower_bound, upper_bound))
        
        mask = sum(masks)
        contours, hierarchy = cv2.findContours(mask, retr_contours, cv2.CHAIN_APPROX_SIMPLE)
    return contours, grabed_region_RGB


def setScreenRegion(region_position):
    x, y, width, height = region_position
    region = {"left": x, "top": y,
              "width": width, "height": height}
    return region


def calcContourPosition(contour: np.ndarray, region: dict) -> tuple:
    """
    Calculates the position of a contour within a given region and points define contour.

    Args:
        contour (numpy.ndarray): An array of points that define the contour.
        region (dict): A dictionary containing the 'left', 'top', 'width', and 'height' values that define the rectangular region in which the contour is located.

    Returns:
        tuple: A tuple containing the (x, y, w, h) values that define the position of the contour.
            x and y represent the top-left corner of the contour relative to the top-left corner of the region,
            while w and h represent the width and height of the contour.
    
    Note:
        This function uses the cv2.boundingRect function to calculate the bounding rectangle of the contour.
        The returned (x, y, w, h) values are calculated by adding the 'left' and 'top' values of the region
        to the x and y values of the bounding rectangle, respectively.
    """
    (x, y, w, h) = cv2.boundingRect(contour)
    x, y = region['left'] + x, region['top'] + y
    return (x, y, w, h)


def getShortestDistance(contours, app_window, region, shortest_distance):
    element_pos = None

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        ship_pos_x, ship_pos_y = getShipPos(app_window)
        bonus_box_pos_x, bonus_box_pos_y = region['left'] + x + (1/2)*w, region['top'] + y + (1/2)*h
        distance = sqrt((ship_pos_x - bonus_box_pos_x)**2 +
                        (ship_pos_y - bonus_box_pos_y)**2)

        if distance < shortest_distance:
            element_pos = (bonus_box_pos_x, bonus_box_pos_y)
            shortest_distance = distance
    return element_pos, shortest_distance


def getShipPos(app_window) -> tuple:
    """
    Returns the center position of a window that represents a ship in a game.

    Args:
        app_window (pywinauto.win32_hooks.HookMixin): A window object that represents the game window. This object should be obtained using setScreenRegion() function.

    Returns:
        tuple: A tuple containing the x and y coordinates of the center position of the window - ship position.

    Note:
        This function assumes that the window object passed in represents a rectangular shape that
        has a center point. The function calculates the center point by adding half of the window's
        width to the left coordinate, and half of the window's height to the top coordinate.
    """
    return app_window.left + app_window.width/2, app_window.top + app_window.height/2


def isHandCursor() -> bool:
    """
    Determines whether the current Windows cursor is the standard hand cursor.

    Returns:
        bool: True if the current cursor is the hand cursor, False otherwise.

    Note:
        This function relies on the Windows API and only works on Windows operating systems.

        The function detects the hand cursor by examining the current cursor's bitmap data. The standard
        Windows hand cursor icon has a white arrow on a black background, so the function counts the number
        of black pixels in the bitmap and returns True if the count exceeds a certain threshold. The
        threshold value can be adjusted as needed to improve accuracy.
    """

    cursor_info = win32gui.GetCursorInfo()
    cursor_handle = cursor_info[1]

    if cursor_handle is not None:
        icon_info = win32gui.GetIconInfo(cursor_handle)
        icon_bitmap_handle = icon_info[3]
        create_bitmap = win32ui.CreateBitmapFromHandle(icon_bitmap_handle)
        # Get the bitmap data as a Python bytes object.
        bitmap_data = create_bitmap.GetBitmapBits(True)
        # The standard Windows hand cursor icon has a white arrow on a black background.
        # We can check for this by counting the number of black pixels in the icon bitmap.
        num_black_pixels = sum(1 for pixel in bitmap_data if pixel == 0)
        if num_black_pixels > 30:  # adjust this threshold as needed
            return True
    return False


def calcElementPosition(point1, point2) -> tuple:
    x, y = point1
    w = point2[0] - x
    h = point2[1] - y
    return (x, y, w, h)



def checkDidCollected(colors_sought, app_region):
    start = time.time()
    while True:
        contours, _= findContours(colors_sought, app_region)
        if contours or (time.time() - start >= MAX_COLLECTION_INTERVAL):
            return True


def is_number_in_range(number: float, lower_bound: float, upper_bound: float) -> bool:
    """
    Determines whether a number is within a specified range.

    Args:
        number (float): The number to check.
        lower_bound (float): The lower bound of the range.
        upper_bound (float): The upper bound of the range.

    Returns:
        bool: True if the number is within the specified range, False otherwise.     

    Note:
        This function assumes that the range is inclusive, meaning that the number can be equal to either
        the lower or upper bound and still be considered within the range. The function also assumes that
        the lower bound is less than or equal to the upper bound.

        The function can be used to check whether a given number falls within a certain range, such as a
        valid age range or a valid temperature range.
    """
    return lower_bound <= number <= upper_bound


def checkBlockedAreaColision(blocked_items: list, object_pos: tuple) -> bool:
        for item in blocked_items:
            (x, y, w, h) = item
            mouse_x, mouse_y = object_pos
            if (x <= mouse_x <= x + w) and (y <= mouse_y <= y + h):
                return True
        return False


def drawContours(grabed_view, contours):
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(grabed_view, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # wyświetlanie konturów
    cv2.imshow("Template matching", grabed_view)
    if cv2.waitKey(25) & 0xFF == 27:
        cv2.destroyAllWindows()


def searchEnemy(app_region):
    enemy_contour, _ = findContours(colors_sought={RGB_SOLAR: None, RGB_VEGA: None}, region=app_region, retr_contours=cv2.RETR_EXTERNAL)
    if enemy_contour:
        return True
    else:
        return False
        
    
def playerPosition(minimap_region):
    player_contour, grabed_view = findContours(colors_sought={None: [RGB_PLAYER_POINT_MIN, RGB_PLAYER_POINT_MAX]}, region=minimap_region)
    drawContours(grabed_view=grabed_view, contours=player_contour)
    if player_contour:
        return player_contour
