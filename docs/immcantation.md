## install the container

```bash
make install-immcantation-container-docker
```

## Start the container

```bash
make start-immcantation
```

This will start the container in a bash shell. Directories in the `immcantation-analysis` directory will
be exposed to the container.

## immcantation usage

[usage instructions](https://immcantation.readthedocs.io/en/stable/getting_started/intro-lab.html)

### Inputs

- A fasta containing process reads (input sequence)
- A reference germline database (human and mouse are included in the docker container)

### VDJ gene annotation

- -b = reference germline database
- -s = input sequence

```bash
mkdir -p results/igblast

AssignGenes.py igblast \
    -s /home/magus/data/input.fasta \
    -b /usr/local/share/igblast_test_tigger \
    --organism human \
    --loci ig \
    --format blast \
    --outdir results/igblast \
    --nproc 8

```

### Standardized database file

Takes the results generated from the previous step reformats output to airr.

- -s = original input sequence
- -i = newly generated igblast output

```bash
MakeDb.py igblast \
    -s /home/magus/data/input.fasta \
    -i results/igblast/input_igblast.fmt7 \
    --format airr \
    -r /usr/local/share/germlines/imgt_test_tigger/human/vdj/ \
    --outdir results/changeo \
    --outname data
```

### subset data

```bash

ParseDb.py select \
    -d results/changeo/data_db-pass.tsv \
    -f productive \
    -u T \
    --outname data_p
```
