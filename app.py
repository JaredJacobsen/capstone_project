from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
from utils import convert_acc_nums_to_df, add_protein_characteristics
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
    data = json.loads(request.data)
    df = convert_acc_nums_to_df(data['text_input'])
    X = add_protein_characteristics(df['sequence'].to_frame())
    X = X.drop(['sequence'], axis=1)
    df['prediction'] = allergen_model.predict(X)
    return df.T.to_json()

##dont forget to add database

if __name__ == "__main__":
    with open('allergen_demo/allergen_model.pkl', 'r') as fin:
        allergen_model = pickle.load(fin)
    app.run()
