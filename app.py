import streamlit as st
from dotenv import load_dotenv
from models.text_generation import generate_text
from utils.leonardo_api import generate_image
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO)

st.title("Viral Post Assistant")

topic = st.text_input("Enter a topic for your viral post:")

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Select social media platform:", ['Twitter', 'Instagram', 'Facebook', 'LinkedIn', 'TikTok'])
with col2:
    post_type = st.selectbox("Select post type:", ['Informative', 'Controversial', 'Heartwarming', 'Humorous'])

if st.button("Generate Post"):
    if topic:
        with st.spinner("Generating post..."):
            prompt = f"Create a {post_type.lower()} viral social media post for {platform} about {topic}. The post should be engaging, shareable, and optimized for maximum reach. Include relevant hashtags if appropriate."
            try:
                post = generate_text(prompt)
                st.text_area("Generated Post:", post, height=200)
                logging.info(f"Generated post for topic: {topic}")
            except Exception as e:
                st.error("Failed to generate post. Please try again.")
                logging.error(f"Error generating post: {str(e)}")
    else:
        st.warning("Please enter a topic.")

if st.button("Generate Image"):
    if topic:
        with st.spinner("Generating image..."):
            image_prompt = f"Create a visually striking image related to the topic: {topic}. The image should be eye-catching and suitable for a viral social media post."
            try:
                image_url = generate_image(image_prompt)
                if image_url:
                    st.image(image_url, caption="Generated Image")
                    logging.info(f"Generated image for topic: {topic}")
                else:
                    st.error("Failed to generate image. Please try again.")
            except Exception as e:
                st.error("Failed to generate image. Please try again.")
                logging.error(f"Error generating image: {str(e)}")
    else:
        st.warning("Please enter a topic.")

st.sidebar.title("About")
st.sidebar.info("This Viral Post Assistant uses OpenAI's GPT-3.5-turbo for text generation and Leonardo AI for image generation. Enter a topic, choose your platform and post type, and let AI help you create viral content!")
