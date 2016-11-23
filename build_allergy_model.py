import pandas as pd
import numpy as np
from utils import add_protein_characteristics
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
import cPickle as pickle
import sys

def build_model():
    with open('pickles/full_ABT_df.pkl', 'r') as fin:
        df = pickle.load(fin)

    gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, min_samples_leaf=17)

    X = df.drop(['sequence','allergen'], axis=1)
    y = df['allergen'].copy()

    gb.fit(X, y)

    with open('pickles/allergen_model.pkl', 'w') as fout:
        pickle.dump(gb, fout)

    #should modify to accept options
    if len(sys.argv) == 2 and sys.argv[1] == 'cv':
        print 'cross validation scores: ' + str(cross_val_score(rf, X, y, cv=5, scoring='f1')) + '\n'
    return gb

if __name__ == '__main__':
    build_model()
