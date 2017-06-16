"""
runtime script starts application from json run-file
"""

import json
import sys
import os
import time

import on_screen_finder

root_folder = ''

def move_mouse(coordinates):
    on_screen_finder.move_mouse_to_coords(coordinates)


def perform_generic_actions(act_dict):
    if 'sway' in act_dict:
        time.sleep(.5) # assure click completed
        (x, y) = on_screen_finder.get_mouse_coordinates()
        x += act_dict['sway'][0]
        y += act_dict['sway'][1]
        on_screen_finder.move_mouse_to_coords((x, y))

    if 'wait_after' in act_dict:
        time.sleep(act_dict['wait_after'])


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
        move_mouse((x,y))

    if 'action' in act_dict:
        if act_dict['action'] == 'single_click':
            on_screen_finder.click('click')
            print('i clicked')
        elif act_dict['action'] == 'double_click':
            on_screen_finder.click('double-click')
            print('i clicked 2x')

    if 'keys' in act_dict:
        import key_handler
        key_list = act_dict['keys']
        key_handler.press(*key_list)


        '''
        for ac in act_dict['keys']:
            on_screen_finder.press_a_key(ac)
            time.sleep(0.1)
        '''

    perform_generic_actions(act_dict)



def process_loop(loop_dict, action_library):

    if 'picture' not in loop_dict:
        print('cannot process, missing loop picture!')
        return

    # find all the loop picutres
    all_hits = on_screen_finder.find_all_on_screen(root_folder + loop_dict['picture'])

    # identify targets
    if 'indexes' in loop_dict:
        selection = loop_dict['indexes']
    else:
        selection = range(len(all_hits))

    selected_coordinates = [all_hits[sel] for sel in selection]

    for sel in selected_coordinates:
        move_mouse((int(sel[1]), int(sel[0])))

        if 'actions' in loop_dict:
            for act in loop_dict['actions']:
                process_action(action_library[act])
        print('done with loop {}'.format(sel))

    perform_generic_actions(loop_dict)


def dispatch(todo, loops, actions):

    if todo in loops:
        process_loop(loops[todo], actions)
    elif todo in actions:
        process_action(actions[todo])

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
    todos = d['todo']
    loops = d['loops']
    actions = d['actions']

    # check validity of json data
    todos_keys = set(todos)
    loop_keys = set(loops.keys())
    actions_keys = set(actions.keys())
    if len(loop_keys & actions_keys) > 0:
        print(loop_keys & actions_keys)
        print('ambiguous actions/loops found in json file')
    available = todos_keys - loop_keys
    available = available - actions_keys
    if len(available) > 0:
        print('some todos are not defined. See: {}'.format(available))

    # run the actions list
    [dispatch(todo, loops, actions) for todo in todos]

    # done! That's it
    print('finished loop.')
