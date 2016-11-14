import pandas as pd
import numpy as np
from utils import get_sequences_from_fasta, create_balanced_df, add_protein_characteristics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import cPickle as pickle

def build_model():
    allergen_sequences = get_sequences_from_fasta(open('data/uniprot_allergens.fasta'))
    non_allergen_sequences = get_sequences_from_fasta(open('data/uniprot_sprot.fasta'))

    df = create_balanced_df(allergen_sequences, non_allergen_sequences, 'allergen')
    df = add_protein_characteristics(df)

    X = df.drop(['sequence','allergen'], axis=1)
    y = df['allergen']
    rf = RandomForestClassifier()
    print 'cross validation score: ' + str(np.mean(cross_val_score(rf, X, y, cv=5))) + '\n'
    rf.fit(X, y)
    with open('pickles/allergen_model.pkl', 'w') as fout:
        pickle.dump(rf, fout)
    return rf

if __name__ == '__main__':
    build_model()
