!pip install transformers Pillow requests
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg' 
raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

# conditional image captioning
text = "a photography of"
inputs = processor(raw_image, text, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))
# >>> a photography of a woman and her dog

# unconditional image captioning
inputs = processor(raw_image, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))


!pip install flask-ngrok
!pip install flask transformers pillow requests

import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Initialize BLIP processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Example image URL (you can replace it with any image URL)
img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg' 
raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

# Generate image caption using BLIP
inputs = processor(raw_image, return_tensors="pt")
out = model.generate(**inputs)
caption = processor.decode(out[0], skip_special_tokens=True)

# User-defined prompt
user_prompt = "show me images like this"

# Merge the BLIP caption with the user prompt
combined_text = f"{user_prompt}: {caption}"

# Output the final combined text
print("Combined Text:")
print(combined_text)


import requests

# SerpAPI setup
api_key = "4a3e1f0609cb7e3cf138e436f4d2b162a6d0d6e1e3efc68cd199e2807ee395a5"


def serp_search(combined_text, api_key):
    url = f"https://serpapi.com/search.json?q={combined_text}&api_key={api_key}"
    response = requests.get(url)
    return response.json()

results = serp_search(combined_text, api_key)

# Display search results
for result in results['organic_results']:
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
