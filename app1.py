from flask import Flask, render_template, request, jsonify
import os
from config import app_config
from cc import generate_content_chunk #, upload_file_handler

app = Flask(__name__)
app.config.from_object(app_config)

@app.route('/')
def index():
    return render_template('home.html')

#@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    categories = request.form.getlist('category[]')
    essay = generate_content_chunk(categories)
    return jsonify({'status': 'success', 'essay': essay})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    return upload_file_handler(request)

if __name__ == '__main__':
    app.run(debug=True)
