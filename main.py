from flask import Flask, request, jsonify, send_file, render_template
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')


@app.route('/test', methods=['GET', 'POST'])
def testing():
    print(app.root_path)
    if request.method == 'POST':
        print("got post request")
        file = request.files.getlist('class1[]')
        target = os.path.join(app.root_path, 'static\\img\\class1\\')   
        if not os.path.isdir(target):
            os.makedirs(target)
        for i in file:
            print(i.filename)
            file_name = i.filename
            destination = '/'.join([target, file_name])
            i.save(destination)
        file = request.files.getlist('class2[]')
        target = os.path.join(app.root_path, 'static\\img\\class2\\')   
        if not os.path.isdir(target):
            os.makedirs(target)
        for i in file:
            print(i.filename)
            file_name = i.filename
            destination = '/'.join([target, file_name])
            i.save(destination)


        data = request.form
        print(data)
    return render_template('form.html')

@app.route('/', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        print("Recieved POST request")
        try:
            # print(request.form['requestData'])
            print(request.form)
            print(request.files)
            print(request.get_json)
            class_count = request.json['requestData']['classCount']
            # class_count = request.form.get('classCount', 0)
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

            return jsonify({'message': 'Files successfully uploaded and processed with class count: ' + str(request.json['requestData']['classCount'])}), 200

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Internal server error'}), 500

    else:
        return "Only POST requests are allowed", 405

if __name__ == '__main__':
    app.run(debug=True)
