import os, random
from PIL import Image
from numpy import asarray
from matplotlib import pyplot
import json
# Using readlines()
# file1 = open('bible.txt', 'r')
# lines = file1.readlines()
  
# count = 0
# Strips the newline character
# line = random.choice(lines)
# print("Line{}: {}".format(count, line.strip()))


# file_name = random.choice(os.listdir("/Users/spencersymington/Downloads/PNG"))


# load_img_rz = Image.open("/Users/spencersymington/Downloads/PNG/%s" %file_name).convert('1').resize((384,726))

# data = asarray(load_img_rz)
# inverter = lambda x: 1-x 


# data = inverter(data)
# pyplot.imshow(data)
# pyplot.show()



# pass in a string and return an array of strings the appropriate line length, TBD
def wrap_for_printing(input_string):
	length_limit = 12
	lines = []
	
	words = input_string.split()
	line = ""
	for word in words:
		if len(line) + len(word) + 1 < length_limit:
			line += " "
			line += word
		else:
			lines.append(line)
			line = word

	lines.append(line)
	return lines

# to_print = wrap_for_printing("This is a long sentence I want to see how it wraps with this function I wrote.")

# for line in to_print:
# 	print(line)



story_state = []
  
# Opening JSON file
f = open('story1.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
nodes = data['nodes']

f.close()

# Go to Node
current_node = next(i for i in nodes if i["name"] == "Story Start")
is_running = True
while is_running:
	# Process Events
	for event in current_node["events"]:

	# Check event conditions
	  for condition in event["conditions"]:
	  	print(condition)

	# Process the results
	  for result in event["results"]:

	  	if result[0] == "print_text":
	  		print(result[1])

	  	if result[0] == "write_state":
	  		story_state.append(result[1])


	# Show Choices
	for choice in current_node["choices"]:
		# Check choices conditions
		print(choice["first"] + " " + choice["second"])

	# Choose choice
	# Process choice results
	# goto destination







