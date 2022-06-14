from math import floor, sqrt
from pygame import midi
import pyautogui
from pynput.keyboard import Key, Controller
import pynput.mouse
# import pydirectinput
import vgamepad as vg
import sys
import json

# SETUP:
keyboard = Controller()
mouse = pynput.mouse.Controller()
gamepad = vg.VX360Gamepad()
MAX_VEL = 0
FRACTION = 0
TICK_RATE = 0
ENABLE_MOUSE = False
key_downs = dict()
mouse_dict = dict()
mouse_x = []
mouse_y = []
midi.init()
default_id = midi.get_default_input_id()
if default_id<0:
    print("NO MIDI DEVICE DETECTED")
    midi.quit()
    exit()

midi_input = midi.Input(device_id=default_id)

# For reference
MID_C = 60       

# GENERATE THE NEEDED ACTIONS
def key_press(key):
    return [lambda k: keyboard.press(key), lambda k: keyboard.release(key)]

def mouse_click(button: pynput.mouse.Button):
    return [lambda k: mouse.press(button), lambda k: mouse.release(button) ]

def clean_list(key: int, list):
    condition = True
    while condition:
        try:
            list.remove(key)
        except ValueError:
            condition = False


def closing_routine(placeholder):
    midi.quit()
    exit()



def dummy(placeholder):
    return

# Read the config json:
path = "config.json"
key_dict = dict()
if len(sys.argv)>1:
    path = sys.argv[1]

def refresh_routine(placeholder):
    global MAX_VEL
    global FRACTION
    global key_dict
    global path
    global TICK_RATE
    global ENABLE_MOUSE
    global mouse_x
    global mouse_y
    global mouse_dict
    key_dict.clear()
    with open(path, 'r') as f:
        data = json.load(f)

    TICK_RATE = data["TICK_RATE"]
    ENABLE_MOUSE = data["ENABLE_MOUSE"]
    MAX_VEL = data["MAX_VEL"]
    FRACTION = data["FRACTION"]
    keys = data["keys"]
    for d in keys:
        key_command = keys[d]
        if key_command.lower() == "quit":
            key_dict.update({int(d):[closing_routine,dummy]})
        elif key_command.lower() == "refresh":
            key_dict.update({int(d):[refresh_routine,dummy]})
        elif key_command.upper() == "MB_L":
            key_dict.update({int(d):mouse_click(pynput.mouse.Button.left)}) 
        elif key_command.upper() == "MB_R":
            key_dict.update({int(d):mouse_click(pynput.mouse.Button.right)}) 
        elif key_command.upper() == "M_LEFT":
            mouse_dict.update({int(d):-MAX_VEL})
            key_dict.update({int(d):[lambda k: mouse_x.append(k),lambda k:clean_list(k,mouse_x) ]}) 
        elif key_command.upper() == "M_RIGHT":
            mouse_dict.update({int(d):MAX_VEL})
            key_dict.update({int(d):[lambda k: mouse_x.append(k),lambda k:clean_list(k,mouse_x) ]})
        elif key_command.upper() == "MM_LEFT":
            mouse_dict.update({int(d):-MAX_VEL*FRACTION})
            key_dict.update({int(d):[lambda k: mouse_x.append(k),lambda k:clean_list(k,mouse_x) ]}) 
        elif key_command.upper() == "MM_RIGHT":
            mouse_dict.update({int(d):MAX_VEL*FRACTION})
            key_dict.update({int(d):[lambda k: mouse_x.append(k),lambda k:clean_list(k,mouse_x) ]})
        elif key_command.upper() == "M_DOWN":
            mouse_dict.update({int(d):-MAX_VEL})
            key_dict.update({int(d):[lambda k: mouse_y.append(k),lambda k:clean_list(k,mouse_y) ]}) 
        elif key_command.upper() == "M_UP":
            mouse_dict.update({int(d):MAX_VEL})
            key_dict.update({int(d):[lambda k: mouse_y.append(k),lambda k:clean_list(k,mouse_y) ]})
        elif key_command.upper() == "MM_DOWN":
            mouse_dict.update({int(d):-MAX_VEL*FRACTION})
            key_dict.update({int(d):[lambda k: mouse_y.append(k),lambda k:clean_list(k,mouse_y) ]}) 
        elif key_command.upper() == "MM_UP":
            mouse_dict.update({int(d):MAX_VEL*FRACTION})
            key_dict.update({int(d):[lambda k: mouse_y.append(k),lambda k:clean_list(k,mouse_y) ]}) 
        elif key_command.upper() == "SPACE":
            key_dict.update({int(d):key_press(Key.space)})
        elif key_command.upper() == "SHIFT":
            key_dict.update({int(d):key_press(Key.shift_l)})
        elif key_command.upper() == "CTRL_L":
            key_dict.update({int(d):key_press(Key.ctrl_l)}) 
        else:
            key_dict.update({int(d):key_press(key_command.lower())})

refresh_routine(0)


# print(mouse_dict.get(76))


#CSGO

