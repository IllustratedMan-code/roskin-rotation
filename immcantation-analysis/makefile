help: ## show this help
	@sed -ne "s/^##\(.*\)/\1/p" $(MAKEFILE_LIST)
	@printf "────────────────────────`tput bold``tput setaf 2` Make Commands `tput sgr0`────────────────────────────────\n"
	@sed -ne "/@sed/!s/\(^[^#?=]*:\).*##\(.*\)/`tput setaf 2``tput bold`\1`tput sgr0`\2/p" $(MAKEFILE_LIST)
	@printf "────────────────────────`tput bold``tput setaf 4` Make Variables `tput sgr0`───────────────────────────────\n"
	@sed -ne "/@sed/!s/\(.*\)?=\(.*\)##\(.*\)/`tput setaf 4``tput bold`\1:`tput setaf 5`\2`tput sgr0`\3/p" $(MAKEFILE_LIST)
	@printf "───────────────────────────────────────────────────────────────────────\n"

.DEFAULT_GOAL := help




data_dir ?= /data ## location of control fasta files

GZ_FILES := $(subst :,\:, $(wildcard data/*/*.gz))
UNZIPPED_FILES := $(patsubst %.gz,%, $(GZ_FILES))

debug: 
	$(info $(UNZIPPED_FILES))


unzip : $(UNZIPPED_FILES) ## Unzips every .fasta.gz file

data/chavi/subject=boydlab:BFI-0003702

%.fasta : %.fasta.gz
	gzip -dk $<


input ?= /data/mpaach_controls/subject=mpaach:MP00508.fasta ## input fasta
db?=/usr/local/share/igblast## igblast db
germ_db ?= /usr/local/share/germlines/imgt/human/vdj
results ?=/software/analysis/results## results directory


assign-genes:   #assigns vdj segments to fasta
	mkdir -p $(results)/igblast
	AssignGenes.py igblast \
		-s $(input) \
		-b $(db) \
		--organism human \
		--loci ig \
		--format blast \
		--outdir $(results)/igblast \
		--nproc 8

standardized-database:
	mkdir -p $(results)/changeo
	MakeDb.py igblast \
		-s $(input) \
		-i $(results)/igblast/subject=mpaach:MP00508_igblast.fmt7 \
		--format airr \
		-r $(germ_db) \
		--outdir $(results)/changeo \
		--outname data

only-productive-heavy-chain:
	ParseDb.py select \
		-d $(results)/changeo/data_db-pass.tsv \
		-f productive -u T --outname data_p

	ParseDb.py select \
		-d $(results)/changeo/data_p_parse-select.tsv \
		-f v_call -u IGHV --regex --outname data_ph


clone_mutation_level:
	module load python3 && python software/clone_mutation_level.py " "


.PHONY := debug help unzip