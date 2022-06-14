from math import floor, sqrt
from pygame import midi
import pyautogui
from pynput.keyboard import Key, Controller
import pynput.mouse
import pydirectinput
import vgamepad as vg

gamepad = vg.VX360Gamepad()
MAX_VEL = 16000
midi.init()
keyboard = Controller()

mouse = pynput.mouse.Controller()


default_id = midi.get_default_input_id()
midi_input = midi.Input(device_id=default_id)
#CSGO

#OW
# key_dict = {46:"y",48: "e", 49: "g",50: Key.shift,51:Key.ctrl_l,52:"a", 53:"s", 54:"w",55:"d",56:"q",57:Key.space, 58:"c",59:"r",
#  60: "e", 61: "g",62:Key.ctrl_l,74:"",75:"",76:"M_LEFT",77:"M_DOWN",78:"M_UP",79:"M_RIGHT",80:"1",81:"2",82:"3",83:"4",84:"5"}
#DOTA
key_dict = {46:"y",48: "e", 49: "g",50:"q",51:"a",52:"w", 53:"e", 54:"s",55:"d",56:"b",57:"f", 58:"q",59:"r",
 60: "e", 61: "g",62:Key.ctrl_l,63:"1",64:"2",65:"3",66:"4",74:"",75:"",76:"M_LEFT",77:"M_DOWN",78:"M_UP",79:"M_RIGHT",80:"",81:"ML",82:"MR",83:"l",84:"d",85:"u",86:"r"}

key_downs = dict()
mid_c = 60
tick=-1
x = 0
y = 0
(x_pos,y_pos) = (0,0)
print(default_id)
while True:
    # for k,v in key_downs.items():
    #     print("note %d vel %d"%(k,v))
    tick=(tick+1)%10000000
    if tick%5==0:
        # (p1,p2)=mouse.position
        if x==0 and y ==0:
            gamepad.right_joystick(0, 0)
        elif x!=0 and y!=0:
            gamepad.right_joystick(x_value=floor(x*sqrt(2)/2), y_value=floor(y*sqrt(2)/2))
            # if tick%1000==0:
            #     mouse.position=(p1+x_pos, p2+y_pos)
        else:
            # if tick%1000==0:
            #     mouse.position=(x_pos+p1, y_pos+p2)
            gamepad.right_joystick(x_value=x, y_value=y)
        gamepad.update()
        # print(gamepad.p)
    if midi_input.poll():
        
        for event in midi_input.read(num_events=25):
            
            (_, note, vel, _)=event[0]
            if note == 21:
                midi.quit()
                exit()
            if vel==0:
                if note in key_dict.keys():
                    key_downs.pop(note)
                    if note>73 and note<88:
                        if note == 78 or note == 77 or note == 84 or note == 85:
                            if not (78 in key_downs.keys() or 77 in key_downs.keys() or 84 in key_downs.keys() or 85 in key_downs.keys()):
                                y=0
                                y_pos=0
                        elif note == 76 or note == 79 or note == 83 or note == 86:
                            if not (76 in key_downs.keys() or 79 in key_downs.keys() or 83 in key_downs.keys() or 86 in key_downs.keys()):
                                x=0
                                x_pos=0
                        elif note == 74 or note == 81:
                            mouse.release(pynput.mouse.Button.left)
                        elif note == 75 or note == 82:
                            mouse.release(pynput.mouse.Button.right)
                        continue
                    # pyautogui.keyUp(key_dict.get(note))
                    keyboard.release(key_dict.get(note))

                    
            else:
                
                if note in key_dict.keys():
                    if note>73 and note<88:
                        if note == 78 or note==85:
                            if key_downs.get(77) is None or key_downs.get(77)<tick or key_downs.get(84) is None or key_downs.get(84)<tick:
                                y_pos=-1
                                y = floor(MAX_VEL*22/30) if note==78 else floor( MAX_VEL*3/4)
                        elif note == 77 or note==84:
                            if key_downs.get(78) is None or key_downs.get(78)<tick or key_downs.get(85) is None or key_downs.get(85)<tick:
                                y =floor( -MAX_VEL*22/30) if note==77 else floor( -MAX_VEL*3/4)
                                y_pos=1

                        elif note == 76 or note == 83:
                            if key_downs.get(79) is None or key_downs.get(79)<tick or key_downs.get(86) is None or key_downs.get(86)<tick:
                                x = -MAX_VEL if note==76 else floor(-MAX_VEL*3/4)
                                x_pos=-1
                        elif note == 79 or note == 86:
                            if key_downs.get(76) is None or key_downs.get(76)<tick or key_downs.get(83) is None or key_downs.get(83)<tick:
                                
                                x = MAX_VEL if note==79 else floor(MAX_VEL*3/4)
                                x_pos=1
                        elif note == 74 or note == 81:
                            mouse.press(pynput.mouse.Button.left)
                        elif note == 75 or note == 82:
                            
                            mouse.press(pynput.mouse.Button.right)
                        
                    else:
                        # print(key_dict.get(note))
                    # pyautogui.keyDown(key_dict.get(note))
                        if note ==49:
                            pyautogui.write("qeed",interval=0.15)
                        elif note ==48:
                            pyautogui.write("weed",interval=0.15)
                        else:
                            keyboard.press(key_dict.get(note))
                    if note not in key_downs.keys():
                        key_downs.update({note:tick})
            # print("note %d vel %d"%(note,vel))
qqedqqed