#OW
# key_dict = {46:"y",48: "e", 49: "g",50: Key.shift,51:Key.ctrl_l,52:"a", 53:"s", 54:"w",55:"d",56:"q",57:Key.space, 58:"c",59:"r",
#  60: "e", 61: "g",62:Key.ctrl_l,74:"",75:"",76:"M_LEFT",77:"M_DOWN",78:"M_UP",79:"M_RIGHT",80:"1",81:"2",82:"3",83:"4",84:"5"}
#DOTA
# key_dict = {46:"y",48: "e", 49: "g",50:"q",51:"a",52:"w", 53:"e", 54:"s",55:"d",56:"b",57:"f", 58:"q",59:"r",
#  60: "e", 61: "g",62:Key.ctrl_l,63:"1",64:"2",65:"3",66:"4",74:"",75:"",76:"M_LEFT",77:"M_DOWN",78:"M_UP",79:"M_RIGHT",80:"",81:"ML",82:"MR",83:"l",84:"d",85:"u",86:"r"}
# print(key_dict)


tick=-1
x = 0
y = 0
(x_pos,y_pos) = (0,0)

while True:
    # for k,v in key_downs.items():
    #     print("note %d vel %d"%(k,v))
    tick=(tick+1)%10000000
    
    if tick%TICK_RATE==0:
        # print(len(mouse_x))
        (p1,p2)=mouse.position
        x = 0
        y = 0
        if len(mouse_x)==0 and len(mouse_y) ==0:
            gamepad.right_joystick(0, 0)
        elif len(mouse_x)!=0 and len(mouse_y)!=0:
            x = mouse_dict.get(mouse_x[len(mouse_x)-1])
            y = mouse_dict.get(mouse_y[len(mouse_y)-1])
            gamepad.right_joystick(x_value=floor(x*sqrt(2)/2), y_value=floor(y*sqrt(2)/2))
            # if tick%1000==0:
            #     mouse.position=(p1+x_pos, p2+y_pos)
        elif len(mouse_x)!=0:
            # if tick%1000==0:
            #     mouse.position=(x_pos+p1, y_pos+p2)
            
            x=mouse_dict.get(mouse_x[len(mouse_x)-1])
            # print(x)
            gamepad.right_joystick(x_value=floor(x), y_value=0)
        else:
            y=mouse_dict.get(mouse_y[len(mouse_y)-1])
            gamepad.right_joystick(x_value=0, y_value=floor(y))
        if ENABLE_MOUSE:
            mouse.position=(p1+floor(x/6000), p2-floor(y/6000))
        else:
            gamepad.update()
        # print(gamepad.p)
    if midi_input.poll():
        
        for event in midi_input.read(num_events=25):
            
            (_, note, vel, _)=event[0]
            
            if vel==0:
                if note in key_dict.keys():
                    key_downs.pop(note)
                    key_dict.get(note)[1](note)
                    # if note>73 and note<88:
                    #     if note == 78 or note == 77 or note == 84 or note == 85:
                    #         if not (78 in key_downs.keys() or 77 in key_downs.keys() or 84 in key_downs.keys() or 85 in key_downs.keys()):
                    #             y=0
                    #             y_pos=0
                    #     elif note == 76 or note == 79 or note == 83 or note == 86:
                    #         if not (76 in key_downs.keys() or 79 in key_downs.keys() or 83 in key_downs.keys() or 86 in key_downs.keys()):
                    #             x=0
                    #             x_pos=0
                    #     elif note == 74 or note == 81:
                    #         mouse.release(pynput.mouse.Button.left)
                    #     elif note == 75 or note == 82:
                    #         mouse.release(pynput.mouse.Button.right)
                    #     continue
                    # # pyautogui.keyUp(key_dict.get(note))
                    # keyboard.release(key_dict.get(note))

                    
            else:
                
                if note in key_dict.keys():
                    if note not in key_downs.keys():
                        key_downs.update({note:tick})
                    key_dict.get(note)[0](note)
                    # if note>73 and note<88:
                    #     if note == 78 or note==85:
                    #         if key_downs.get(77) is None or key_downs.get(77)<tick or key_downs.get(84) is None or key_downs.get(84)<tick:
                    #             y_pos=-1
                    #             y = floor(MAX_VEL*22/30) if note==78 else floor( MAX_VEL*3/4)
                    #     elif note == 77 or note==84:
                    #         if key_downs.get(78) is None or key_downs.get(78)<tick or key_downs.get(85) is None or key_downs.get(85)<tick:
                    #             y =floor( -MAX_VEL*22/30) if note==77 else floor( -MAX_VEL*3/4)
                    #             y_pos=1

                    #     elif note == 76 or note == 83:
                    #         if key_downs.get(79) is None or key_downs.get(79)<tick or key_downs.get(86) is None or key_downs.get(86)<tick:
                    #             x = -MAX_VEL if note==76 else floor(-MAX_VEL*3/4)
                    #             x_pos=-1
                    #     elif note == 79 or note == 86:
                    #         if key_downs.get(76) is None or key_downs.get(76)<tick or key_downs.get(83) is None or key_downs.get(83)<tick:
                                
                    #             x = MAX_VEL if note==79 else floor(MAX_VEL*3/4)
                    #             x_pos=1
                    #     elif note == 74 or note == 81:
                    #         mouse.press(pynput.mouse.Button.left)
                    #     elif note == 75 or note == 82:
                            
                    #         mouse.press(pynput.mouse.Button.right)
                        
                    # else:
                    #     # print(key_dict.get(note))
                    # # pyautogui.keyDown(key_dict.get(note))
                    #     if note ==49:
                    #         pyautogui.write("qeed",interval=0.15)
                    #     elif note ==48:
                    #         pyautogui.write("weed",interval=0.15)
                    #     else:
                    #         keyboard.press(key_dict.get(note))
                    
            # print("note %d vel %d"%(note,vel))
