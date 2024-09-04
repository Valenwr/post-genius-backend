import logging
import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI
from utils.leonardo_api import generate_image

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=250):
    """
    Generates a completion from the OpenAI model based on the given prompt.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise Exception(f"Error in generating completion: {str(e)}")

def generate_content(topic, content_type, platform):
    """
    Generates social media content based on the given topic, content type, and platform.
    """
    prompt = f"""Create a {content_type} social media post for {platform} about {topic}. 
    Focus on providing deep, informative content related to history, world curiosities, or general interest science. 
    The post should be engaging, educational, and optimized for {platform}. 
    Include relevant hashtags if appropriate."""
    
    try:
        content = get_completion(prompt)
        return content
    except Exception as e:
        raise Exception(f"Error in generating content: {str(e)}")

st.title("Deep Dive Social Media Content Generator")

topic = st.text_input("Enter a topic (e.g., 'Ancient Roman technology', 'Bioluminescent creatures', 'Quantum entanglement'):")

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Select social media platform:", ['Twitter', 'Instagram', 'Facebook'])
with col2:
    content_type = st.selectbox("Content type:", ['Historical fact', 'Scientific curiosity', 'World wonder', 'Technological marvel'])

if st.button("Generate Content"):
    if topic:
        with st.spinner("Generating content..."):
            try:
                post = generate_content(topic, content_type, platform)
                st.text_area("Generated Post:", post, height=200)
                logging.info(f"Generated {content_type} post for topic: {topic}")
                
                # Generate image
                try:
                    image_prompt = f"Create a visually striking image related to {topic}, focusing on {content_type}"
                    image_url = generate_image(image_prompt)
                    if image_url:
                        st.image(image_url, caption="Generated Image")
                        logging.info(f"Generated image for topic: {topic}")
                    else:
                        st.warning("Image generation is currently unavailable. Please try again later.")
                except Exception as img_e:
                    st.warning(f"Image generation failed: {str(img_e)}. Focusing on text content only.")
                    logging.error(f"Error in image generation: {str(img_e)}")
            except Exception as e:
                st.error(f"Failed to generate content: {str(e)}")
                logging.error(f"Error generating content: {str(e)}")
    else:
        st.warning("Please enter a topic.")

st.sidebar.title("Content Inspiration")
if st.sidebar.button("Get Random Topic Idea"):
    inspiration_prompt = "Suggest an interesting topic for a social media post related to history, world curiosities, or general interest science."
    try:
        topic_idea = get_completion(inspiration_prompt, max_tokens=50)
        st.sidebar.write(f"Topic Idea: {topic_idea}")
    except Exception as e:
        st.sidebar.error(f"Failed to generate topic idea: {str(e)}")

st.sidebar.title("About")
st.sidebar.info("This Deep Dive Social Media Content Generator uses OpenAI's GPT-3.5-turbo for text generation and Leonardo AI for image creation. It focuses on producing engaging, educational content about history, world curiosities, and general interest science topics.")
