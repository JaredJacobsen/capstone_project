from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
from utils import convert_acc_nums_to_X
import cPickle as pickle
import json

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    print request.data
    return json.dumps({'predictions': 1})

@app.route('/predict_allergens', methods=['POST'])
def predict_allergens():
    print request.data
    data = json.loads(request.data)
    X = convert_acc_nums_to_X(data['text_input'])
    predictions = allergen_model.predict(X)
    return json.dumps({'predictions': predictions})

##dont forget to add database

if __name__ == "__main__":
    with open('allergen_demo/allergen_model.pkl', 'r') as fin:
        allergen_model = pickle.load(fin)
    app.run()
