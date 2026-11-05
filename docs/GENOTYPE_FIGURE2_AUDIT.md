# KRAS genotype and grouping correction

**Primary source:** Long et al., *Cancer Research* (2026), DOI: 10.1158/0008-5472.CAN-25-1835, **Figure 2A (PDF page 7)**. GEO series: [GSE310675](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310675).

The source paper labels all 12 PDAC cell lines with KRAS variants. Its Q61H comparison consists of **3 Q61H cell lines and 9 non-Q61H cell lines**, not the archived 4-vs-8 grouping.

| Q61H | Non-Q61H |
|---|---|
| Hs766T, Pa02C, T3M4 | AsPC-1, HPAC, HuP-T3, MIA PaCa-2, Pa01C, Pa04C, Pa14C, Pa16C, PANC-1 |

**Specific errors in archived project metadata:** Pa14C (G12D) was labeled Q61H; Pa02C (Q61H) was labeled non-Q61H; HuP-T3 (G12R) was labeled Q61H. This changes group membership and invalidates using the historical results as a correctly grouped comparison.

Machine-readable source mapping: [sample_manifest.csv](../data_manifest/sample_manifest.csv). This table is transcribed from the **paper figure**, not an independent sequencing-based mutation call. Individual GEO sample metadata and the consistency of sample identifiers with expression columns still require checking.

## Interpretation safeguards

- The 12 GEO supplementary gene-expression files are **TPM**, not integer gene counts.
- The paper's RNA-seq methods describe Kallisto quantification in counts and TPM; public availability of the original count files is **not established**.
- A single GEO sample per cell line does not prove the absence of biological replication in the broader study. Determine the RNA-seq design separately.
- Historical TPM-derived DEG and enrichment outputs are archived for provenance, not endorsed as statistically validated findings.
- The source paper reports KRAS inhibitor resistance biology; LDHB docking and MD do **not** establish an LDHB inhibitor or drug efficacy.
- A corrected exploratory expression comparison must explicitly account for sample independence, confounding and multiple testing.

## Portfolio versus publication

**Portfolio:** Show documented data provenance, transparent corrections, reproducible scripts, quality control, docking/MD methodology and limitations.

**Publication:** Requires a distinct question, verified design, appropriate statistical inference, independent validation and defensible molecular evidence.

This document is a source correction, not a completed reanalysis.
