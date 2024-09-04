import requests
import os
import time

LEONARDO_API_KEY = os.getenv("LEONARDO_API_KEY")

def generate_image(prompt):
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {LEONARDO_API_KEY}"
    }
    payload = {
        "prompt": prompt,
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
        "width": 768,
        "height": 768,
        "num_images": 1,
        "promptMagic": True
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        generation_id = response.json()["sdGenerationJob"]["generationId"]
        return get_generated_image(generation_id)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error in image generation: {str(e)}")

def get_generated_image(generation_id):
    url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {LEONARDO_API_KEY}"
    }
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            generated_images = response.json()["generations_by_pk"]["generated_images"]
            if generated_images:
                return generated_images[0]["url"]
            time.sleep(5)  # Wait 5 seconds before trying again
        except requests.exceptions.RequestException:
            if attempt == max_attempts - 1:
                raise
            time.sleep(5)
    return None
