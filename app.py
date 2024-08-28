from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPEN_API_KEY")

@app.route('/generate-post', methods=['POST'])
def generate_post():
    data = request.json
    topic = data.get('topic')
    tone = data.get('tone', 'neutral')
    length = data.get('length', 'medium')
    platform = data.get('platform', 'general')
    
    prompt = f"Generate a {length} {tone} post for {platform} about '{topic}'."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert social media content creator."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_post = response.choices[0].message['content']
        return jsonify({"post": generated_post})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate-title", methods=['POST'])
def generate_title():
    data = request.json
    post_content = data.get('post_content')

    prompt = f"Generate an attractive, consice title for this post:\n\n{post_content}"

    try:
        response = openai.ChatCompletion.create(
            model='',
            message=[
                {"role": "system", "content": "You are an expert at creating engaging titles for social media posts."},
                {"role": "user", "content": prompt}
            ]
        )
        generate_title = response.choices[0].message['content']
        return jsonify({"title": generate_title})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/generate-hashtags', methods=['POST'])
def generate_hashtags():
    data = request.json
    post_content = data.get('post_content')
    num_hashtags = data.get('num_hashtags', 5)

    prompt = f"Generate {num_hashtags} relevant and popularrelevant and popular hashtags for this post:\n\n{post_content}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at creating relevant and trending hashtags for social media posts."},
                {"role": "user", "content": prompt}
            ]            
        )
        generated_hashtags = response.choices[0].message['content'].split('\n')
        return jsonify({"hashtags": generated_hashtags})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/refine-post', methods=['POST'])
def refine_post():
    data = request.json
    post_content = data.get('post_content')
    refinement_instructions = data.get('refinement_instructions')
    
    prompt = f"Refine this post according to these instructions:\n\nPost: {post_content}\n\nInstructions: {refinement_instructions}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at refining and improving social media posts."},
                {"role": "user", "content": prompt}
            ]
        )
        refined_post = response.choices[0].message['content']
        return jsonify({"refined_post": refined_post})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', 'False') == 'True')