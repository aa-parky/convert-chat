import requests
import json

url = "http://192.168.1.11:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

# Define the style prefix
style_prefix = "Briefly rephrase this in a whimsical and very devious goblin style, without adding explanations or notes, keep the same amount of sentences: "
def generate_response(prompt):
    # Prepend the style to the user's prompt
    styled_prompt = style_prefix + prompt

    # Send only the current styled prompt to the model
    data = {
        "model": "mistral",
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
    user_input = input("D-Enter your prompt: ")
    if user_input.lower() == 'exit':
        break
    response = generate_response(user_input)
    print("Response:", response)
