from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
from utils import protein_input_to_pred_df
from gene_ontology import build_GO_model
import cPickle as pickle
import json

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    print request.data
    return json.dumps({'predictions': 1})

@app.route('/predict-allergens', methods=['POST'])
def predict_allergens():
    data = json.loads(request.data)
    df = protein_input_to_pred_df(data['text_input'], allergen_model)
    return df.T.to_json()

@app.route('/build-GO-model', methods=['POST'])
def set_GO_model():
    data = json.loads(request.data)
    go_id = data['go_id']
    GO_model = build_GO_model(go_id)

@app.route('/predict-GO', methods=['POST'])
def predict_gene_ontology():
    data = json.loads(request.data)
    df = protein_input_to_pred_df(data['text_input'], GO_model)
    return df.T.to_json()

if __name__ == "__main__":
    GO_model = None
    with open('pickles/allergen_model.pkl', 'r') as fin:
        allergen_model = pickle.load(fin)
    app.run()
