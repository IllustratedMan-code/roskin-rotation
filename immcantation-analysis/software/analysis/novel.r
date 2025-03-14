suppressPackageStartupMessages(library(airr))
suppressPackageStartupMessages(library(alakazam))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(tigger))

results <- file.path("software", "analysis", "results")
dir.create(file.path(results, "tigger"))


db <- read_rearrangement(file.path(results, "changeo",
                                   "data_ph_parse-select.tsv"))


ighv <- readIgFasta(file.path("", "usr", "local", "share", "germlines",
                              "imgt", "human", "vdj",
                              "imgt_human_IGHV.fasta"))


nv <- findNovelAlleles(db, germline_db = ighv, nproc = 8) # find novel alleles

selectNovel(nv) # show novel alleles

png(file.path(results, "tigger", "novel.png"))
plotNovel(db, selectNovel(nv)[1, ]) # visualize the novel allele(s)
dev.off()