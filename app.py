import requests
import os
import sys
import time
from configparser import ConfigParser
from PIL import Image
from rich.console import Console
import colorama
from colorama import Fore, Back, Style, init
init()
console = Console()

dbconf = ConfigParser()
dbconf.read_file(open("config.ini"))

# Replace "YOUR_DALL-E_API_KEY" with your own DALL-E API key
API_KEY = dbconf.get("SETTING","API_KEY")
Width_Size = dbconf.get("SETTING","WIDTH_SIZE")
High_Size = dbconf.get("SETTING","HIGH_SIZE")
Loop_Mode = console.input("[bold white3]LOOP MODE [ON/OFF] : ")

Width_Size = int(Width_Size)
High_Size = int(High_Size)

text = console.input("\n[bold white3]Enter TEXT Prompt (use '\ n' for other prompt) : \n")

def textagain():
    text = console.input("\n[bold white3]Enter TEXT Prompt (use '\ n' for other prompt) : \n")
    if text == "RESET":
        Loop_Mode = console.input("[bold white3]LOOP MODE [ON/OFF] : ")

def main():
    # The text we want to generate an image for

    # Build the DALL-E API endpoint URL
    endpoint = "https://api.openai.com/v1/images/generations"

    # Build the request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Build the request payload
    data = {
        "model": "image-alpha-001",
        "prompt": text
    }

    # Send the request to the API and get the response
    response = requests.post(endpoint, headers=headers, json=data)    # Get the URL of the generated image from the response
    image_url = response.json()["data"][0]["url"]

    # Send a request to the image URL to download the image
    response = requests.get(image_url)

    # Save the image data to a file
    with open("generated_image.jpg", "wb") as f:
        f.write(response.content)

    # Open the image file
    image = Image.open("generated_image.jpg")

    # Resize the image to the specified dimensions
    width, height = (Width_Size, High_Size)
    image = image.resize((width, height), Image.ANTIALIAS)

    # Print the image data
    print(image.getdata())

    # Display the image
    image.show()
    print(Fore.YELLOW, Style.BRIGHT)
    print("=============================================================")
    print(Style.RESET_ALL)
    return

if __name__ == "__main__":
    while True:
        if Loop_Mode == "ON":
            print(Fore.LIGHTGREEN_EX, Style.BRIGHT)
            mes='----->> Please Waiting For New Loop // Press ❌ to Close'
            console.print(mes)
            print(Style.RESET_ALL)
            main()
            time.sleep(1)
        if Loop_Mode == "OFF":
            print(Fore.LIGHTGREEN_EX, Style.BRIGHT)
            mes='----->> Please Wait AI Generating Your Text-To-Image'
            console.print(mes)
            print(Style.RESET_ALL)
            main()
            text = console.input("\n[bold white3]Enter TEXT Prompt (use '\ n' for other prompt) : \n")
            if text == "RESET":
                Loop_Mode = console.input("[bold white3]LOOP MODE [ON/OFF] : ")
                text = console.input("\n[bold white3]Enter TEXT Prompt (use '\ n' for other prompt) : \n")
            time.sleep(1)
            continue