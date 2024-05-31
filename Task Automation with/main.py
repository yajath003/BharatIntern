import os
import shutil
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
DIRECTORY_TO_ORGANIZE = os.path.join(app.static_folder, 'target')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DIRECTORY_TO_ORGANIZE, exist_ok=True)

FILE_TYPE_MAPPING = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Presentations": [".ppt", ".pptx"],
    "Archives": [".zip", ".rar", ".tar.gz"],
    "Others": []
}


def organize_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(filename)[1].lower()
            moved = False
            for folder, extensions in FILE_TYPE_MAPPING.items():
                if file_extension in extensions:
                    target_folder = os.path.join(directory, folder)
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    shutil.move(file_path, os.path.join(target_folder, filename))
                    moved = True
                    break
            if not moved:
                target_folder = os.path.join(directory, "Others")
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                shutil.move(file_path, os.path.join(target_folder, filename))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            shutil.move(file_path, os.path.join(DIRECTORY_TO_ORGANIZE, file.filename))
            return redirect(url_for('index'))
    return render_template('upload.html')


@app.route('/organize', methods=['POST'])
def organize():
    organize_files(DIRECTORY_TO_ORGANIZE)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
