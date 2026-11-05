# Reproducibility and scientific release status

## What is reproducible from this repository

Supported: Python 3.11 synthetic smoke tests, exploratory gene-TPM matrix construction given separately downloaded GEO processed TPM files, exploratory group statistics, Vina log parsing and a standalone MD geometric analysis script with appropriate source files.

**Not reproduced end to end:** original RNA-seq alignment/count generation, statistically validated differential expression, target validation, full docking screen or original MD trajectory generation. Original Colab notebooks are archival and have not been certified as runnable.

## Running the smoke tests

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Running exploratory TPM preprocessing

1. Obtain the 12 processed gene-level TPM sample files from GEO [GSE310675](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310675). These are **not raw sequencing FASTQ files**.
2. Store them under `data/raw/` (ignored by Git).
3. Verify `data_manifest/sample_manifest.csv` independently against individual GEO sample metadata.
4. Run:
   ```bash
   python scripts/build_tpm_matrix.py --input-dir data/raw --output-dir results/local --groups-file data_manifest/sample_manifest.csv
   python scripts/exploratory_deg.py --matrix results/local/TPM_matrix.csv --metadata results/local/metadata.csv --output results/local/exploratory_deg.csv
   ```
5. Review QC and sample metadata before interpreting any statistics.

The exploratory Welch tests on log2(TPM+1) are **not count-based differential-expression tests** and do not address cell-line confounding or batch effects. The original **4 Q61H vs 8 other** assignments were wrong. **Do not recycle** their nominal p-values or LDHB statistics as corrected 3-vs-9 results.

## Docking and MD

Docking scores describe a computational scoring model, **not** experimental affinity. The MD work was a 20 ns GROMACS simulation at 310 K; geometric stability metrics cannot alone establish inhibition or binding free energy. Documented artifacts do not establish the exact MD ligand/pose provenance. Check [scientific audit](SCIENTIFIC_AUDIT.md) and [MD results](../results/md/README.md).

## Release boundary

This repository intentionally has a new Git history. Binary pose archive, score workbook, original gene-level processed data, trajectories and checkpoints are **not bundled**. This is an accessible portfolio/research-methods record, **not a complete published manuscript supplement**.

See [PUBLICATION_STATUS.md](PUBLICATION_STATUS.md) for outstanding scientific work.
