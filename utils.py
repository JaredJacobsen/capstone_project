import pandas as pd
import numpy as np
import math
import re
import requests
import StringIO

from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

def get_sequences_from_fasta(fin):
    fasta_sequences = SeqIO.parse(fin,'fasta')
    return [str(fasta.seq) for fasta in fasta_sequences]

#Accepts fasta header and returns (db, unique_identifier, entry_name, protein_name, organism_name)
def parse_description(d):
    p = '(\w{2})\s*\|\s*([\w\d]+)\s*\|\s*(.*?)\s(.*?)\sOS=([\w]* [\w]*)'
    group_object = re.match(p, d)
    return group_object.group(1, 2, 3, 4, 5)

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

def parse_fasta_str(fasta_str):
    fin = StringIO.StringIO(fasta_str)
    fasta_sequences = SeqIO.parse(fin,'fasta')
    return [list(parse_description(f.description)) + [str(f.seq)] for f in fasta_sequences]

#assumes pos_sequences outnumbers neg_sequences
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
    prop_dict = {'aromaticity': [], 'instability_index': [], 'helix': [], 'turn': [], 'sheet': []}
    for i, s in enumerate(df['sequence']):
        pa = ProteinAnalysis(s)
        prop_dict['aromaticity'].append(pa.aromaticity())
        prop_dict['instability_index'].append(pa.aromaticity())
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
    parsed_fasta = parse_fasta_str(fasta)
    df = pd.DataFrame(data=parsed_fasta, columns=['db', 'identifier', 'entry_name', 'protein_name', 'organism_name', 'sequence'])
    return df
