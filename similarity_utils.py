from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62
from skbio.alignment import local_pairwise_align_ssw
from skbio.sequence import Protein
from difflib import SequenceMatcher
import Levenshtein as lv

def seq_sim_of_alignment_pair(a):
    seq1, seq2 = a
    identity = 0
    similiarity = 0
    align_len = 0
    for i in xrange(min(len(seq1), len(seq2))):
        if seq1[i] == "-" and seq2[i] == "-":
            pass
        else:
            align_len += 1
            if seq1[i] == seq2[i]:
                identity += 1
                similiarity += 1
            elif seq1[i] in "GAVLI" and seq2[i] in "GAVLI":
                similiarity += 1
            elif seq1[i] in "FYW" and seq2[i] in "FYW":
                similiarity += 1
            elif seq1[i] in "CM" and seq2[i] in "CM":
                similiarity += 1
            elif seq1[i] in "ST" and seq2[i] in "ST":
                similiarity += 1
            elif seq1[i] in "KRH" and seq2[i] in "KRH":
                similiarity += 1
            elif seq1[i] in "DENQ" and seq2[i] in "DENQ":
                similiarity += 1
            elif seq1[i] in "P" and seq2[i] in "P":
                similiarity += 1
    return round(float(identity)/align_len, 2), round(float(similiarity)/align_len, 2)

def contig_seq_match(seq1, seq2, window_len=7):
    for i in xrange(0, len(seq1) - window_len):
        if seq1[i: i + window_len] in seq2:
            return True
    return False

def quick_seq_sim_ratio(s1, s2, thresh=0.95):
    sm = SequenceMatcher(None, s1, s2)
    if sm.real_quick_ratio() > thresh and sm.quick_ratio() > thresh and lv.ratio(s1, s2) > thresh:
        return True
    return False


def window_seq_sim(seq1, seq2, window_len=80, thresh=0.3):
    for i in xrange(0, len(seq1) - window_len):
        for j in xrange(0, len(seq2) - window_len):
#             a = pairwise2.align.globalds(seq1[i: i + window_len], seq2[j: j + window_len], blosum62, -10, -0.5, one_alignment_only=True)[0]
#             if seq_sim_of_alignment_pair((a[0], a[1]))[0] > thresh:
#                 return True
            s1, s2 = seq1[i: i + window_len], seq2[j: j + window_len]
            sm = SequenceMatcher(None, s1, s2)
            if quick_seq_sim_ratio(s1, s2):
                return True
    return False

def sequence_similarity(seq1, seq2):
    a = pairwise2.align.globalds(seq1, seq2, blosum62, -10, -0.5, one_alignment_only=True)[0]
    return seq_sim_of_alignment_pair((a[0], a[1]))


def get_unique_sequences(sequences, thresh=0.9):
    unique_seq_ids = []
    unique_seqs = []
    for i, a in enumerate(sequences):
        is_unique = True
        for b in unique_seqs:
            if quick_seq_sim_ratio(a,b, thresh=thresh):
                is_unique = False
        if is_unique:
            unique_seq_ids.append(i)
            unique_seqs.append(a)
    return unique_seq_ids, unique_seqs

def filter_df_by_sim_among_positives(df, thresh, target_var_name='allergen'):
    pos_df = df[df[target_var_name] == 1].reset_index(drop=True)
    neg_df = df[df[target_var_name] == 0].reset_index(drop=True)
    sequences = pos_df['sequence']
    unique_ids = get_unique_sequences(sequences, thresh)
    return df[sequences]
