help: ## show this help
	@sed -ne "s/^##\(.*\)/\1/p" $(MAKEFILE_LIST)
	@printf "────────────────────────`tput bold``tput setaf 2` Make Commands `tput sgr0`────────────────────────────────\n"
	@sed -ne "/@sed/!s/\(^[^#?=]*:\).*##\(.*\)/`tput setaf 2``tput bold`\1`tput sgr0`\2/p" $(MAKEFILE_LIST)
	@printf "────────────────────────`tput bold``tput setaf 4` Make Variables `tput sgr0`───────────────────────────────\n"
	@sed -ne "/@sed/!s/\(.*\)?=\(.*\)##\(.*\)/`tput setaf 4``tput bold`\1:`tput setaf 5`\2`tput sgr0`\3/p" $(MAKEFILE_LIST)
	@printf "───────────────────────────────────────────────────────────────────────\n"

.DEFAULT_GOAL := help

start-nextflow:
	source /etc/bashrc && \
	proxy_on && \
	module load singularity && \
	module load nextflow && \
	nextflow run nf-core/airrflow \
	-r 4.2.0 \
	-profile singularity \
	--input samplesheet.tsv \
	--mode assembled \
	--outdir results

resume-nextflow:
	source /etc/bashrc && \
	proxy_on && \
	module load singularity && \
	module load nextflow && \
	nextflow run nf-core/airrflow \
	-r 4.2.0 \
	-resume \
	-c nextflow.config \
	-profile singularity \
	--input samplesheet.tsv \
	--mode assembled \
	--outdir results \

pull-airrflow:
	source /etc/bashrc && \
	proxy_on && \
	module load singularity && \
	module load nextflow && \
	nextflow pull nf-core/airrflow \
	-r 4.2.0

samplesheet.tsv: samplesheet.csv
	sed -E 's/("([^"]*)")?,/\2\t/g' $< > samplesheet.tsv
