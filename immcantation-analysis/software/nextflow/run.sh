module load singularity && \
module load nextflow && \
nextflow run nf-core/airrflow \
-profile singularity \
--input samplesheet.tsv \
--mode assembled \
--outdir results