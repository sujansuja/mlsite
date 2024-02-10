from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')


@app.route('/', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        print("Recieved POST request")
        try:
            class_count = request.form.get('classCount', 0)
            print(f"Class Count: {class_count}")
            img_data = request.files.getlist('imgData[]')

            upload_folder = 'upload_folder'
            os.makedirs(upload_folder, exist_ok=True)

            # Process uploaded files
            for image_file in img_data:
                class_name = request.form.get('className')
                class_folder = os.path.join(upload_folder, class_name)
                os.makedirs(class_folder, exist_ok=True)

                filename = image_file.filename
                filepath = os.path.join(class_folder, filename)
                image_file.save(filepath)
                print(f"Saved the file: {filename} to {filepath}")

            return jsonify({'message': 'Files successfully uploaded and processed!'}), 200

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Internal server error'}), 500

    else:
        return "Only POST requests are allowed", 405

if __name__ == '__main__':
    app.run(debug=True)
