help: ## show this help
	@sed -ne "s/^##\(.*\)/\1/p" $(MAKEFILE_LIST)
	@printf "────────────────────────`tput bold``tput setaf 2` Make Commands `tput sgr0`────────────────────────────────\n"
	@sed -ne "/@sed/!s/\(^[^#?=]*:\).*##\(.*\)/`tput setaf 2``tput bold`\1`tput sgr0`\2/p" $(MAKEFILE_LIST)
	@printf "────────────────────────`tput bold``tput setaf 4` Make Variables `tput sgr0`───────────────────────────────\n"
	@sed -ne "/@sed/!s/\(.*\)?=\(.*\)##\(.*\)/`tput setaf 4``tput bold`\1:`tput setaf 5`\2`tput sgr0`\3/p" $(MAKEFILE_LIST)
	@printf "───────────────────────────────────────────────────────────────────────\n"

.DEFAULT_GOAL := help

select_control_studies: src/metafetch/select_control_studies.py
	python -m metafetch.select_control_studies

request_data: src/metafetch/request_data.py
	python -m metafetch.request_data

#	docker run -it -v immcantation-analysis/data:/data:z -v immcantation-analysis/scratch:/scratch:z immcantation-analysis/oasis:/oasis:z immcantation-analysis/software:/software:z immcantation/suite:4.5.0 bash
start-immcantation: ## starts immcantation container in new shell
	@mkdir -p $(realpath .)/immcantation-analysis/data
	@mkdir -p $(realpath .)/immcantation-analysis/scratch
	@mkdir -p $(realpath .)/immcantation-analysis/oasis
	@mkdir -p $(realpath .)/immcantation-analysis/software
	docker run -it -v $(realpath .)/immcantation-analysis/data:/data:z \
	               -v $(realpath .)/immcantation-analysis/scratch:/scratch:z \
	               -v $(realpath .)/immcantation-analysis/oasis:/oasis:z \
	               -v $(realpath .)/immcantation-analysis/software:/software:z \
				   immcantation/suite:4.5.0 bash

start-immcantation-singularity: ## starts immcantation container in new shell
	@mkdir -p $(realpath .)/immcantation-analysis/data
	@mkdir -p $(realpath .)/immcantation-analysis/scratch
	@mkdir -p $(realpath .)/immcantation-analysis/oasis
	@mkdir -p $(realpath .)/immcantation-analysis/software
	module load singularity && \
	singularity shell --no-home -c -B $(realpath .)/immcantation-analysis/data:/data,$(realpath .)/immcantation-analysis/scratch:/scratch,$(realpath .)/immcantation-analysis/oasis:/oasis,$(realpath .)/immcantation-analysis/software:/software,$(realpath .)/immcantation-analysis/makefile:/makefile \
				   immcantation_suite-4.5.0.sif
install-immcantation-container-docker: ## installs immcantation docker container
	docker pull immcantation/suite:4.5.0

install-immcantation-container-singularity:
	module load singularity && \
	singularity build immcantation_suite-4.5.0.sif docker://immcantation/suite:4.5.0


.PHONY := help  request_data start-immcantation install-immcantation-container-docker