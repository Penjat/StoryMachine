from RPi import GPIO
from rx.subject import Subject

class Knob:
    def __init__(self, clk, dt):
        self.clk = clk
        self.dt = dt
        GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.clk_last_state = GPIO.input(clk)
        self.dt_last_state = GPIO.input(dt)
        self.output_subject = Subject()
        
    def check_input(self):
        clk_state = GPIO.input(self.clk)
        dt_state = GPIO.input(self.dt)
            
        if clk_state != self.clk_last_state:
            if clk_state == dt_state:
                self.output_subject.on_next("down")
                print("down")
            else:
               self.output_subject.on_next("up")
               print("up")
                
        self.dt_last_state = dt_state
        self.clk_last_state = clk_state
        
class PressButton:
    
    def __init__(self, pin):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.state = GPIO.input(pin)
        self.pin = pin
        self.output_subject = Subject()
        
    def check_input(self):
        new_state = GPIO.input(self.pin)
        if new_state != self.state:
            if new_state == 1:
                self.output_subject.on_next("pressed")
            if new_state == 0:
                self.output_subject.on_next("released")
            self.state = new_state
            
class SwitchButton:
    
    def __init__(self, pin):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.state = GPIO.input(pin)
        self.pin = pin
        self.output_subject = Subject()
        
    def check_input(self):
        new_state = GPIO.input(self.pin)
        if new_state != self.state:
            self.output_subject.on_next("pressed")
            self.state = new_state