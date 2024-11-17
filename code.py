!pip install sentence_transformers


from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/clip-ViT-B-32")


from sentence_transformers import SentenceTransformer, util
from PIL import Image

#Load CLIP model
model = SentenceTransformer('clip-ViT-B-32')

#Encode an image:
img_emb = model.encode(Image.open('download.jpg'))

#Encode text descriptions
text_emb = model.encode(['Two dogs in the snow'])

#Compute cosine similarities
cos_scores = util.cos_sim(img_emb, text_emb)
print(cos_scores)


!pip install requests beautifulsoup4 pillow sentence-transformers


# Example user prompt
user_prompt = "Show me towels of the same type but in different colors."


!pip install sentence-transformers pillow requests flask



from sentence_transformers import SentenceTransformer
from PIL import Image

# Load CLIP model
model = SentenceTransformer('clip-ViT-B-32')

# Load the input image
input_image_path = '/content/download.jpg'  # Replace with actual image path
input_image = Image.open(input_image_path)

# Encode the image into an embedding
image_embedding = model.encode(input_image)

# Print the shape of the embedding
print("Embedding shape:", image_embedding.shape)



# Input prompt from the user
user_prompt = "Show me similar towels"  # Example prompt

# Encode the text prompt into an embedding
prompt_embedding = model.encode(user_prompt)
import requests
from io import BytesIO

def search_images_on_api(query):
    # Example with Unsplash API
    api_key = 'wTyfFBDn0SqcIMqKOhY-v4IzygHAmNgBBlOsPbE9SdU'
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={api_key}"
    response = requests.get(url)
    return response.json()

# Get image results for the user's prompt
search_results = search_images_on_api(user_prompt)
similar_images_urls = [img['urls']['small'] for img in search_results['results']]

# Download and encode similar images
similar_images_embeddings = []
for img_url in similar_images_urls:
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    img_embedding = model.encode(img)
    similar_images_embeddings.append(img_embedding)
from sentence_transformers import util

# Compare input image with similar images using cosine similarity
similarity_scores = util.cos_sim(image_embedding, similar_images_embeddings)

# Output the top N most similar images
top_n = 7
top_matches = sorted(zip(similarity_scores[0], similar_images_urls), reverse=True)[:top_n]
for score, img_url in top_matches:
    print(f"Similarity score: {score.item()} - Image URL: {img_url}")
from PIL import Image
import requests

from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

inputs = processor(text=["a photo of a cat", "a photo of a dog"], images=image, return_tensors="pt", padding=True)

outputs = model(**inputs)
logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1)  # we can take the softmax to get the label probabilities
!pip install flask-ngrok
!pip install flask transformers pillow requests


!pip install transformers Pillow requests
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

img_url ='shampoo.png'
raw_image = Image.open(img_url).convert('RGB')

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
!pip install anvil-uplink


import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import anvil.server

# Initialize BLIP processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Define a function to process the image and perform the search
@anvil.server.callable
def process_image_and_search(img_url, user_prompt):
    # Load image from the URL
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

    # Generate image caption using BLIP
    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    # Merge the caption with the user-defined prompt
    combined_text = f"{user_prompt}: {caption}"

    # Perform SerpAPI search
    api_key = "your_serpapi_key"  # Replace with your SerpAPI key
    search_url = f"https://serpapi.com/search.json?q={combined_text}&api_key={api_key}"
    response = requests.get(search_url).json()

    # Collect and return search results
    search_results = []
    for result in response.get('organic_results', []):
        search_results.append({'title': result['title'], 'link': result['link']})

    return search_results
import requests

# SerpAPI setup
api_key = "4a3e1f0609cb7e3cf138e436f4d2b162a6d0d6e1e3efc68cd199e2807ee395a5"


def serp_search(combined_text, api_key):
    url = f"https://serpapi.com/search.json?q={combined_text}&api_key={api_key}"
    response = requests.get(url)
    return response.json()

# Define combined_text with your desired search query
combined_text = ""  # Replace with your actual query

results = serp_search(combined_text, api_key)

# Display search results
for result in results['organic_results']:
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
import requests

# SerpAPI setup
api_key = "4a3e1f0609cb7e3cf138e436f4d2b162a6d0d6e1e3efc68cd199e2807ee395a5"


def serp_search(combined_text, api_key):
    url = f"https://serpapi.com/search.json?q={combined_text}&api_key={api_key}"
    response = requests.get(url)
    return response.json()

# Define combined_text with your desired search query
combined_text = ""  # Replace with your actual query

results = serp_search(combined_text, api_key)

# Display search results
for result in results['organic_results']:
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
anvil.server.wait_forever()
