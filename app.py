from flask import Flask, request, jsonify, render_template_string
import pandas as pd
from PyPDF2 import PdfReader
import csv
from werkzeug.utils import secure_filename
import os

import cc

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB Max limit.
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure upload folder exists

# HTML Template with integrated CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CoherentComposer</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', sans-serif;
        }
        html, body {
            height: 100%;
            background-color: #000000;  /* Black background */
            color: #FFFFFF;  /* White text */
        }
        body {
            display: flex;
            flex-direction: column;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 30px;
            background-color: #333;  /* Dark gray */
            color: #ffffff;
        }
        nav a {
            color: #fff;
            text-decoration: none;
            margin-left: 20px;
        }
        main {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: #222;  /* Darker gray */
            padding: 20px;
            border-radius: 8px;
            width: 100%;
            max-width: 600px;
        }
        h1 {
            color: #FFF;
        }
        input[type="number"], textarea, input[type="file"], button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        button {
            background-color: #3498DB;  /* Blue */
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #85C1E9;  /* Lighter blue */
        }
        #outputText {
            background-color: #444;  /* Light black */
            color: #FFF;
            padding: 10px;
            margin-top: 20px;
            border-left: 5px solid #3498DB;  /* Blue */
            font-size: 14px;
        }
        footer {
            text-align: center;
            padding: 10px 0;
            background-color: #333;
            color: #ffffff;
            width: 100%;
        }
        .logo {
    width: 80px;  /* Adjusted for better visibility */
    height: auto;  /* Maintain aspect ratio */
    padding: 10px; /* Adds space around the logo */
}

header div, nav {
    display: flex;
    align-items: center;
    justify-content: center;
}

nav a {
    color: #fff;
    text-decoration: none;
    padding: 0 20px; /* More readable navigation */
}

/* Ensure the header has sufficient padding and space */
header {
    padding: 15px 30px;
    background-color: #333;
    color: #ffffff;
}

    </style>
</head>
<body>
    <header>
    <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
        <img src="static/image/logo.png" alt="Logo" class="logo" style="margin-right: auto;">
        <div>CoherentComposer Platform</div>
        <nav style="margin-left: auto;">
            <a href="/">Home</a>
            <a href="/about">About Us</a>
        </nav>
    </div>
    </header>


    <main>
        <div class="container">
            <h1>Welcome to CoherentComposer</h1>
            <input type="number" id="number" placeholder="Enter number of categories" min="1" max="10" />
            <button onclick="addInputs()">Generate Inputs</button>
            <form action="/submit" method="post" id="inputContainer"></form>
            <input type="file" id="fileInput" style="margin-top: 10px;">
            <button onclick="uploadFile()">Upload</button>
            <div id="outputText"></div>
        </div>
    </main>
    <footer> 2024 CoherentComposer. All rights reserved.</footer>

    <script>
        function addInputs() {
            var number = document.getElementById('number').value;
            var container = document.getElementById('inputContainer');
            container.innerHTML = ''; // Clear previous inputs
            for (var i = 0; i < number; i++) {
                container.innerHTML += '<input type="text" id="box '+ i'" name="category[]" placeholder="Enter Category ' + (i + 1) + '"/><br/>';
            }
            container.innerHTML += '<button type="submit">Submit Categories</button>';
        }
        document.addEventListener('DOMContentLoaded', function() {
            window.uploadFile = async () => {
                const fileInput = document.getElementById('fileInput');
                if (!fileInput.files.length) {
                    document.getElementById('outputText').textContent = 'Please select a file first.';
                    return;
                }
                const file = fileInput.files[0];
                const formData = new FormData();
                formData.append('file', file);

                try {
                    const response = await fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    document.getElementById('outputText').textContent = 'File uploaded successfully.';
                } catch (error) {
                    document.getElementById('outputText').textContent = 'Failed to upload file: ' + error.message;
                }
            };
        });
    </script>
</body>
</html>
"""

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB Max limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure upload folder exists

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/about')
def about():
    return "<h1>About Us</h1><p>This is the About Us page for CoherentComposer.</p>"

@app.route('/submit', methods=['POST'])
def submit_form():
    categories = request.form.getlist('category[]')
    # Generate the essay based on the categories
    essay = generate_essay(categories)
    return jsonify({'status': 'success', 'essay': essay})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(file_path)
        return jsonify({'status': 'success', 'message': 'File uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_essay(categories):
    # Example function to generate essay based on categories
    essay = "Generated Essay:\n"
    for category in categories:
        essay += f"\nCategory: {category}\nContent related to {category}..."
    return essay

if __name__ == '__main__':
    app.run(debug=True, port=5005)
