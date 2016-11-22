import cPickle as pickle
import xml.etree.ElementTree as ET
import itertools
import sys
from collections import defaultdict

def create_dicts_from_uniprot_xml(filename, max_events=sys.maxint):
    NMSP = {'up': 'http://uniprot.org/uniprot'}
    names_list = []

    protein_dict = {}
    gene_dict = defaultdict(list)

    context = itertools.islice(ET.iterparse(filename, events=('start', 'end')), 0, max_events)
    _, root = context.next()

    for event, elem in context:
        if event == 'end' and elem.tag == '{http://uniprot.org/uniprot}entry':
            db = elem.attrib['dataset']
            entry_name = elem.find('./up:name', namespaces=NMSP).text
            protein_name = elem.find('./up:protein//up:fullName', namespaces=NMSP).text
            sequence = elem.find('./up:sequence', namespaces=NMSP).text.strip('\n').replace('\n', '')

            allergen = elem.find('./up:protein//up:allergenName', namespaces=NMSP)
            allergen = allergen is not None

            ec_num = elem.find('./up:protein//up:ecNumber', namespaces=NMSP)
            ec_num = ec_num.text if ec_num is not None else None

            acc_nums = elem.findall('./up:accession', namespaces=NMSP)
            acc_nums = [x.text for x in acc_nums]
            primary_acc_num = acc_nums[0]

            gene_names = elem.findall('./up:gene/up:name', namespaces=NMSP)
            gene_names = [x.text for x in gene_names]

            organism_ref = elem.find('./up:organism/up:dbReference', namespaces=NMSP)
            organism_name = None
            if organism_ref is not None and organism_ref.attrib['type'] == 'NCBI Taxonomy':
                organism_name = organism_ref.attrib['id']

            for g in gene_names:
                gene_dict[(g, organism_name)].append(primary_acc_num)
            for acc_num in acc_nums:
                other_acc_nums = [a for a in acc_nums if a != acc_num]
                protein_dict[acc_num] = {'db': db, 'acc_num': acc_num, 'other_acc_nums': other_acc_nums,
                                         'entry_name': entry_name, 'protein_name': protein_name,
                                         'organism_name': organism_name, 'gene_names': gene_names,
                                         'allergen': allergen, 'ec_num': ec_num, 'sequence': sequence}
            root.clear()
    return protein_dict, gene_dict


if __name__ == '__main__':
    protein_dict, gene_dict = create_dicts_from_uniprot_xml('data/uniprot_sprot.xml')
    with open('pickles/protein_dict.pkl', 'w') as fout:
        pickle.dump(protein_dict, fout)
    with open('pickles/gene_dict.pkl', 'w') as fout:
        pickle.dump(gene_dict, fout)
