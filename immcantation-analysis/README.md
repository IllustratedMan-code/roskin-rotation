# Analysis using the Immcantation framework

This directory houses analysis/scripts that utilize the immcantation framework.


> Some caveats
> This project is not particularly well organized, but
> I did try to run most things through the makefile at the
> root of this directory.

I had explored the docker container given by the immcantation framework, but settled
on using the airrflow nextflow pipeline (written by the same authors). 


Most things are housed in the `software` directory. 

## Important scripts (in software)

- `linearmodels.py` is used to determine the effect of age on mutation level (no make target)
- `clone_mutation_level.py` Aggregates mutation level, junction length (make target)
- `plot_mutation_level.py` Plots stuff from `clone_mutation_level.py` (make target)

### Nextflow Runs

There are three nextflow pipeline outputs that are used (located in `software`):

- `nextflow` This is the mpaach data
- `nextflow-hhc` This is the healthy human control data
- `nextflow-chavi` This is the HIV control data

### Metadata

The `metadata` folder contains age metadata for the three cohorts



### Important note about Nextflow
If you are in this directory trying to learn how I used the nextflow pipeline,
make sure to take a look at the `nextflow.config ` and `makefile` in each of the nextflow directories.
