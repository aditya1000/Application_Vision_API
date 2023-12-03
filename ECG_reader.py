import os
import openai
from openai import OpenAI
import base64
import json
import time
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
                raise
            time.sleep(0.1)




def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe the ECG and describe in English language"},
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
                You are Dr. Patel, a renowned cardiologist. Whats going on in this perticular ECG.
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
    image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

    # getting the base64 encoding
    base64_image = encode_image(image_path)

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
