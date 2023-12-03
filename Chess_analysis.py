import os
import openai
from openai import OpenAI
import base64
import json
import time
import simpleaudio as sa
import errno

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI() 


def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)




def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "How to out play the white team specific to the scene shown in the image"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{base64_image}",
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
                You are a Chess coach, a renowned Chess player. Describe the specific stratagy for the current position.
                Figure out which move will be best to play for black team.
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
    # path to your image
    image_path = os.path.join(os.getcwd(), "./frames/chess1.png")

    # getting the base64 encoding
    base64_image = encode_image(image_path)
    #print(base64_image) 
    # analyze posture
    print("👀 Coach is watching...")
    analysis = analyze_image(base64_image, script=script)

    print("🎙️ Coach says:")
    print(analysis)

    script = script + [{"role": "assistant", "content": analysis}]

    # wait for 5 seconds
    time.sleep(5)

        

if __name__ == "__main__":
    main()
