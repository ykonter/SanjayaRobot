"""
runtime script starts application from json run-file
"""

import json
import sys
import os
import time

import on_screen_finder

root_folder = ''

def process_action(act_dict):
    print(act_dict)

    move_mouse = False
    (x,y) = on_screen_finder.get_mouse_coordinates()
    # print("{}, {}".format(*new_coords))


    if 'picture' in act_dict:
        print('looking for picture')
        move_mouse = True
        (x,y) = on_screen_finder.find_on_screen(root_folder + act_dict['picture'])

    if 'relative' in act_dict:
        move_mouse = True
        print(x, y)
        x += act_dict['relative'][0]
        y += act_dict['relative'][1]
        print(x, y)

    if move_mouse:
        on_screen_finder.move_mouse_to_coords((x,y))

    if 'action' in act_dict:
        if act_dict['action'] == 'single_click':
            on_screen_finder.click('click')
            print('i clicked')
        elif act_dict['action'] == 'double_click':
            on_screen_finder.click('double-click')
            print('i clicked 2x')

    if 'keys' in act_dict:
        for ac in act_dict['keys']:
            on_screen_finder.press_a_key(ac)
            time.sleep(0.1)

    if 'sway' in act_dict:
        time.sleep(.5) # assure click completed
        (x, y) = on_screen_finder.get_mouse_coordinates()
        x += act_dict['sway'][0]
        y += act_dict['sway'][1]
        on_screen_finder.move_mouse_to_coords((x, y))

    if 'wait_after' in act_dict:
        time.sleep(act_dict['wait_after'])




if __name__ == '__main__':

    # run_time file
    file_name = r'offline_test_folder\run.json'
    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    # fetch the run dictionary
    d = {}
    with open(file_name) as json_data:
        d = json.load(json_data)
        print(d)
    # setup root_folder pointer
    root_folder = os.path.dirname(file_name) + "/"
    print(root_folder)

    # fetch stuff
    items = on_screen_finder.find_all_on_screen(d['loop_picture'])
    loop_instructions = d['loop']
    actions = d['actions']

    # loop over the stuff
    for act in loop_instructions:
        process_action(actions[act])

    # done! That's it
    print('finished loop.')
