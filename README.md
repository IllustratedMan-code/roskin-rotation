## Basic usage

List all available commands

```bash
make help
```

## Methods


### immcantation methods

[detailed instructions here](./docs/immcantation.md)

[more explaination](./immcantation-analysis/README.md)

#### nextflow pipeline
https://nf-co.re/airrflow/4.2.0

### Papers with IGH

##### Fetching Data

This never really went anywhere, but if you are looking for an example of how to interact
with the iReceptor API, maybe this would be useful.

The metafetch python package is stored in `src` and can be used to interact with the Ireceptor airr commons api. I do plan to make it usable as a module.

Metadata was downloaded from ireceptor gateway using the "human" and "IGH" filters.

`ireceptor-number-of-subjects.py` counts the number of subjects for each experiment and sorts them from largest to smallest.

##### Links (data is available on iReceptor)

> Note: These subjects do not have available sequences
> so data is essentially useless (maybe email authors?)
- https://pubmed.ncbi.nlm.nih.gov/35943978/ 95

  - 95 subjects
  - Some are patients treated for covid
  - 43 Sero(-)
  - 20 Sero(+)
  - supplemental table has pdf metadata
  - extract metadata
  - genomic DNA

- https://pubmed.ncbi.nlm.nih.gov/23742949/ 76

  - 13 healthy subjects

- https://pubmed.ncbi.nlm.nih.gov/20161664/ 56
- https://pubmed.ncbi.nlm.nih.gov/32668194/ 35
- https://pubmed.ncbi.nlm.nih.gov/28959265/ 25

