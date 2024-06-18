# Summarizer API

## Overview
Summarizer API is a Flask-based application that uses a pre-trained large language model (LLM) to generate summaries of provided conversations. The application is secured with HTTP Basic Authentication and leverages the `ctransformers` library to handle the model.

## Features
- **Authentication**: Secured with HTTP Basic Authentication to ensure only authorized users can access the API.
- **Asynchronous Summary Generation**: Handles multiple requests simultaneously using asynchronous operations.
- **Customizable Prompts**: Allows users to input their own conversation for summarization.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Clone the Repository
```bash
git clone https://github.com/yourusername/summarizer-api.git
cd summarizer-api
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Configuration

### Authentication Setup
Replace the `admin` username and password hash in the `users` dictionary with your own credentials:
```python
users = {
    "admin": generate_password_hash("yourpassword")
}
```

### Model Setup
Ensure you have the correct model name and path in the configuration:
```python
model_name = 'TheBloke/Mistral-7B-Instruct-v0.1-GGUF'
model_path = 'mistral-7b-instruct-v0.1.Q3_K_S.gguf'
```

## Usage

### Start the Application
Run the Flask application:
```bash
python app.py
```

### API Endpoint
#### `POST /summarize`
This endpoint takes a conversation in JSON format and returns a summary.

**Request:**
- **Headers:**
  - `Authorization: Basic <base64-encoded-credentials>`
- **Body:**
  ```json
  {
      "conversation": "Your conversation text here"
  }
  ```

**Response:**
- **Success:**
  ```json
  {
      "summary": "Generated summary of the conversation"
  }
  ```
- **Error:**
  ```json
  {
      "error": "No conversation provided"
  }
  ```

## Example
**Request:**
```bash
curl -X POST http://localhost:5000/summarize \
    -u admin:12345678 \
    -H "Content-Type: application/json" \
    -d '{"conversation": "Your conversation text here"}'
```

**Response:**
```json
{
    "summary": "Generated summary of the conversation"
}
```

## Code Explanation

### Imports and Configuration
```python
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from ctransformers import AutoModelForCausalLM, AutoConfig
from werkzeug.security import generate_password_hash, check_password_hash
import torch

app = Flask(__name__)
auth = HTTPBasicAuth()

# Replace these with your username and password
users = {
    "admin": generate_password_hash("12345678")
}
```
- The necessary libraries are imported.
- Flask and HTTPBasicAuth are set up for the web application and authentication.
- The pre-trained model is configured and loaded.

### Authentication Verification
```python
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
```
- A function to verify the user's password against the stored hash.

### Model Loading
```python
model_name = 'TheBloke/Mistral-7B-Instruct-v0.1-GGUF'
model_path = 'mistral-7b-instruct-v0.1.Q3_K_S.gguf'
config = AutoConfig.from_pretrained(model_name)
config.config.max_new_tokens = 2048
config.config.context_length = 4096
llm = AutoModelForCausalLM.from_pretrained(model_name, model_file=model_path, model_type='mistral', config=config, device_map="auto")
```
- The model is loaded once at the start to improve performance and handle multiple requests efficiently.

### Summarization Endpoint
```python
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

    summary = generate_summary(prompt)
    
    return jsonify({"summary": summary})
```
- A POST endpoint `/summarize` that takes a conversation and returns a summary.
- Requires authentication to access.
- Validates the input and generates a prompt for the model.

### Summary Generation Function
```python
def generate_summary(prompt):
    return llm(prompt)
```
- Generates a summary using the preloaded model.


This README provides a comprehensive overview of the Summarizer API, including installation instructions, usage examples, and a detailed explanation of the code. Replace placeholder values with your actual information before publishing.
