import sys
print(sys.path)
sys.path.append('/home/pi/Documents/HauntedPrinter2')


def main(args=None):
	print("started main package")
	if args is None:
		args = sys.argv[1:]

	if len(args) < 1:
		print("please specify terminal or physical")

	elif args[0] == "terminal":
		print("run the terminal app")
		from Application.Terminal.StoryMachineTerminal import StoryMachineTerminal
		terminal_app = StoryMachineTerminal()
		terminal_app.run_app()

	elif args[0] == "physical":
		print("run the physical app")
		from Application.Physical.StoryMachinePhysicalV2 import StoryMachinePhysical
		app = StoryMachinePhysical()
		app.run_app()

	else:
		print("please specify terminal or physical")



if __name__ == "__main__":
    main()