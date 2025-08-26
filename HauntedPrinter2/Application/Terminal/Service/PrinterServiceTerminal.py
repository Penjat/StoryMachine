from rx.subject import Subject


class PrinterServiceTerminal:
	def __init__(self):
		self.print_history_subject = Subject()
		self.print_history = []

	def print_array(self, array):
		pyplot.imshow(array)
		pyplot.show()

	def print_text_size(self, text, size):
		self.print_history.append(text)
		self.print_history_subject.on_next(self.print_history)

	def feed(self, number_lines):
		for i in range(0, number_lines):
			self.print_history.append("")
		self.print_history_subject.on_next(self.print_history)