import pandas as pd
import numpy as np
import math
import re
import requests
import StringIO
import cPickle as pickle
import xml.etree.ElementTree as ET
import itertools
import sys
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

if __name__ != '__main__':
    with open('pickles/go_dict.pkl', 'r') as fin:
        go_dict = pickle.load(fin)
    with open('pickles/protein_dict.pkl', 'r') as fin:
        protein_dict = pickle.load(fin)
    with open('pickles/gene_dict.pkl', 'r') as fin:
        gene_dict = pickle.load(fin)

def get_sequences_from_fasta(fin):
    fasta_sequences = SeqIO.parse(fin,'fasta')
    return [str(fasta.seq) for fasta in fasta_sequences]

#Accepts fasta header and returns (db, unique_identifier, entry_name, protein_name, organism_name, gene_name)
def parse_description(d):
    organism_name = re.search('OS=(.*?)\s*(?:GN=|PE=)', d).group(1)
    gene_name = re.search('GN=(.*?)\s*PE=', d)
    if gene_name: gene_name = gene_name.group(1)
    db, unique_identifier, entry_name, protein_name = re.search('.*?(\w{2})\|([\w\d]+)\|(.*?)\s(.*?)\sOS=', d).group(1,2,3,4)
    return (db, unique_identifier, entry_name, protein_name, organism_name, gene_name)

#returns (db, unique_identifier)
def parse_allerhunt_description(d):
    print d
    return re.search('(\w{2})\|([\w\d]+)\|', d).group(1,2)

#Accepts fasta string and returns (db, unique_identifier, entry_name, protein_name, organism_name, gene_name, seqeunce)
def parse_fasta_str(fasta_str, parse_description_func=parse_description):
    fin = StringIO.StringIO(fasta_str)
    fasta_sequences = SeqIO.parse(fin,'fasta')
    return [list(parse_description_func(f.description)) + [str(f.seq)] for f in fasta_sequences]

def extract_accession_nums(s):
    pattern = '[\w\d]{6}'
    accession_nums = re.findall(pattern, s)
    return accession_nums

def get_fasta_from_uniprot(accession_nums):
    url = 'http://www.uniprot.org/uploadlists/'
    params = {
    'from':'ACC',
    'to':'ACC',
    'format':'fasta',
    'query': ' '.join(map(str, accession_nums)),
    }
    response = requests.get(url, params)
    return response.text


#assumes neg_sequences outnumbers pos_sequences
def create_balanced_df(pos_sequences, neg_sequences, target_column_name):
    pos_set = set(pos_sequences)
    neg_sequences = [seq for seq in neg_sequences if seq not in pos_set]
    neg_sequences = np.random.choice(neg_sequences, len(pos_sequences)).tolist()
    balanced_df = pd.DataFrame({'sequence': pos_sequences + neg_sequences,
                                target_column_name: [1]*len(pos_sequences) + [0]*len(neg_sequences)})
    return balanced_df

#accepts pandas df with sequence column. non_mutative df
def add_protein_characteristics(df):
    df = df.copy()
    aa_list = ['A', 'C','E','D','G','F','I','H','K','M','L','N','Q','P','S','R','T','W','V','Y']
    aa_dict = {}
    for aa in aa_list:
        aa_dict[aa] = []
    prop_dict = {'aromaticity': [], 'instability_index': [], 'helix': [], 'turn': [], 'sheet': [],
                'isoelectric_point': [], 'gravy': [], 'flexibility': []}
    for i, s in enumerate(df['sequence']):
        s = s.replace('B', 'D').replace('Z', 'E').replace('J', 'L').replace('X', 'G').replace('U', 'C').replace('O', 'K')
        pa = ProteinAnalysis(s)
        prop_dict['aromaticity'].append(pa.aromaticity())
        prop_dict['instability_index'].append(pa.instability_index())
        prop_dict['isoelectric_point'].append(pa.isoelectric_point())
        prop_dict['gravy'].append(pa.gravy())
        prop_dict['flexibility'].append(np.mean(pa.flexibility()))
        for fraction, ss in zip(pa.secondary_structure_fraction(), ['helix', 'turn', 'sheet']):
            prop_dict[ss].append(fraction)
        for k, v in pa.get_amino_acids_percent().items():
            aa_dict[k].append(v)
    for k, v in aa_dict.items():
        df[k] = v
    for k, v in prop_dict.items():
        df[k] = v
    return df

def convert_acc_nums_to_df(a_nums_str):
    a_nums = extract_accession_nums(a_nums_str)
    fasta = get_fasta_from_uniprot(a_nums)
    parsed_fasta = parse_fasta_str(fasta, parse_description)
    df = pd.DataFrame(data=parsed_fasta, columns=['db', 'identifier', 'entry_name', 'protein_name', 'organism_name', 'gene_name', 'sequence'])
    return df

def protein_input_to_pred_df(text, model):
    if len(text.split()[0]) > 7:
        df = pd.DataFrame(data=entries, columns=['sequence'])
        X = add_protein_characteristics(df)
    else:
        df = a_nums_to_df(text)
        X = add_protein_characteristics(df['sequence'].to_frame())
    X = X.drop(['sequence'], axis=1)
    df['prediction'] = model.predict(X)
    return df

def a_nums_to_df(a_nums_str, columns=None):
    a_nums = extract_accession_nums(a_nums_str)
    proteins = [protein_dict[a] for a in a_nums]
    if columns is None: columns = proteins[0].keys()
    columns_data = []
    for c in columns:
        columns_data.append([p[c] for p in proteins])
    df = pd.DataFrame(data=dict(zip(columns, columns_data)))
    return df

def build_GO_model(go_id):
    if go_id not in go_dict:
        print 'go id not in go_dict'
        return None
    pos_sequences = [protein_dict[a_num]['sequence'] for a_num in go_dict[go_id]]
    pos_sequences = list(set(pos_sequences))
    if len(pos_sequences) < 50:
        print 'len(pos_sequences) < 50'
        return None

    neg_go_genes = None
    with open('data/Rocchio_human_MF_names.txt', 'r') as fin:
        for l in fin:
            if l[3:10] == go_id:
                neg_go_genes = [g for g in l.split()[1:] if g != 'NONE']
                if len(neg_go_genes) > 0 and len(pos_sequences) < len(neg_go_genes):
                    break
                print 'not enough neg go genes'
                return None
    if neg_go_genes is None:
        print 'no neg genes found'
        return None
    neg_sequences = [[protein_dict[a_num]['sequence'] for a_num in gene_dict[(g, '9606')]] for g in neg_go_genes]
    neg_sequences = [s for lst in neg_sequences for s in lst]
    neg_sequences = list(set(neg_sequences))
    print 'neg_sequences before: ', len(neg_sequences)
    print 'pos_sequences before: ', len(pos_sequences)
    df = create_balanced_df(pos_sequences, neg_sequences, 'go')
    df = add_protein_characteristics(df)

    X = df.drop(['sequence','go'], axis=1)
    y = df['go']
    rf = RandomForestClassifier()
    rf.fit(X, y)
    return rf
