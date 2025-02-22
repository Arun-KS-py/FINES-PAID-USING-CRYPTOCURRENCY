from flask import Flask, send_from_directory, redirect, render_template, request, jsonify
from google.generativeai import configure, GenerativeModel
import os
import requests

app = Flask(__name__)

# Coinbase API Key (from environment variable)
COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
COINBASE_API_URL = 'https://api.commerce.coinbase.com'

configure(api_key="AIzaSyBtySQSt-YbnZU5XXAQIONfrMvgc05Jc2c")
gemini = GenerativeModel("gemini-pro")
# Serve HTML pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/feature.html')
def feature():
    return render_template('feature.html')

@app.route('/roadmap.html')
def roadmap():
    return render_template('roadmap.html')

@app.route('/token.html')
def token():
    return render_template('token.html')

@app.route('/service.html')
def service():
    return render_template('service.html')

@app.route('/404.html')
def fournotfour():
    return render_template('404.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/faq.html')
def faq():
    return render_template('faq.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('question')
    
    # Generate prompt based on user input
    if user_input == "How does this project help the government?":
        full_prompt = (
            "Explain how an automated crypto trading system helps governments generate profits "
            "by reinvesting fines and unused funds into stable crypto assets using AI strategies."
        )
    else:
        full_prompt = f"Provide a clear, crypto-specific response to: {user_input}. Keep it concise."

    # Get response from Gemini
    response = gemini.generate_content(full_prompt)
    return jsonify({'response': response.text})

# Serve static files (CSS, JS, images)
@app.route('/assets/<path:filename>')
def static_files(filename):
    return send_from_directory(ASSETS_FOLDER, filename)

# Create charge for payment (Coinbase API)
@app.route('/api/create_charge', methods=['POST'])
def create_charge():
    from flask import request, jsonify

    amount = request.form.get('amount')
    currency = request.form.get('currency')

    headers = {
        'Content-Type': 'application/json',
        'X-CC-Api-Key': COINBASE_API_KEY
    }

    payload = {
        'name': 'CryptoFinePay Token',
        'description': 'Payment for cryptocurrency fines',
        'pricing_type': 'fixed_price',
        'local_price': {
            'amount': amount,
            'currency': currency
        },
        'redirect_url': 'http://localhost:5000/',
        'cancel_url': 'http://localhost:5000/token'
    }

    response = requests.post(
        f'{COINBASE_API_URL}/charges',
        json=payload,
        headers=headers
    )

    if response.status_code == 201:
        return jsonify({'hosted_url': response.json()['data']['hosted_url']})
    else:
        return jsonify({'error': response.json()}), 500

if __name__ == '__main__':
    app.run(debug=True)
