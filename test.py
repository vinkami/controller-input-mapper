from mapper import Listener
from pynput.keyboard import Controller as KBctrl
from pynput.mouse import Controller as MOUSEctrl, Button as MOUSEbtn
from threading import Thread
import time

cursor_move_max_speed = 1000
cursor_move_reaction_time = 1 / 120

kb = KBctrl()
mouse = MOUSEctrl()
RS_pos = [0, 0]
listen = Listener.load_code2key_json(open("mycontroller.json"))


@listen.action("other")
def other():
    global RS_pos
    RS_pos = [0, 0]


@listen.action("A")
def a(state):
    if state == 1:
        mouse.press(MOUSEbtn.left)
    elif state == 0:
        mouse.release(MOUSEbtn.left)


@listen.action("B")
def b(state):
    if state == 1:
        mouse.press(MOUSEbtn.right)
    elif state == 0:
        mouse.release(MOUSEbtn.right)


@listen.action("RS_V")
def cursor_move_vert_change(state):
    RS_pos[1] = - state / 32768 * cursor_move_max_speed * cursor_move_reaction_time


@listen.action("RS_H")
def cursor_move_vert_change(state):
    RS_pos[0] = state / 32768 * cursor_move_max_speed * cursor_move_reaction_time


def cursor_move():
    while True:
        mouse.move(*RS_pos)
        time.sleep(cursor_move_reaction_time)


Thread(target=cursor_move).start()
listen.run()
