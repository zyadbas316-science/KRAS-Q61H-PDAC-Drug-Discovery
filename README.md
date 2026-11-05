# KRAS Q61H in Pancreatic Cancer (PDAC): Transcriptomics, LDHB Prioritization, Docking & Molecular Dynamics

**Computational oncology · Bioinformatics · Structure-based drug discovery · Reproducible research**

An openly documented research portfolio investigating the **KRAS Q61H** subgroup of **pancreatic ductal adenocarcinoma (PDAC)** through exploratory RNA-expression analysis, candidate **LDHB** prioritization, ligand screening, molecular docking and molecular dynamics (MD).

> **Research status:** This is an **exploratory, curated research archive**, **not** a validated drug-discovery or end-to-end reproducible therapeutic pipeline. The historical differential-expression group labels contain errors. No corrected, validated differential-expression findings or biochemical inhibition claims are presented.

## Scientific question

Can RNA-expression patterns across pancreatic cancer cell lines carrying KRAS Q61H inform a testable candidate-target hypothesis, and how can structure-based computational methods evaluate preliminary ligand interactions with that candidate?

The workflow is documented as a research history, **not** as evidence that LDHB is a specific KRAS Q61H dependency or that any screened compound is an effective inhibitor.

## Data and KRAS genotype audit

The underlying expression dataset is **NCBI GEO [GSE310675](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310675)**. The archived analysis uses **12 processed gene-level TPM sample files**, *not raw sequencing FASTQ/count data*. The source-paper Figure 2 assignments indicate **three Q61H cell lines (Hs766T, Pa02C, T3M4)** and **nine non-Q61H lines**. Independent verification of individual GEO sample metadata remains an open step.

**Important correction:** Historical source notebooks erroneously analyzed a **4-vs-8** grouping. Its reported p-values and LDHB statistics are **not valid corrected-group results**. They must not be quoted as evidence for a Q61H-specific target. See [genotype figure audit](docs/GENOTYPE_FIGURE2_AUDIT.md) and [scientific audit](docs/SCIENTIFIC_AUDIT.md).

## Research workflow and repository contents

| Stage | Location | Evidence status |
| --- | --- | --- |
| Sample mapping and metadata | [data_manifest/](data_manifest/) | Paper-derived 3-vs-9 mapping; GEO records still to be independently checked |
| Gene-level TPM preprocessing | [scripts/build_tpm_matrix.py](scripts/build_tpm_matrix.py) | Synthetic tests; requires original GEO processed files |
| Exploratory statistics | [scripts/exploratory_deg.py](scripts/exploratory_deg.py) | Welch tests on TPM, **not** validated count-based DEG |
| Archived transcriptomics, enrichment and screening notebooks | [notebooks/](notebooks/) | Preserved for historical transparency; not certified to execute |
| Docking with AutoDock Vina | [notebooks/docking/](notebooks/docking/) and [results/docking/](results/docking/) | Archived scores; **not** experimental binding affinity |
| 20 ns GROMACS MD and structural checks | [inputs/md/](inputs/md/), [scripts/analyze_md.py](scripts/analyze_md.py), [results/md/](results/md/) | Reanalysis documented; neither free-energy proof nor inhibitor validation |
| Limitations and reproducibility | [docs/](docs/) | Scope, genotype correction, source limitations and rerun instructions |
| Automated synthetic smoke tests | [tests/](tests/) | Checks core Python scripts, not full study reproducibility |

The **LDHB** structural work used **PDB 7DBJ** and exploratory ligand collection/docking. Available processed geometry and docking artifacts are research records; ligand provenance and its relationship to the MD system require further verification. The 20 ns simulation at 310 K is not sufficient to establish binding thermodynamics or therapeutic activity.

## Run the supported Python checks

Requires **Python 3.11**.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

To reproduce the TPM preprocessing, download the **12 GSE310675 gene-level TPM files** separately into `data/raw/` and run:

```bash
python scripts/build_tpm_matrix.py --input-dir data/raw --output-dir results/local --groups-file data_manifest/sample_manifest.csv
```

**Check the individual GEO sample annotations before statistical interpretation.** Without an explicit mapping, the preprocessing script leaves sample group assignments as `UNVERIFIED`. An optional exploratory comparison is documented in [reproducibility instructions](docs/REPRODUCIBILITY_AND_RELEASE.md). It does not replace a count-based design with suitable controls.

## What is included and excluded

This clean repository was assembled from the **current curated files** with a **fresh Git history**, instead of cloning the old collaborative development history.

Included: analysis scripts, tests, six archival notebooks with stripped execution outputs, genotype manifest, method/audit notes, selected structure files, documented Vina scores, GROMACS MDP inputs and MD analysis summary.

Not included: original raw datasets or trajectory/checkpoint files, and the historical `docked_poses.tgz` archive or `original_score_workbook.xlsx` (binary archive review pending). Some source datasets and prior project links are intentionally not exposed. See [publication status](docs/PUBLICATION_STATUS.md) for remaining scientific and reproducibility work.

## Citation and source credit

- **Expression data:** [NCBI GEO GSE310675](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310675).
- **Underlying study:** Long et al. (2026), *CRISPR-Cas9 Screening Identifies Resistance Mechanisms to KRAS Inhibition in Pancreatic Cancer*, *Cancer Research*. [DOI: 10.1158/0008-5472.CAN-25-1835](https://doi.org/10.1158/0008-5472.CAN-25-1835).
- **Structure:** [RCSB PDB 7DBJ](https://www.rcsb.org/structure/7DBJ).
- See [CITATION.cff](CITATION.cff) for citing this code archive. Cite upstream papers, databases and software for their respective contributions.

## License and responsible use

**MIT License** applies to original software and documentation for which the maintainer holds licensing rights. **Upstream datasets, PDB/ZINC records, third-party software and independently owned content are not automatically covered**; see [third-party notices](THIRD_PARTY_NOTICES.md). This repository is for research and education, not clinical decision-making.

Maintained by [zyadbas316-science](https://github.com/zyadbas316-science).
