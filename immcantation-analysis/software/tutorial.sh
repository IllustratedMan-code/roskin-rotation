mkdir -p results/igblast

AssignGenes.py igblast \
    -s /home/magus/data/input.fasta \
    -b /usr/local/share/igblast_test_tigger \
    --organism human \
    --loci ig \
    --format blast \
    --outdir results/igblast \
    --nproc 8

mkdir -p results/changeo

MakeDb.py igblast \
    -s /home/magus/data/input.fasta \
    -i results/igblast/input_igblast.fmt7 \
    --format airr \
    -r /usr/local/share/germlines/imgt_test_tigger/human/vdj/ \
    --outdir results/changeo \
    --outname data

ParseDb.py select \
    -d results/changeo/data_db-pass.tsv \
    -f productive \
    -u T \
    --outname data_p