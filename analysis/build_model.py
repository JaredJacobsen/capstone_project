import pandas as pd
import numpy as np
import math
import re

from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

def get_sequences_from_fasta(fin):
    fasta_sequences = SeqIO.parse(fin,'fasta')
    return [str(fasta.seq) for fasta in fasta_sequences]

def get_accession_nums(s)
    pattern = r'\(([\w\d]{6})\)'
    accession_nums = re.findall(pattern, s)
    return accession_nums

if __name__ == "__main__":
    pass
