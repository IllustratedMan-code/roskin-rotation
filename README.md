## Basic usage

List all available commands

```bash
make help
```

## methods

The metafetch python package is stored in `src` and can be used to interact with the Ireceptor airr commons api. I do plan to make it usable as a module.

Metadata was downloaded from ireceptor gateway using the "human" and "IGH" filters.

`ireceptor-number-of-subjects.py` counts the number of subjects for each experiment and sorts them from largest to smallest.

## immcantation methods

[detailed instructions here](./docs/immcantation.md)

Current method for using the immcantation is to use the docker container. I plan on making a functional flake for it as well, but may need to examine the docker image to get full dependency list.

The dockerfile itself isn't very helpful. I think they construct it manually? Very weird.

## Links to papers with IGH

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
