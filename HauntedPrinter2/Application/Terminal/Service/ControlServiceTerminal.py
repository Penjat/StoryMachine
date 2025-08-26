from rx.subject import Subject

class ControlServiceTerminal:
	def __init__(self):
		self.main_button_subject = Subject()
		self.left_knob_subject = Subject()
		self.right_knob_subject = Subject()