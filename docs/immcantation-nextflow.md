# outputs
SHM, CDR3

`immcantation-analysis/software/nextflow/results/repertoire_comparison/repertoires` these tables have the SHM(mut_freq) and CDR3 length

Collapse Reads into clones into subjects


# Look into mut_freq

stan (baysian inference)

# Running the pipeline
The airrflow pipeline requires a "samplesheet" containing various metadata about a set of fasta files.

Also, very important note, `process.executor = "lsf"` must go in `nextflow.config` in the directory where the pipeline is run.

I wrote a handy makefile script in each nextflow directory that can start the pipeline.

## Creating the samplesheet
The samplesheet is made using a python script that I wrote called `samplesheetmaker.py`.

# nextflow-hhc

- running the pipeline on hhc fails with the default clonal-threshold setting as the clonal threshold can not be determined for some of the files.
    - This is apparently intentional, which is a bit upsetting, as it might make sense to calculate the clonal threshold for all samples that it can be calculated for.

# Processing the output

`clone_mutation_level.py` handles the results in the `nextflow/results/repertoire_comparison` directory.
