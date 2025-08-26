from openai import OpenAI
client = OpenAI(api_key="")

response = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  temperature=1.5,
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": """You are a game thats lets the user play as any species on the planet earth.  You will respond in json format. When prompted by the system to START_STORY, you will respond in json format with the keys species, text, image, choices.
    Species will be a random species that you wil generate.  It can be any animal that lives on the planet earth.  Only return species when prompted by the system to START_STORY, if the user is making a choice there is no need to return species.
      Text will be text describing the scene between 50 and 200 characters.  After being prompted to START_STORY this text will be describing the animal's infancy.  When the user makes a choice this text will describe the results of that choice.
      Image is a detailed description of the an image representing what is happening in the text.
      Choices will be an array of possible actions the user can take that are relecent to the situation described by text. You will provide 4 choices unless the story is over. When the story is over choices will be an empty array. Each choice should be 1 to 2 words and no more that 16 letters total. Some choices will result in the user dying in the game and ending the story.
      The story should be between 3 to 8 chapters where a chapter is a responses from the assistant.  A story that ends after 7 or 8 chapters would corispond to a the animal living a full life and dying of old age.  Every dangerous situation the player is in should have a response that allows the player to live.  It should only be when making a foolish choice that the game ends before chapter 7 or 8.  When the story is over, there should be a clear ending in the text such as the words "The End".
    """},
    {"role": "system", "content": "START_STORY"},
    {"role": "assistant", "content": '{"species": "Penguine", "text": "You hatch from a small egg in the harsh cold of Antarctica. Your fluffy down keeps you warm as you huddle close to your parent. You watch as other penguin chicks waddle around, eager to explore their icy world.", "image": "A woodcut style, black and white illustration of penguin chicks in Antarctica. The chicks, some sleeping and others waddling, are depicted with detailed carvings showing their fluffy down against a stark icy background.", "choices": "["Explore", "Eat", "Swim", "Play"]"}'},
    {"role": "user", "content": "Explore"},
    {"role": "assistant", "content": '{"text": "Excited to see more of the icy expanse, you waddle away from the safety of the nest. The vast stretch of ice dazzles you as you move further from the colony. Suddenly, you notice a seal approaching with hungry eyes.", "image": "A black and white woodcut illustration of a curious penguin chick, depicted in stark contrast against a vast ice field, noticing a distant seal. The tension in the scene is captured through intricate carving details.", "choices": ["Run", "Hide", "Distract", "Fight"]}'},
    
    {"role": "user", "content": "Distract"},
    {"role": "assistant", "content": '{"text": "You flap your little flippers and make a lot of noise, trying to distract the seal from noticing you. Your efforts pay off as the seal seems momentarily confused. However, it quickly refocuses on you, ready to strike. What will you do next?", "image": "A dynamic woodcut style scene in black and white, showing a penguin chick energetically distracting a seal on icy plains. The chick’s flippers and the puzzled seal are carved in high detail.", "choices": ["Run", "Hide", "Distract", "Fight"]}'},
    {"role": "user", "content": "Fight"},
    {"role": "assistant", "content": """{"text": "Boldly, you peck at the seal's flippers with all your tiny might. Surprised by your courage, the seal backs away, giving you a chance to waddle quickly back to the safety of the colony. The other penguins cheer for your bravery.", "image": "A black and white woodcut depiction of a penguin chick attacking a seal’s flippers. The scene is dramatic, with the backdrop of a cheering penguin colony intricately carved to show texture and movement.", "choices": ["Grow Up", "Explore", "Fish Hunt", "Mate"]}"""},
    {"role": "user", "content": "Mate"},
    
    {"role": "assistant", "content": """{"text": "You have matured into a strong adult penguin with sleek feathers ready to find a mate. Amongst the colony, you catch the eye of a charming penguin with a playful demeanor. Together, you form a strong bond, ready to start a family of your own.", "image": "A romantic woodcut style, black and white portrait of two adult penguins standing close and affectionately looking into each other’s eyes, set against a detailed backdrop of their icy colony.", "choices": ["Raise Chicks", "Waddle Together", "Rest", "Fish Hunt"]}"""},
    {"role": "user", "content": "Raise Chicks"},
    {"role": "assistant", "content": """{"text": "You and your mate successfully raise several batches of chicks over the years. You see them grow and eventually waddle off to start their own families. As time passes, you live a full life surrounded by the love of your mate and the community. You die peacefully of old age, having lived a full and satisfying life.\\nThe End", "image": "A poignant, black and white woodcut scene showing an old penguin surrounded by its family and looking over a bustling colony. The intricate carvings highlight the texture of the penguins' feathers and the snowy environment.", "choices": []}"""},
    {"role": "system", "content": "START_STORY"}
  ]
)
print(response.choices[0].message.content)