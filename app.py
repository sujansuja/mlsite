from flask import Flask, request, jsonify, send_file
import os
import shutil
from werkzeug.utils import secure_filename
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/', methods=['POST'])
def upload_images():
    # try:
    #     class_count = request.form.get('classCount')
    #     return jsonify({'classCount': class_count})
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
        # classCount = request.form.get('classCount', 10)
        # uploaded_files = request.files.getlist('imgData', [])
        # numbers = request.form.getlist('numbers[]')

        # class_folders = []
        # for class_name in class_names:
        #     class_folder = os.path.join(app.config['UPLOAD_FOLDER'], class_name)
        #     os.makedirs(class_folder, exist_ok=True)
        #     class_folders.append(class_folder)

        # for item in uploaded_files:
            # class_name = item.get('className')
            # class_folders.append(class_name)
            # print(class_name)

        # uploaded_filenames = []
        # for i, file in zip(numbers,uploaded_files):
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         class_folder = class_folders[int(i)-1]
        #         file_path = os.path.join(class_folder, filename)
        #         file.save(file_path)
        #         uploaded_filenames.append(filename)

        

    try:

        class_count = request.form.get('classCount', 0)
        img_data = request.form.getlist('imgData', [])

        for item in img_data:
            class_name = item.get('className')
            images = item.get('images', [])

            class_folder = os.path.join('upload_folder', class_name)
            os.makedirs(class_folder, exist_ok=True)

            for i, image_data in enumerate(images):
                filename = image_data.get('filename', f'img_{i}.jpg')
                file_content = image_data.get('file_content')
                filepath = os.path.join(class_folder, filename)

                with open(filepath, 'wb') as file:
                    file.write(file_content)

        return jsonify({'message': 'Data successfully processed!'}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


if __name__ == '__main__':
    app.run(debug=True)
