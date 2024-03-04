from flask import Flask, render_template, request, jsonify
import os
from flask_cors import CORS
import shutil
import time

app = Flask(__name__)
CORS(app)
app.debug = True

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # not including  symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    
    return total_size / (1024 * 1024)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Got POST method")
        try:
            count = request.form.get('classCount')

            for i in range(int(count)):
                classNum = "className" + str(i)
                className = request.form.get(classNum)

                class_folder = os.path.join(app.config['UPLOAD_FOLDER'], className)
                os.makedirs(class_folder, exist_ok=True)

                imageName = "images" + str(i)
                files = request.files.getlist(imageName)
                for i,img in enumerate(files):
                    if allowed_file(img.filename):
                        filename = str(i) + ".png"
                        img.save(os.path.join(class_folder, filename))
                        print(i, end="")
            print("Uploaded file size: ", end="")
            print(get_size("./uploads"), 'MB')

            time.sleep(5)
            shutil.rmtree("./uploads", ignore_errors=True)

            return jsonify({"message": "Images uploaded successfully!"}),200
        
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Internal server error'}), 500
        
    return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)
