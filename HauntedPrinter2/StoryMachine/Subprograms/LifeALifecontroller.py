from LifeALife2 import LifeALife, Story, Chapter
from rx import combine_latest
from rx.subject import Subject



printer_service = Subject()
display_service = Subject()


printer_service.subscribe(lambda x: print(x))
display_service.subscribe(lambda x: print(x))


lifeALife = LifeALife(display_service, printer_service)


lifeALife.progress_story(1)

lifeALife.process_right_knob("up")
lifeALife.process_right_knob("up")
lifeALife.process_right_knob("up")
lifeALife.process_right_knob("up")

lifeALife.progress_story(1)