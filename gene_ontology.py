import cPickle as pickle
from utils import create_balanced_df, add_protein_characteristics
import xml.etree.ElementTree as ET
import itertools
import sys
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier

if __name__ != '__main__':
    with open('pickles/go_dict.pkl', 'r') as fin:
        go_dict = pickle.load(fin)
    with open('pickles/protein_dict.pkl', 'r') as fin:
        protein_dict = pickle.load(fin)
    with open('pickles/gene_dict.pkl', 'r') as fin:
        gene_dict = pickle.load(fin)
    # print 'starting to load neg_go_dict'
    # with open('pickles/neg_go_dict.pkl', 'r') as fin:
    #     neg_go_dict = pickle.load(fin)
    # print 'finished loading neg_go_dict'

def build_GO_model(go_id):
    pos_sequences = [protein_dict[a_num] for a_num in go_dict[go_id]]
    pos_sequences = list(set(pos_sequences))
    if len(pos_sequences) < 50:
        return None

    with open('data/Rocchio_human_MF_names.txt', 'r') as fin:
        for l in fin:
            if l[3:10] == go_id:
                neg_go_genes = l.split()[1:]
                break

    neg_sequences = [[protein_dict[a_num] for a_num in gene_dict[g]] for g in neg_go_genes]
    neg_sequences = [s for lst in neg_sequences for s in lst]
    neg_sequences = list(set(neg_sequences))

    df = create_balanced_df(pos_sequences, neg_sequences, 'go')
    df = add_protein_characteristics(df)

    X = df.drop(['sequence','go'], axis=1)
    y = df['go']
    rf = RandomForestClassifier()
    rf.fit(X, y)
    return rf

def create_GO_dicts():
    NMSP = {'up': 'http://uniprot.org/uniprot'}
    names_list = []

    go_dict = defaultdict(list)
    protein_dict = {}
    gene_dict = defaultdict(list)

    context = itertools.islice(ET.iterparse('data/uniprot_sprot.xml', events=('start', 'end')), 0, sys.maxint)
    _, root = context.next()

    for event, elem in context:
        if event == 'end' and elem.tag == '{http://uniprot.org/uniprot}entry':
            acc_nums = elem.findall('./up:accession', namespaces=NMSP)
            acc_nums = [x.text for x in acc_nums]
            try:
                primary_acc_num = acc_nums[0]
                sequence = elem.find('./up:sequence', namespaces=NMSP).text
            except:
                print 'oops, apparently this protein does not have an accession number and/or sequence'
            refs = elem.findall('./up:dbReference', namespaces=NMSP)
            go_nums = [x.attrib['id'][3:] for x in refs if x.attrib['type'] == 'GO']
            gene_names = elem.findall('./up:gene/up:name', namespaces=NMSP)
            gene_names = [x.text for x in gene_names]
            organism_ref = elem.find('./up:organism/up:dbReference', namespaces=NMSP)
            organism_name = None
            if organism_ref is not None and organism_ref.attrib['type'] == 'NCBI Taxonomy':
                organism_name = organism_ref.attrib['id']
            for g in gene_names:
                gene_dict[(g, organism_name)].append(primary_acc_num)
            for n in go_nums:
                go_dict[n].append(primary_acc_num)
            for acc_num in acc_nums:
                protein_dict[acc_num] = sequence
            root.clear()
    return go_dict, protein_dict, gene_dict

# def create_neg_go_dict():
#     neg_go_dict = {}
#     with open('data/Rocchio_human_MF_names.txt', 'r') as fin:
#         for l in fin:
#             l = l.split()
#             go_name = l[0][3:]
#             genes = [(g, '9606') for g in l[1:] if g != 'NONE']
#             neg_go_dict[go_name] = genes

if __name__ == '__main__':
    go_dict, protein_dict, gene_dict = create_GO_dicts()
    # neg_go_dict = create_neg_go_dict()
    with open('pickles/go_dict.pkl', 'w') as fout:
        pickle.dump(go_dict, fout)
    with open('pickles/protein_dict.pkl', 'w') as fout:
        pickle.dump(protein_dict, fout)
    with open('pickles/gene_dict.pkl', 'w') as fout:
        pickle.dump(gene_dict, fout)
    # with open('pickles/neg_go_dict.pkl', 'w') as fout:
    #     pickle.dump(neg_go_dict, fout)
