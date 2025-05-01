# Software to remove duplicate keys from fasta files.

from glob import glob
from Bio import SeqIO
import os
from pathlib import Path
import pandas as pd
from numba import jit

def remove_duplicate_keys(input_file, output_file):
	count_records = {}
	input_file = open(input_file, "r")
	output_file = open(output_file, "w")
	while True:
		key = input_file.readline().strip()
		value = input_file.readline().strip()
		if key not in count_records:
			output_file.write(f"{key}\n{value}\n")
			count_records[key] = 1
	else:
		count_records[key] += 1
	input_file.close()
	output_file.close()
	return pd.DataFrame.from_dict(count_records, orient="index", columns=["duplicate_count"])


def remove_and_summarize(input_dir, output_dir, summary_file):
	input_fasta = glob(os.path.join(input_dir, "*.fasta"))
	output_fasta = [os.path.join(output_dir, Path(i).name) for i in input_fasta]
	print(input_fasta)
	dup_counts = {}
	for input_file, output_file in zip(input_fasta, output_fasta):
		name = Path(input_file).name
		print(name)
		dup_counts[name] = remove_duplicate_keys(input_file, output_file)
	
	summary = {"file":[], "total_duplicates":[], "unique_duplicate_counts":[]}
	print(dup_counts)
	for k,v in dup_counts.items():
		summary["file"].append(k)
		summary["total_duplicates"].append(v["duplicate_count"].sum())
		summary["unique_duplicate_counts"].append(v["unique_duplicate_counts"])
	summary = pd.DataFrame(summary)
	with pd.ExcelWriter(summary_file) as writer:
		summary.to_excel(writer, sheet_name="summary")
		for k,v in dup_counts.items():
			v.to_excel(writer, sheet_name=k)
		

if __name__ == "__main__":
	remove_and_summarize("test_remove_dups", "test_remove_dups_out", "dups_summary.xlsx")


		

