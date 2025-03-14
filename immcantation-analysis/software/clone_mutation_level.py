import sys
import argparse
import logging
import pandas as pd
import numpy as np
from scipy.stats import skew
from glob import glob

def percentie100(x):
    return np.max(x)
def percentie90(x):
    return np.percentile(x, 90)
def percentie75(x):
    return np.percentile(x, 75)
def percentie10(x):
    return np.percentile(x, 10)

parser = argparse.ArgumentParser(description='calculate the clone-wise average mutation level per subject',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('mutation_level_filenames', metavar='mut_level.csv', help='files with the mutation level data')


logging.basicConfig(level=logging.INFO)

column_mapping = {
    "subject_id" : "subject",
    "mu_freq": "mutation_level",
    "filename": "source",
    "vdj_in_frame": "vdj_in_frame"
}

args = parser.parse_args()

class MutationAggregator():
    def __init__(self, mutation_level_files=args.mutation_level_filenames, column_mapping=column_mapping):
        self.column_mapping = column_mapping
        self.mutation_data = mutation_level_files
      
    @property
    def mutation_data(self):
        return self._mutation_data
    
    @mutation_data.setter
    def mutation_data(self, value):
        dfs =  [pd.read_csv(v, usecols=self.column_mapping.keys()).rename(self.column_mapping) for v in value]
        return dfs
        
        
         
    def aggregate_by_clone(self, data):
        data <- data.groupby(['subject', 'sample', 'isotype', 'lineage'], dropna=False)
        data <- data.aggregate({'mutation_level': [np.size, np.mean, np.median]})
        return data
    def aggregate_by_subject(self, data):
        data <- self.aggregate_by_clone(data)
        data <- data.groupby(['subject', 'sample', 'isotype'], dropna=False)
        data <- data.aggregate({('mutation_level', 'size'):   [np.size, np.mean, np.median, np.sum, percentie100, percentie90, percentie75, percentie10],
                           ('mutation_level', 'mean'):   [np.size, np.mean, np.median, skew,   percentie100, percentie90, percentie75, percentie10],
                           ('mutation_level', 'median'): [np.size, np.mean, np.median, skew,   percentie100, percentie90, percentie75, percentie10]})
        return data
    
    def aggregate(self):
        return pd.concat([aggregate_by_subject(d) for d in self.mutation])
def main():
    MutationAggregator(glob("./software/nextflow/results/repertoire_comparison/repertoires/*.tsv"))
        

        

def main2():

    writer = None

    all_data = []

    for filename in args.mutation_level_filenames:
        logging.info('processing file %s', filename)

        data = pd.read_csv(filename,
            dtype={ 'subject': str,
                    'sample': str,
                    'source': str,
                    'isotype': str,
                    'target1': str,
                    'v_segment': str,
                    'lineage': str,
                    'v_j_in_frame': 'boolean',
                    'has_stop_codon': 'boolean',
                    'mutation_level': float})

        # drop the out-of-frame reads and those with stop codons
        data = data[data['v_j_in_frame'] & (~data['has_stop_codon'])]

        # remove alleles from isotype call
        data['isotype'] = data['isotype'].str.split('*').str[0]
        # drop row without isotype
        data_all = data[data['isotype'].notnull()]
        data_all['isotype'] = 'IGHCall'
        # copy out IgAs
        data_iga = data[data['isotype'].isin(['IGHCA1', 'IGHCA2'])].copy()
        # copy out IgGs
        data_igg = data[data['isotype'].isin(['IGHCG1', 'IGHCG2', 'IGHCG3', 'IGHCG4'])].copy()
        # rename "isotypes"
        data_iga['isotype'] = 'IGHCA'
        data_igg['isotype'] = 'IGHCG'
        # add back in
        data = pd.concat([data, data_all, data_iga, data_igg], axis=0)

        clone_data   = data.groupby(['subject', 'sample', 'isotype', 'lineage'], dropna=False).\
                aggregate({'mutation_level': [np.size, np.mean, np.median]})
        subject_data = clone_data.groupby(['subject', 'sample', 'isotype'], dropna=False).\
                aggregate({('mutation_level', 'size'):   [np.size, np.mean, np.median, np.sum, percentie100, percentie90, percentie75, percentie10],
                           ('mutation_level', 'mean'):   [np.size, np.mean, np.median, skew,   percentie100, percentie90, percentie75, percentie10],
                           ('mutation_level', 'median'): [np.size, np.mean, np.median, skew,   percentie100, percentie90, percentie75, percentie10]})

        subject_data.columns = ['.'.join(c) for c in subject_data.columns]

        all_data.append(subject_data)

    pd.concat(all_data).to_csv(sys.stdout, float_format='%.5f')

if __name__ == '__main__':
    
    main()
