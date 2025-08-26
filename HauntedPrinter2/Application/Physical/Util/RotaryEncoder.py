from RPi import GPIO
from time import sleep
import time
from RPLCD import i2c
from KnobInput import *
import rx

lcdmode = 'i2c'
cols = 20
rows = 2
charmap = 'A00'
i2c_expander = 'PCF8574'

address = 0x27
port = 1

lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)

GPIO.setmode(GPIO.BCM)

right_knob = Knob(23,24)
left_knob = Knob(17,27)
main_button = SwitchButton(6)

main_button.output_subject.subscribe(
    lambda x: print("recieved from subscription")
    )

def update_screen():
    print(counter)
    lcd.clear()
    lcd.write_string(str(counter))
    lcd.cursor_pos = (1, 6)
    lcd.write_string(str(counter2))


try:
    while True:
        right_knob.check_input()
        left_knob.check_input()
        main_button.check_input()
        sleep(0.01)
finally:
    GPIO.cleanup()
    

