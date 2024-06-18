from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from ctransformers import AutoModelForCausalLM, AutoConfig
from werkzeug.security import generate_password_hash, check_password_hash
import torch

import torch

app = Flask(__name__)
auth = HTTPBasicAuth()

# Replace these with your username and password
users = {
    "admin": generate_password_hash("12345678")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

# Load the model and configuration only once at the start of the application
model_name = 'TheBloke/Mistral-7B-Instruct-v0.1-GGUF'
model_path = 'mistral-7b-instruct-v0.1.Q3_K_S.gguf'
config = AutoConfig.from_pretrained(model_name)
config.config.max_new_tokens = 2048
config.config.context_length = 4096
llm = AutoModelForCausalLM.from_pretrained(model_name, model_file=model_path, model_type='mistral', config=config,device_map="auto")

@app.route('/summarize', methods=['POST'])
@auth.login_required
def summarize():
    data = request.get_json()
    conversation = data.get("conversation", "")
    
    if not conversation:
        return jsonify({"error": "No conversation provided"}), 400

    prompt = f"""
    You are a highly skilled summarizer. Your task is to provide a detailed and accurate summary of the conversation below. Don't forget to include important keywords. Make it concise.

    Here is the conversation:

    {conversation}

    Summary:
    """

    # Generate the summary asynchronously to handle multiple requests simultaneously
    summary = generate_summary(prompt)
    
    return jsonify({"summary": summary})

def generate_summary(prompt):
    # Generate the summary using the preloaded model
    return llm(prompt)

if __name__ == '__main__':
    app.run(debug=False)
