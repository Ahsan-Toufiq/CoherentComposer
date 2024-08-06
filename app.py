from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from cc import *

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

    print("Categories: ", categories)

    file_path = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"File saved to {file_path}")

    essay = generate_essay(categories, file_path) if file_path else "No file uploaded."
    
    return render_template('index.html', essay=essay)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    categories = request.form.getlist('category[]')

    if file and file.filename:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    
    essay = generate_essay(categories, file_path)
    return jsonify({'status': 'success', 'message': 'File uploaded successfully', 'essay': essay})

def generate_essay(categories, file_path):
    csv_file = file_path

    return main(csv_file, categories)


if __name__ == '__main__':
    app.run(debug=True, port=5006)
