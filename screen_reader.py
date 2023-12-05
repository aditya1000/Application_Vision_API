import pyautogui
from PIL import Image

import os
import openai
from openai import OpenAI
import base64
import json
import time
import errno



def capture_screen():
    # Take a screenshot
    time.sleep(3)
    screenshot = pyautogui.screenshot()
    return screenshot


def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue())


openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI() 


def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:    
                raise
            time.sleep(0.1)




def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe the Screenshot in English language"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/gif;base64,{base64_image}",
                },
            ],
        },
    ]


def analyze_image(base64_image, script):
    response = client.chat.completions.create(
        model= "gpt-4-vision-preview",   
        messages=[
            {
                "role": "system",
                "content": """
                You are a observer, Whats going on in this perticular screenshot.
                """,
            },
        ]
        + script
        + generate_new_line(base64_image),
        max_tokens=500,
    )
    response_text = response.choices[0].message.content
    return response_text


def main():
    script = []
    # image path
    #image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")
    screenshot = capture_screen()
    # getting the base64 encoding
     # Convert the screenshot to base64
    base64_image = convert_image_to_base64(screenshot)


    # analyze image
    print("Doctor is watching...")
    analysis = analyze_image(base64_image, script=script)

    print("🎙️ Doctor says:")
    print(analysis)

    script = script + [{"role": "assistant", "content": analysis}]

    # wait for 5 seconds
    time.sleep(5)

        

if __name__ == "__main__":
    main()
