from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
from utils import protein_input_to_pred_df
import cPickle as pickle
import json

application = Flask(__name__)
CORS(application)

@application.route('/predict-allergens', methods=['POST'])
def predict_allergens():
    data = json.loads(request.data)
    df = protein_input_to_pred_df(data['text_input'], allergen_model)
    return df.T.to_json()

if __name__ == "__main__":
    with open('pickles/allergen_model.pkl', 'r') as fin:
        allergen_model = pickle.load(fin)
    application.run()
