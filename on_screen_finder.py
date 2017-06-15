from PIL import ImageGrab  # PIL is windows machine only.
from PIL import Image
from numpy import array, unravel_index, argmax, max, zeros, arange
from scipy.signal import correlate2d
from scipy.ndimage import label, center_of_mass

import matplotlib.pyplot as plt
import time

import win32api, win32con


from code_library import VK_CODE


def get_mouse_coordinates():
    coord = win32api.GetCursorPos()
    return coord


def press_a_key(input):

    if input in VK_CODE:
        input = VK_CODE[input]
    elif len(input) > 1:
        print('invalid key token, skipping')
        return
    print(input)
    # time.sleep(20
    win32api.keybd_event(input, 0, 0, 0)
    time.sleep(.5)
    win32api.keybd_event(input, 0, win32con.KEYEVENTF_KEYUP, 0)
    #win32api.Send


def click(c_type):
    if c_type == 'click':
        single_click()

    if c_type == 'double-click':
        single_click()
        time.sleep(0.1)
        single_click()
        # press enter for second click
        #win32api.keybd_event(0x0D, 0, 0, 0)
        #time.sleep(0.05)
        #win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)


def single_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0,0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0,0, 0, 0)
    print('mouse button went up and down')


def fetch_correlation(image_path_raw_string, wait=0.001, debug=False):
    # wait before screenshot
    time.sleep(wait)

    # capture full screen
    screen = ImageGrab.grab()  # screen
    icon = Image.open(image_path_raw_string)  # icon to find

    # d-type conversions for faster computation
    bulk = array(screen.convert('L'))
    #bulk = bulk / bulk.max()
    bulk = bulk - bulk.mean()
    # plt.imshow(bulk)
    # plt.show()
    detail = array(icon.convert('L'))
    #detail = detail / detail.max()
    detail = detail - detail.mean()
    # detail -= detail.mean(dtype='uint8')

    print('finding match')
    corr = correlate2d(bulk, detail, boundary='symm', mode='same')
    corr -= corr.min()  # make all values positive [0, ->>
    corr = corr / corr.max()  # all values between [0, 1]

    if debug:
        plt.imshow(corr)
        plt.show()

    if corr.mean() > 0.41:
        print('warning: low confidentiality. Button not found?')

    return corr


def find_on_screen(image_path_raw_string, wait=0.001, debug=False):
    corr = fetch_correlation(image_path_raw_string, wait=wait, debug = debug)
    vertical_coord, horizontal_coord = unravel_index(argmax(corr), corr.shape)

    if debug:
        plt.imshow(corr)
        plt.plot(horizontal_coord, vertical_coord, 'r.')
        plt.show()
        print("vertical coordinates")
        print(vertical_coord)
        print("vhorizontal coordinates")
        print(horizontal_coord)

    vertical_coord, horizontal_coord = unravel_index(argmax(corr), corr.shape)

    return (horizontal_coord, vertical_coord )


def find_all_on_screen(image_path_raw_string, debug=False, threshold=0.9):
    corr = fetch_correlation(image_path_raw_string, debug=debug)

    possible_peak_filter = zeros(corr.shape)
    possible_peak_filter[corr > threshold] = 1.

    # create lables
    labeled_array, feature_count = label(possible_peak_filter)
    center_points = center_of_mass(corr, labeled_array, arange(feature_count) + 1)
    print(center_points)

    if debug:
        print('found {} area(s) of interests.'.format(feature_count))
        plt.imshow(labeled_array)
        plt.show()

    return center_points


def move_mouse_to_coords(coords_as_list):
    win32api.SetCursorPos(coords_as_list)


if __name__ == '__main__':
    im_path = r'image_resources\atom_launcher.PNG'
    # time.sleep(20)
    hit = find_all_on_screen(im_path)
    #move_mouse_to_coords(hit)


