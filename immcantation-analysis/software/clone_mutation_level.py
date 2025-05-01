import sys
import argparse
import logging
import pandas as pd
import numpy as np
from scipy.stats import skew
from glob import glob
from multiprocessing import Pool
import re
from tqdm import tqdm
import os

def percentie100(x):
    return np.max(x)
def percentie90(x):
    return np.percentile(x, 90)
def percentie75(x):
    return np.percentile(x, 75)
def percentie10(x):
    return np.percentile(x, 10)

def percentile(percent):
    def p(x):
        return np.percentile(x, percent)
    p.__name__ = f"percentile{percent}"
    return p


#TODO add clone threshold size.size >= x
    

parser = argparse.ArgumentParser(description='calculate the clone-wise average mutation level per subject',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('mutation_level_filenames', metavar='mut_level.csv', help='files with the mutation level data')


logging.basicConfig(level=logging.INFO)

column_mapping = {
    "subject_id" : "subject",
    "junction_length": "junction_length",
    "mu_freq": "mutation_level",
    "filename": "source",
    "vj_in_frame": "v_j_in_frame",
    "c_call": "isotype",
    "sequence_id": "lineage",
    "sample_id": "sample"
    
}

args = parser.parse_args()


class MutationAggregator():
    allele_regex = re.compile(".*?\*")
    
    def __init__(self, mutation_level_files=args.mutation_level_filenames, column_mapping=column_mapping, parallel=True, remove_alleles=True):
        self.parallel = parallel
        self.column_mapping = column_mapping
        self._mutation_data = None
        self.mutation_data = mutation_level_files
        self.remove_alleles=remove_alleles
        
      
    @property
    def mutation_data(self):
        return self._mutation_data
    
    @mutation_data.setter
    def mutation_data(self, value):
        global read # needed to placate multiprocessing
        def read(v):
            return (pd.read_csv(v, sep="\t", usecols=self.column_mapping.keys()).rename(columns= self.column_mapping))
        if self.parallel:
            process_pool = Pool(os.cpu_count())
            #dfs = process_pool.map(read, value)
            dfs = list(tqdm(process_pool.imap(read, value), total=len(value), desc="Reading files"))
        else:
            dfs =  [ read(v) for v in tqdm(value, desc="Reading files")]
        self._mutation_data = dfs
        
    def aggregate_by_clone(self, data, var):
        if self.remove_alleles:
            def cut_alleles(s):
                s = str(s)
                m = self.allele_regex.match(s)
                if m:
                    s = s[:m.end()-1].strip()
                return s
            data["isotype"] = data["isotype"].apply(cut_alleles)
        data = data.groupby(['subject', 'sample', 'isotype', 'lineage'], dropna=False)
        data = data.aggregate({var: [np.size, np.mean, np.median]})
        return data
    
    def aggregate_by_subject(self, data, var):
        data = self.aggregate_by_clone(data, var)
        data = data.groupby(['subject', 'sample', 'isotype'], dropna=False)
        data = data.aggregate({(var, 'size'):   [np.size, np.mean, np.median, np.sum, percentile(100), percentile(90), percentile(75), percentile(10)],
                           (var, 'mean'):   [np.size, np.mean, np.median, skew,   percentile(100), percentile(90), percentile(75), percentile(10)],
                           (var, 'median'): [np.size, np.mean, np.median, skew,    percentile(100), percentile(90), percentile(75), percentile(10)]})
        
        data.columns = ['.'.join(c) for c in data.columns]
        return data
    
    def aggregate(self):
        global process
        def process(d):
            return pd.concat([self.aggregate_by_subject(d, "mutation_level"), self.aggregate_by_subject(d, "junction_length")])
        if self.parallel:
            process_pool = Pool(os.cpu_count())
            #dfs = process_pool.map(process, self.mutation_data)
            dfs = list(tqdm(process_pool.imap(process, self.mutation_data), total=len(self.mutation_data), desc="Processing Files"))
        else:
            dfs =  [ process(d) for d in tqdm(self.mutation_data, desc="Processing Files")]
        
        return pd.concat(dfs)
    
   
def aggregate_and_save(files):
    ma = MutationAggregator(glob("./software/nextflow/results/repertoire_comparison/repertoires/*.tsv"))
    output = ma.aggregate()

def main():
    mpaach = MutationAggregator(glob("./software/nextflow/results/repertoire_comparison/repertoires/*.tsv"))
    mpaach.aggregate().to_csv("mpaach_mut_level.csv")
    hhc = MutationAggregator(glob("./software/nextflow-hhc/results/repertoire_comparison/repertoires/*.tsv"), parallel=True)
    hhc.aggregate().to_csv("hhc_mut_level.csv")
    chavi = MutationAggregator(glob("/scratch/ros6cc/david/chavi/pipeline_output/results/repertoire_comparison/repertoires/*.tsv"), parallel=True)
    chavi.aggregate().to_csv("chavi_mut_level.csv")

if __name__ == '__main__':
    
    main()
