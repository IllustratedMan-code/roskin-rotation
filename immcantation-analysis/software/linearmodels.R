library(tidyverse)

dfs <- list(
   "hhc" = list(
       "data" = read.csv("/data/RoskinLab/team/david/roskin-rotation/immcantation-analysis/hhc_mut_level.csv"),
        "metadata" = read.csv("/data/RoskinLab/team/david/roskin-rotation/immcantation-analysis/metadata/UTF-8hhc_meta.csv")),
   "chavi" = list(
        "data" = read.csv("/data/RoskinLab/team/david/roskin-rotation/immcantation-analysis/chavi_mut_level.csv"),
        "metadata" = read.csv("/data/RoskinLab/team/david/roskin-rotation/immcantation-analysis/metadata/hiv_negative_meta.csv"))
)

for (i in names(dfs)){
    value = dfs[[i]]
    df = merge(value$metadata, value$data)
    dfs[[i]] = df
}

dfs$chavi$cohort <- "chavi"

dfs$hhc$cohort <- "hhc"

df <- as_tibble(rbind(dfs$chavi, dfs$hhc))

isotype_models <- list()
for (i in unique(df$isotype)){
    
    data = df[df$isotype == i,]
    model = lm(mutation_level.mean.median ~ cohort, data=data)
    isotype_models[[i]] = model
    }




plot <- ggplot(df, aes(x = age, y = mutation_level.mean.median)) +
  geom_point() +
  geom_smooth(method = "lm", method.args = list(), se = FALSE) +
  facet_wrap(~ isotype) +
  labs(title = "Mutation Rate vs Age across groups")


ggsave("linear_regression.png")
