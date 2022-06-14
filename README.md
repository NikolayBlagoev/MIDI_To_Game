# MIDI_To_Game
Play videogames with your instrument

TO RUN: python run.py

If you want to run a specific config file:

python run.py NAME_OF_CONFIG.json


### JSON STRUCTURE:

MAX_VEL - integer, specifies the change (32000 is maximum)
FRACTION - float, used for the micro mouse movements
TICK_RATE - integer, how often an update is considered (LARGE MEANS LESS OFTEN)
ENABLE_MOUSE - boolean, if true mouse is moved, if false - XBOX controller joystic is moved. This is because some games won't work with the mouse movement
keys - the object with binds. The rule is:
"NOTE": "FUNCTION"

Single character functions are mapped to that key press (For example "60": "g" will map middle C to the key g)
Some special functions:
quit - exit program
refresh - refreshes config (thus you can change config without needing to restart the program)
SHIFT - maps to left shift key
CTRL_L - maps to left control key
SPACE - maps to space key
MB_L - maps to left mouse button
MB_R - maps to right mosue button
M_LEFT  - maps to mouse movement to the left
M_DOWN - maps to mouse movement down
M_UP - maps to mouse movement up
M_RIGHT - maps to mouse movement to the right
MM_LEFT - maps to small movement to the left (using fraction. Essentially does MAX_VEL * FRACTION)
MM_DOWN - maps to small movement down (using fraction. Essentially does MAX_VEL * FRACTION)
MM_UP - maps to small movement up (using fraction. Essentially does MAX_VEL * FRACTION)
MM_RIGHT - maps to small movement to the right (using fraction. Essentially does MAX_VEL * FRACTION)
