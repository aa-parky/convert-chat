import requests
import json

url = "http://192.168.1.11:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

# Define the NPC's background
npc_background = {
    "name": "Glimwick",
    "personality": "whimsical and nervous",
    "role": "Goblin merchant",
    "backstory": "Glimwick is a goblin merchant known for his quirky behavior and nervous laughter. He has a knack for acquiring rare items but is always wary of being tricked.",
    "goals": "To sell rare items and collect shiny treasures."
}

def generate_response(prompt):
    # Craft the style prefix using the NPC's background
    style_prefix = f"Act as {npc_background['name']}, a {npc_background['personality']} {npc_background['role']}. {npc_background['backstory']} {npc_background['goals']} please keep responses short: "

    # Prepend the style to the user's prompt
    styled_prompt = style_prefix + prompt

    # Send only the current styled prompt to the model
    data = {
        "model": "solar",
        "stream": False,
        "prompt": styled_prompt,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        return actual_response
    else:
        print("Error:", response.status_code, response.text)
        return None

# Loop to continuously get user input from the command line
while True:
    user_input = input("Enter your prompt: ")
    if user_input.lower() == 'exit':
        break
    response = generate_response(user_input)
    print("Response:", response)
