from flask import Flask, request
from flask_cors import CORS, cross_origin
import cPickle as pickle
import json
import pandas as pd
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from sklearn.ensemble import GradientBoostingClassifier

def add_protein_characteristics(df):
    df = df.copy()
    aa_list = ['A', 'C','E','D','G','F','I','H','K','M','L','N','Q','P','S','R','T','W','V','Y']
    aa_dict = {}
    for aa in aa_list:
        aa_dict[aa] = []
    prop_dict = {'aromaticity': [], 'helix': [], 'turn': [], 'sheet': [], 'isoelectric_point': [], 'gravy': []} #, 'flexibility': [], 'instability_index': []}
    for i, s in enumerate(df['sequence']):
        s = s.replace('B', 'D').replace('Z', 'E').replace('J', 'L').replace('X', 'G').replace('U', 'C').replace('O', 'K')
        pa = ProteinAnalysis(s)
        prop_dict['aromaticity'].append(pa.aromaticity())
        prop_dict['isoelectric_point'].append(pa.isoelectric_point())
        prop_dict['gravy'].append(pa.gravy())
        # prop_dict['instability_index'].append(pa.instability_index())
        # prop_dict['flexibility'].append(np.mean(pa.flexibility()))
        for fraction, ss in zip(pa.secondary_structure_fraction(), ['helix', 'turn', 'sheet']):
            prop_dict[ss].append(fraction)
        for k, v in pa.get_amino_acids_percent().items():
            aa_dict[k].append(v)
    for k, v in aa_dict.items():
        df[k] = v
    for k, v in prop_dict.items():
        df[k] = v
    return df


def protein_input_to_pred_df(text, model):
    entries = text.split()
    df = pd.DataFrame(data=entries, columns=['sequence'])
    X = add_protein_characteristics(df)
    X = X.drop(['sequence'], axis=1)
    df['prediction'] = model.predict(X)
    return df

application = Flask(__name__)
CORS(application)

@application.route('/predict-allergens', methods=['POST'])
def predict_allergens():
    data = json.loads(request.data)
    df = protein_input_to_pred_df(data['text_input'], allergen_model)
    return df.T.to_json()

if __name__ == "__main__":
    with open('allergen_model.pkl', 'r') as fin:
        allergen_model = pickle.load(fin)
    application.run()
