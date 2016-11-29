from flask import Flask, request
from flask_cors import CORS, cross_origin
import cPickle as pickle
import json
import pandas as pd
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def input_to_nb_pred_df(text, model):
    entries = text.split()
    df = pd.DataFrame(data=entries, columns=['sequence'])
    X = df['sequence'].apply(lambda x: x.replace('B', 'D').replace('Z', 'E').replace('J', 'L').replace('X', 'G').replace('U', 'C').replace('O', 'K'))
    df['prediction'] = model.predict_proba(X)[:, 1]
    return df

application = Flask(__name__)
CORS(application)

@application.route('/predict-allergens', methods=['POST'])
def predict_allergens():
    data = json.loads(request.data)
    df = input_to_nb_pred_df(data['text_input'], allergen_model)
    return df.T.to_json()

if __name__ == "__main__":
    with open('./allergen_model.pkl', 'r') as fin:
        allergen_model = pickle.load(fin)
    application.run()
