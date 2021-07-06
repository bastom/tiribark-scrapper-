import json
from flask import Flask, request
from tensorflow import keras
import tensorflow as tf
import numpy as np
from PIL import Image
import requests
import pickle

def requestResults(imageArray):
    #Get Classified Names from pre-trained Model
    f = open("classNames.obj", 'rb')
    class_names = pickle.load(f)

    #Load the trained model
    model = keras.models.load_model("model2")

    predictions = model.predict(imageArray)
    score = tf.nn.softmax(predictions[0])

    #Get the result
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(class_names[np.argmax(score)], 100 * np.max(score))
    )
    f.close()
    return ({
        "className": class_names[np.argmax(score)],
        "confidence": 100 * np.max(score)
    })


def getImageArrayFrom(link, img_size=500):
    image = Image.open(requests.get(link, stream=True).raw).resize((img_size, img_size))
    img_array = keras.preprocessing.image.img_to_array(image)
    return tf.expand_dims(img_array, 0)

def getObjectOf(shoe_id):
    f = open('./man.json', 'r')
    json_data = json.loads(f.readlines()[0])

    return next((item for item in json_data if item['id'] == shoe_id), None)

# start flask
app = Flask(__name__)

@app.route('/image')
def show_user_profile():
    f = open("classNames.obj", 'rb')
    class_names = pickle.load(f)

    link = request.args.get('link', '')
    imageArray = getImageArrayFrom(link)
    prediction = requestResults(imageArray)
    shoe_id = prediction['className']
    result = getObjectOf(shoe_id)
    result = {
        'title': result['name'].split(' ')[0],
        'description': result['name'],
        'price': '$ ' + str(result['price']),
        'link': result['link'],
        'confidence': prediction['confidence']
    }
    print(result)

    return result


app.run(debug=True)
