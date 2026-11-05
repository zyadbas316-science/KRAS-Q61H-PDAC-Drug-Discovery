# Critical correction: KRAS genotype grouping

On 2026-11-05, primary GEO metadata was checked against the sample mapping in the original project notebook.

**Error found:** [GSM9306530, Pa14C](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9306530) has **KRAS G12D** in NCBI GEO, but the project's notebook assigns it to **KRAS Q61H**.

Consequences:

- The historical 4-vs-8 comparison was performed with at least one incorrectly grouped cell line.
- Previously reported statistical summaries, including the 0-significant-gene exploratory result, **do not constitute a corrected group comparison**.
- The original notebooks remain archived to document what was done, not to endorse the original groups.
- A corrected differential-expression run should wait until each of the 12 sample genotypes is checked against primary GEO metadata.
- `scripts/build_tpm_matrix.py` now writes `UNVERIFIED` group labels by default and accepts explicit verified group assignments from a CSV with columns `accession,group` using `--groups-file`.

Other issues are documented in [SCIENTIFIC_AUDIT.md](SCIENTIFIC_AUDIT.md).

## Verified NCBI GEO sample records (checked against primary source)

| Accession | Cell line | KRAS genotype | Verified group | Primary record |
| --- | --- | --- | --- | --- |
| GSM9306530 | Pa14C | G12D | Non_Q61H | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9306530 |
| GSM9306533 | T3M4 | Q61H | KRAS_Q61H | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9306533 |

**Do not run a corrected full comparison based on this partial table.** Validate the other ten source sample records before generating a complete genotype manifest and rerunning the analysis. The original 4-versus-8 results are historical only.
