# Install necessary packages
!pip install --upgrade transformers
!pip install torch
!pip install gradio
!pip install pyngrok
!pip install pillow

# Imports
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
from PIL import Image
import requests
from io import BytesIO
import gradio as gr
from pyngrok import ngrok
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# Set your token here
access_token="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"

api_key='BSAkgKhqFS9TeHpQ3HWSFZDS_pumn_7'
subscription_token="BSAkgKhqFS9TeHpQ3HWSFZDS_pumn_7"

model=AutoModelForCausalLM.from_pretrained( "meta-llama/Llama-3.2-1B-Instruct",use_auth_token=access_token)
tokenizer=AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct",use_auth_token=access_token)


model_id = "meta-llama/Llama-3.2-1B-Instruct"


pipe = pipeline("text-generation", model=model_id, torch_dtype=torch.bfloat16,device_map="auto",)






# Function to process image and user prompt
def process_input(image, user_prompt):
    try:
        if image is not None:
            image = image.convert("RGB")
        else:
            return "No image provided.", "", ""

        # Preprocess image
        inputs = processor(image, return_tensors="pt").to(device)

        # Generate image caption
        with torch.no_grad():
            caption_ids = blip_model.generate(**inputs)
            image_context = processor.decode(caption_ids[0], skip_special_tokens=True)

        # Build prompt
        messages = [
            {
                "role": "system",
                "content": """You are an intelligent assistant refining search queries by combining image descriptions and user queries.
Always prioritize the user's query, using the image context only when relevant.
Your output must be a clean, concise, and to-the-point search query with no additional explanations, phrases, or unnecessary words."""
            },
            {
                "role": "user",
                "content": f"Image description: {image_context} \nUser's question: {user_prompt}"
            }
        ]

        outputs = pipe(messages, max_new_tokens=64)
        refined_question = outputs[0]["generated_text"][-1]['content']

        # Web search using Brave API
        params = {'q': refined_question, 'count': 10, 'offset': 0}
        headers = {
            'Authorization': f'Bearer {api_key}',
            'x-subscription-token': subscription_token
        }
        response = requests.get("https://api.search.brave.com/res/v1/web/search", headers=headers, params=params)
        if response.status_code != 200:
          return image_context, refined_question, f"Error: Brave API returned status code {response.status_code} — {response.text}"

        search_results = response.json()

        web_results = search_results.get("web", {}).get("results", [])
        output = ""
        if web_results:
            for result in web_results:
                title = result.get("title", "No title available")
                url = result.get("url", "No URL available")
                output += f'<a href="{url}" target="_blank">{title}</a><br><br>'
        else:
            output = "No results found."

        return image_context, refined_question, output

    except Exception as e:
        return "Error during processing", "", f"Exception: {str(e)}"



# Create Gradio interface
iface = gr.Interface(
    fn=process_input,
    inputs=[
        gr.Image(type="pil", label="Drop Image or Upload"),
        gr.Textbox(lines=1, placeholder="Enter your question here...", label="User Question")
    ],
    outputs=[
        gr.Textbox(label="Image Context"),
        gr.Textbox(label="Final Search Query"),
        gr.HTML(label="Search Results")
    ],
    title="Google Lens Pro Max",
    description="""
    <h4 style='font-size: 18px; text-align: center;'>Image and Question-based Search Assistant</h4>
    <p>Upload an image, enter your question, and get relevant search results along with image results.</p>
    """
)

# Ngrok setup
ngrok.kill()
!ngrok config add-authtoken 2nKvobAogGY1eWBnw3DBIOKBIKn_6HSLYUkA2iSfreYyTN3XY

# Start a new tunnel
public_url = ngrok.connect(7860)
print(f"Public URL: {public_url}")

# Launch the Gradio interface
iface.launch()
