from flask import request, make_response, render_template, current_app, jsonify
import os
from flask import Blueprint
import requests
from PIL import Image
from app.model import Subject

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")

model_keras = 'test.h5'

IMG_WIDTH, IMG_HEIGHT = 160, 160
TARGET_SIZE = (IMG_WIDTH, IMG_HEIGHT)

@predict_bp.route('/', methods=['POST'])
def predict():
    filename = request.form['filename']
    img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    img = Image.open(img_path).convert('RGB')
    img = img.resize(TARGET_SIZE)
    #resized_img_name = "stamped_" + filename
    resized_img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    # inferenceAPIにリクエスト
    url = request.host_url + '/predict/api/inference'
    file = { "file": open(resized_img_path, 'rb') }
    response = requests.post(
        url,
        files=file,
    )
    json_obj= response.json()
    class_index= int(json_obj['class_index'])
    result = Subject.name(class_index)

    response = make_response(render_template("result.html", result = result, filename=filename))
    response.set_cookie('result_index', value=str(class_index))
    response.set_cookie('filename', value=filename)

    return response

@predict_bp.route('/api/inference', methods=['POST'])
def inference():
    file = request.files['file']

    path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)
    from keras.preprocessing import image as preprocessing
    img = preprocessing.load_img(path, target_size=TARGET_SIZE)
    img = preprocessing.img_to_array(img)
    import numpy as np
    x = np.expand_dims(img, axis=0)
    del file
    from tensorflow import keras
    keras.backend.clear_session()
    import gc
    gc.collect()
    from tensorflow.keras.models import load_model
    path = os.path.join(current_app.config['MODEL_FOLDER'], model_keras)
    model = load_model(path, compile=False)
    predict = model.predict(x)
    for p in predict:
        class_index = p.argmax()
        probablity = p.max()
        return jsonify({"result":"OK", "class_index":str(class_index), "probality":str(probablity)})