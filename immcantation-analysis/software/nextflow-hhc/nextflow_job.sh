BSUB -W 60:00
#BSUB -n 4
#BSUB -M 16000
#BSUB -R "span[hosts=1]"
#BSUB -e ~/%J.err
#BSUB -o ~/%J.out


# execute program
make resume_nextflow