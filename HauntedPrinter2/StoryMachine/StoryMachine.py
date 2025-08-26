# Menu
from .MainMenu import Menu

# Sub Programs
from .Subprograms.MazeMaker import *
from .Subprograms.TarotReader import *
from .Subprograms.AltTarot import *
# from .Subprograms.LiveALive import *
from .Subprograms.LifeALife2 import LifeALife, Story, Chapter

class StoryMachine:
	def __init__(self, control_service, printer_service, camera_service, key):
		self.display_output = Subject()
		self.command_subject = Subject()
		self.isRunning = True
		self.sub_program = 0
		self.open_ai_api_key = key
		self.command_subject.subscribe(lambda x: self.process_command(x))

		# Set up Menu
		self.menu = Menu(self.display_output, self.command_subject)

		# Services
		self.printer_service = printer_service
		self.camera_service = camera_service    

		# Set Up Buttons
		control_service.main_button_subject.subscribe(lambda x: self.process_center_press(x))
		control_service.left_knob_subject.subscribe(lambda x: self.process_left_knob(x))
		control_service.right_knob_subject.subscribe(lambda x: self.process_right_knob(x))
		

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
			
		if command == "test":
			maze_array = np.zeros((64, 64))
			self.printer_service.print_text('this is some more awesometaski text that I would like to wrap', [])
			self.printer_service.print_text('abcdefghijklmnopqrstuvwxyzabcdef', ['M'])
			self.printer_service.print_text('abcdefghijklmnop', ['L'])

		if command == "push it!!!!":
			self.display_output.on_next("nice!")

		if command == "tell me a story":
			 
			self.printer_service.print_text('Some time ago,', ['L'])
			self.printer_service.print_text('on the internet...', ['L'])
			self.printer_service.feed(3)
			self.printer_service.print_text('thermal printer project')
			load_img_rz = Image.open("/home/pi/Documents/HauntedPrinter2/Images/printer_idea.png").convert('1').resize((384,384))
			data = asarray(load_img_rz)
			inverter = lambda x: 1-x
			data = inverter(data)
			self.printer_service.print_array(data)
			self.printer_service.feed(2)
			# maze_array[:1,:] = 1
			# maze_array[:,:1] = 1
			# maze_array[:,-1:] = 1
			# maze_array[-1:,:] = 1
			# self.printer_service.print_array(maze_array)

		if command == "talk to me":
			string = ""
			options = ["0", "1"]
			for y in range(0, 4):
				
				for x in range(0, 32):
					string += options[random.randrange(0,2)]

			self.printer_service.print_text(string, ["M"])

		if command == "load ideas":
			self.printer_service.print_text('IDEAS:', ['L','Center', 'Underline', 'DW'])
			self.printer_service.feed(1)
			self.printer_service.print_text('+Instant Camera', ['L'])
			self.printer_service.print_text('+Maze Maker', ['L'])
			self.printer_service.print_text('+Tarot Card Reader', ['L'])
			self.printer_service.print_text('+Still Image Games', ['L'])
			self.printer_service.print_text('+Random Bible Quotes', ['L'])
			self.printer_service.print_text('+Ai Camera', ['L','DW'])
			self.printer_service.print_text('+Alt. Universe  Tarot', ['L'])

			self.printer_service.print_text('+Instant Comic creator', ['L'])
			self.printer_service.print_text('+ASCII art generator', ['L'])
			self.printer_service.print_text('+Daily Journaling', ['L'])
			self.printer_service.print_text('+Magic Incantations', ['L'])
			self.printer_service.print_text('+Still image games', ['L'])
			self.printer_service.print_text('+Random Bible Quotes', ['L'])
			self.printer_service.print_text('+Famous novel games', ['L'])
			self.printer_service.print_text('+Story Machine', ['L'])
			self.printer_service.print_text('...', ['L'])
			self.printer_service.feed(3)

			


		# if output == "bible qoute":
		#     printer.justify('L')
		#     printer.setSize('S')
		#     print("random bible quote")
		#     file1 = open('bible.txt', 'r')
		#     lines = file1.readlines()
			  
		#     count = 0
		#     line = random.choice(lines)
		#     print("{}".format(line.strip()))
		#     print_text("{}".format(line.strip()))

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
