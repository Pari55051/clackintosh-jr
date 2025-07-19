# #import all IOs of board
# import board

# #imports from kmk libaray
# from kmk.kmk_keyboard import kmk_keyboard
# from kmk.scanners.keypad import KeysScanner
# from kmk.keys import KC
# from kmk.modules.macros import Press, Release, Tap, Macros

# #main instance of keyboard
# keyboard = KMKKeyboard()

# #adding macro extension
# macros = Macros()
# keyboard.modules.append(macros)

# # DEFINE PINS
# PINS = [board.A0, board.A1, board.A2, board.A3, board.D6, board.D7. board.D0, board.D3, board.D4, board.D2, board.D1]

# # not using matrix code
# keyboard.matrix = KeysScanner(
#     pins = PINS,
#     value_when_pressed = False,
# )

# # DEFINE BUTTONS corresp to pins
# keyboard.keymap = [
#     KC.A, KC.DELETE, KC.MACRO("Hello World"), KC.Macro(Press(KC.LCMD), Tap(KC.S), Release(KC.LMD)),
# ]

# # start kmk
# if __name__ == '__main__':
#     keyboard.go()

# print("Starting")

################################################################
import board
import displayio
import terminalio
from time import sleep

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

from kmk.modules.encoder import EncoderHandler
import adafruit_displayio_ssd1306
from adafruit_display_text import label

# for opening apps - via macros - through spotlight
def spotlight_open(app_name):
    def macro_function(keyboard):
        # Open Spotlight
        keyboard.tap_code(KC.LGUI)
        keyboard.tap_code(KC.SPACE)
        sleep(0.1)
        # Type app name
        for letter in app_name:
            key = getattr(KC, letter.upper(), None)
            if key:
                keyboard.tap_code(key)
                sleep(0.01)
        # Press Enter
        keyboard.tap_code(KC.ENTER)
    return macro_function

# matrix setup
keyboard = KMKKeyboard()
keyboard.col_pins = (board.GP3, board.GP4, board.GP2)    
keyboard.row_pins = (board.GP27, board.GP28, board.GP29)  
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# oled setup
displayio.release_displays()
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128
HEIGHT = 32
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
splash = displayio.Group()
display.show(splash)
status_text = label.Label(terminalio.FONT, text="Clackintosh Jr.", color=0xFFFFFF, x=5, y=18)
splash.append(status_text)

# RE setup
encoder = EncoderHandler()
keyboard.modules.append(encoder)
encoder.pins = ((board.GP0, board.GP1),)
encoder.map = [((KC.VOLU, KC.VOLD),)]

# keymap - all trigger func via macro only
keyboard.keymap = [
    [KC.NO, KC.NO, KC.NO], 
    [KC.NO, KC.NO, KC.NO],
    [KC.NO, KC.NO, KC.NO],
]

# key-app mapping
app_macros = [
    ("Arc", "Arc open!"),                     # Row 1 Col 1
    ("Mail", "Mail open!"),                   # Row 1 Col 2
    ("Terminal", "Terminal open!"),           # Row 1 Col 3
    ("Notes", "Notes open!"),                 # Row 2 Col 1
    ("Spotify", "Spotify open!"),             # Row 2 Col 2
    ("Fantastical", "Fantastical open!"),     # Row 2 Col 3
    ("Todoist", "Todoist open!"),             # Row 3 Col 1
    ("Whatsapp", "Whatsapp open!"),           # Row 3 Col 2
    (None, "Muted!"),                         # Row 3 Col 3 (rotary encoder switch)
]

# key press macro
def custom_key_handler(event):

    if event.pressed:
        key_index = event.key_number

        if key_index < len(app_macros):

            app_name, display_msg = app_macros[key_index]
            status_text.text = display_msg

            if app_name is None:
                keyboard.tap_code(KC.MUTE)
            else:
                spotlight_open(app_name)(keyboard)
                
    else:
        status_text.text = "Clackintosh Jr."

keyboard.key_down_handler = custom_key_handler

if __name__ == '__main__':
    keyboard.go()
