import requests
from configparser import ConfigParser
from PIL import Image

dbconf = ConfigParser()
dbconf.read_file(open("config.ini"))

# Replace "YOUR_DALL-E_API_KEY" with your own DALL-E API key
API_KEY = dbconf.get("SETTING","API_KEY")
Width_Size = dbconf.get("SETTING","WIDTH_SIZE")
High_Size = dbconf.get("SETTING","HIGH_SIZE")

Width_Size = int(Width_Size)
High_Size = int(High_Size)

# The text we want to generate an image for
text = dbconf.get("PROMPT","TEXT_PROMPT")

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
response = requests.post(endpoint, headers=headers, json=data)

# Get the URL of the generated image from the response
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
