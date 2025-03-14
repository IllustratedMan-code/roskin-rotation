from glob import glob
import pandas as pd
import re

# TODO need to fix the absolute pathing or move it to the makefile
files = glob("/data/RoskinLab/team/david/roskin-rotation/immcantation-analysis/data/hhc/*.fasta")

entries = dict(filename=[],species=[], subject_id=[], sample_id=[], tissue=[], sex=[], age=[], biomaterial_provider=[], pcr_target_locus=[], single_cell=[])

defaults = dict(species="human", tissue="NA", sex="NA", age=99, biomaterial_provider="NA", pcr_target_locus="IG", single_cell="FALSE")

subject_id_regex = re.compile(".*subject=.*:(.*).fasta")


def make_fields_from_filename(filename):
    
    subject_id = subject_id_regex.match(filename)[1]
    return {"filename":filename, "subject_id":subject_id, "sample_id":subject_id}
    

for f in files:
    for k,v in defaults.items():
        entries[k].append(v)
    for k,v in make_fields_from_filename(f).items():
         entries[k].append(v)
df = pd.DataFrame(entries) 

df.to_csv("samplesheet.tsv", sep="\t", index=False)