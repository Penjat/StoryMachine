import os
import openai
import json
import requests
from PIL import Image

openai.api_key = ""

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Gigi is an alternat tarot card generator and reader.  It generats an alternate origional tarot card and provides a reading.\n\nCard: The Knight of Sneakers\n\nReading: This card suggests that you are ready to take a risk and make a bold move. The Knight of Sneakers indicates that you have the courage and strength to follow your own path, and to take action that is unconventional and daring. You are well-prepared to take on any challenge that comes your way and to make a lasting impact on your life and the lives of those around you. Do not be afraid to take risks, even if it means going against the grain. The Knight of Sneakers is a reminder that success comes from taking risks and having faith in your own abilities.\n\nCard:",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)


split_txt = response["choices"][0]["text"].split('Reading:')

card_name = split_txt[0]
reading = split_txt[1]

img_response = openai.Image.create(
  prompt="An alterante tarot card called {card_name}.  Black and white.  No text.",
  n=1,
  size="512x512"
)

# print(img_response)
print(card_name)
print(reading)
  

data = requests.get(img_response["data"][0]["url"]).content
  
# Opening a new file named img with extension .jpg
# This file would store the data of the image file
f = open('img.jpg','wb')
  
# Storing the image data inside the data variable to the file
f.write(data)
f.close()
  
# Opening the saved image and displaying it
img = Image.open('img.jpg')

img.show()
