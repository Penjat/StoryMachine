# Menu
from .MainMenu import Menu

# Sub Programs
from .Subprograms.MazeMaker import *
from .Subprograms.TarotReader import *
from .Subprograms.AltTarot import *
from .Subprograms.CellularAutomata import *
# from .Subprograms.LiveALive import *
from .Subprograms.LifeALife2 import LifeALife, Story, Chapter
from .Subprograms.BluetoothConnect import BluetoothConnect

class StoryMachine:
	def __init__(self, control_service, printer_service, camera_service, key):
		self.display_output = Subject()
		self.command_subject = Subject()
		self.isRunning = True
		self.sub_program = 0
		self.open_ai_api_key = key
		self.command_subject.subscribe(lambda x: self.process_command(x))

		# Set up Menu
		self.menu = Menu(self.display_output, self.command_subject, ["quit", "camera", "contrast camera", "Maze Maker", "Bluetooth", "CellularAutomata"])

		# Services
		self.printer_service = printer_service
		self.camera_service = camera_service    

		# Set Up Buttons
		control_service.main_button_subject.subscribe(lambda x: self.process_center_press(x))
		control_service.left_knob_subject.pipe(ops.throttle_first(0.1)).subscribe(lambda x: self.process_left_knob(x))
		control_service.right_knob_subject.pipe(ops.throttle_first(0.1)).subscribe(lambda x: self.process_right_knob(x))
		

	def process_left_knob(self, input):
		
		if self.sub_program != 0:
			self.sub_program.process_left_knob(input)
		else:
			self.menu.left_knob_input.on_next(input)
	
	def process_right_knob(self, input):
		
		if self.sub_program != 0:
			self.sub_program.process_right_knob(input)
		
		else:
			self.menu.right_knob_input.on_next(input)

	def process_center_press(self, input):
		if input != "pressed":
			return

		if self.sub_program != 0:
			# print("sub program")
			self.sub_program.process_center_press(input)
		else:
			# print("menu")
			self.menu.center_button_input.on_next(input)

	def process_cmd(self, output):
		
		cmd_type = output[0]

		if cmd_type == "print array":
			self.printer_service.print_array(output[1])
			return
		

		if cmd_type == "print text":
			self.printer_service.print_text(output[1], output[2])
			return

		if cmd_type == "feed":
			self.printer_service.feed(output[1])
			return

		else:
			print(f"command not recognized {cmd_type}")

	def process_command(self, command):
		print(command)

		if isinstance(command, tuple):
			self.process_cmd(command)
			return

		if command == "main menu":
			self.sub_program = 0
			self.menu.update_display()

		if command == "Bluetooth":
			self.sub_program = BluetoothConnect(self.display_output, self.command_subject)

		if command == "Maze Maker":
			self.sub_program = MazeMaker(self.display_output, self.command_subject)

		if command == "LifeALife":
			self.sub_program = LifeALife(self.display_output, self.command_subject, self.open_ai_api_key)

		if command == "camera":
			my_array = self.camera_service.image_to_array(self.camera_service.camera_image())
			self.printer_service.print_array(my_array)
			self.printer_service.feed(2)
			
		if command == "contrast camera":
			my_array =  self.camera_service.image_to_array2(self.camera_service.camera_image())
			self.printer_service.print_array(my_array)

		if command == "bible qoute":
		    printer.justify('L')
		    printer.setSize('S')
		    print("random bible quote")
		    file1 = open('bible.txt', 'r')
		    lines = file1.readlines()
			  
		    count = 0
		    line = random.choice(lines)
		    print("{}".format(line.strip()))
		    print_text("{}".format(line.strip()))

		if command == "CellularAutomata":
			self.sub_program = CellularAutomataGenerator(self.display_output, self.command_subject)

		if command == "Tarot Reading":
			self.sub_program = TarotReader(self.display_output, self.command_subject)
			
		# if output == "print pic":
		#     load_img_rz = Image.open("/home/pi/Documents/whale3.png").convert('1').resize((384,726))
		#     data = asarray(load_img_rz)
		#     inverter = lambda x: 1-x
		#     data = inverter(data)
		#     print_array(data)

		if command == "alt tarot":
			self.sub_program = AltTarot(self.display_output, self.command_subject)

		if command == "feed":
			self.printer_service.feed(1)

		if command == "quit":
			self.isRunning = False
			self.display_output.on_next("goodbye :-)")
