from flask import Flask, render_template, request, jsonify
import requests
import uuid
import json

app = Flask(__name__)

# Azure Translator Credentials
key = "Da3hWUISx6oL62qO6ekSu5tX7jOLipCEREoehxms1QV7vg8isPhrJQQJ99CEACNns7RXJ3w3AAAbACOGEAha"
endpoint = "https://api.cognitive.microsofttranslator.com/"
location = "koreacentral"

path = '/translate'
constructed_url = endpoint + path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    text = request.json['text']
    target_language = request.json['language']

    params = {
        'api-version': '3.0',
        'to': target_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    response = requests.post(
        constructed_url,
        params=params,
        headers=headers,
        json=body
    )

    result = response.json()

    translated_text = result[0]['translations'][0]['text']

    return jsonify({
        'translated_text': translated_text
    })

if __name__ == '__main__':
    app.run(debug=True)