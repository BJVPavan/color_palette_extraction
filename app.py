import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,send_file
from colorthief import ColorThief
import csv
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        
        color_thief = ColorThief(filepath)
        palette = color_thief.get_palette(color_count=6)

        return render_template('index.html', filename=filename, palette=palette)

@app.route('/download_palette')
def download_palette():
    palette = request.args.getlist('palette')  
    format = request.args.get('format', 'rgb')  

    if format == 'hex':
        palette = [rgb_to_hex(color) for color in palette]

    
    file_path = create_palette_file(palette, format)
    
    return send_file(file_path, as_attachment=True)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def create_palette_file(palette, format):
    if format == 'csv':
        file_name = 'palette.csv'
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Color'])
            for color in palette:
                writer.writerow([f'rgb{color}'])
    else:
        file_name = 'palette.json'
        with open(file_name, 'w') as jsonfile:
            json.dump(palette, jsonfile)

    return file_name

if __name__ == '__main__':
    app.run(debug=True)
