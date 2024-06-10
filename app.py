from flask import Flask, request, jsonify, render_template_string, render_template
import pandas as pd
from PyPDF2 import PdfReader
import csv
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB Max limit.
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure upload folder exists

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return "<h1>About Us</h1><p>This is the About Us page for CoherentComposer.</p>"

@app.route('/submit', methods=['POST'])
def submit_form():
    file = request.files['file']
    categories = request.form.getlist('category[]')
    return jsonify({'status': 'success', 'categories': categories, 'message': 'File and data processed'})

    # Process categories
    print("Categories: ", categories)

    # Save file if it exists
    if file and file.filename:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"File saved to {file_path}")

    # Generate the response based on the categories
    essay = generate_essay(categories)
    return jsonify({'status': 'success', 'essay': essay})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Combining the file upload and form submission in one route
    file = request.files.get('file')
    categories = request.form.getlist('category[]')

    if file and file.filename:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    
    essay = generate_essay(categories)
    return jsonify({'status': 'success', 'message': 'File uploaded successfully', 'essay': essay})

def generate_essay(categories):
    # Example function to generate essay based on categories
    essay = "Generated Essay:\n"
    for category in categories:
        essay += f"\nCategory: {category}\nContent related to {category}..."
    return essay

if __name__ == '__main__':
    app.run(debug=True, port=5005)
