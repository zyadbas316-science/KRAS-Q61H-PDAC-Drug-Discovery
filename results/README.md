# Reproduced checks and results status

## TPM data quality check

Using 12 original compressed GEO GSE310675 gene-level TPM files:

- Samples: **12** (GSM9306522–GSM9306533)
- Common genes: **35,654**
- Missing entries in merged matrix: **0**
- Duplicate gene names in the individual inputs: **0**
- TPM sums per sample: approximately **1,000,000**

These checks concern input consistency only; they do not prove valid biological group comparisons.

## Statistical analysis status

**Withheld pending corrected genotype mapping.** The source project's 4-vs-8 KRAS grouping labels Pa14C as Q61H; the official NCBI record labels Pa14C G12D. Therefore the historical exploratory Welch-test results in the audit are not valid for a corrected Q61H-versus-comparison conclusion.

See [Genotype correction](../docs/GENOTYPE_CORRECTION.md) and [Scientific audit](../docs/SCIENTIFIC_AUDIT.md). No adjusted-significant genes, selected drug targets, or mechanistic conclusions are asserted from a corrected analysis at this time.

## Reproduction

Run `scripts/build_tpm_matrix.py` against the downloaded sample TPM files. Unless a separately verified `--groups-file` is supplied, the metadata output intentionally labels all samples `UNVERIFIED`. The required raw files and corrected full group manifest are not bundled here.
