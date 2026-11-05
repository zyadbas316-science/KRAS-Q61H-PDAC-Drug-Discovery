# Scientific and reproducibility audit

**Status:** static code review plus an independent exploratory recalculation. Not peer-reviewed or experimentally validated.

> **CORRECTION (2026-11-06):** The historical 4-vs-8 genotype grouping documented below is **incorrect**. Source-paper Figure 2A supports 3 Q61H (Hs766T, Pa02C, T3M4) versus 9 non-Q61H. All historical DEG counts, p-values and LDHB statistics in this section describe the **invalid historical grouping** only; they are **not corrected findings**. See [genotype audit](GENOTYPE_FIGURE2_AUDIT.md) and [manifest](../data_manifest/sample_manifest.csv).

## Materials examined

- Original project notebooks: transcriptomics, ligand collection, enrichment, and GROMACS execution.
- 12 original GEO-derived compressed gene-level TPM files for GSE310675.
- Project reports for transcriptomics, docking, and MD.
- Docking score spreadsheet (508 rows), protein–ligand coordinates (PDB and MOL2).

The source project was collaborative. Original notebooks are preserved in curated form, with stored outputs and unnecessary metadata removed. The GitHub commit attribution identifies the curator, not necessarily the sole author of every cell.

## Reproduced data checks

| Check | Result |
| --- | --- |
| GEO series | GSE310675 |
| Samples | 12, GSM9306522 through GSM9306533 |
| Common genes | 35,654 |
| Missing entries | 0 |
| Duplicated gene names in input | 0 |
| TPM sum per sample | Approximately 1,000,000 |
| Grouping **used by source notebook** | KRAS Q61H: Hs766T, HuPT3, Pa14C, T3M4; other 8 lines as comparison |

**Historical, incorrectly grouped exploratory calculation (retained solely for audit):** Welch two-sided t-test across cell lines on log2(TPM+1) expression, with Benjamini–Hochberg correction across 35,654 genes.

- Genes with unadjusted p < 0.05: **963**.
- Genes with BH-adjusted p < 0.05: **0**.
- Minimum BH-adjusted p-value: approximately **0.6775**.
- Example **LDHB**: difference between group mean log2(TPM+1) = **+5.2669**, unadjusted p = **0.01584**, BH-adjusted p = **1.0**.

The notebook labels group-mean log2(TPM+1) differences as `logFC`; that is **not equivalent** to log2 of the ratio of raw group-mean TPM. Do not describe these measurements as validated fold changes without defining the estimand.

### Interpretation

No gene was significant after multiple-testing correction under this **incorrectly grouped historical** exploratory test. This does not establish the result of a corrected analysis. The selected target LDHB is a **hypothesis-generating candidate**, not a statistically confirmed differential-expression hit. A cell-line comparison with four vs eight biologically distinct lines is vulnerable to confounding; TPM-based t-tests are not a substitute for an appropriately designed count-based differential-expression analysis with valid replicates.

## Notebook review

### Transcriptomics

- Several cells hardcode Colab Drive paths.
- A custom “limma-like” moderated t-test fixes prior degrees of freedom to five and uses the median variance; **this is not validated equivalent to limma's empirical Bayes procedure**.
- A second Welch t-test implementation is present; top-five candidates are selected by effect size in some cells without requiring FDR significance.
- A code cell contains R statements in a Python notebook without a clear R cell magic.
- Original notebooks should be treated as educational/archival analysis until rerun from a clean environment.

### Enrichment

- The notebook uses hard-coded lists of five “up” and five “down” genes rather than a programmatically generated, FDR-filtered list.
- Result interpretation should be labeled exploratory, and external gene-set library versions must be rechecked.

### Ligand screening and docking

- Ligand notebook retrieves SDF files by ZINC identifiers, but the input ID list and exact selection criteria are external.
- The original pose archive contains **7,376 files**, including **508 AutoDock Vina logs**. The logs represent **135 unique ZINC identifiers** and **508 conformer runs**.
- **504** logs report nine scored poses; **four** report none. All 508 logs identify **AutoDock Vina 1.2.7**, Vina scoring, grid center **(0.238, −11.634, −15.294)**, box dimensions **30 × 30 × 30 Å**, and **exhaustiveness = 4**.
- Lowest score among reported top modes: **−9.248 kcal/mol**, corresponding to **ZINC000002039299_conf1-1**. This is a scoring-function output, not an experimental binding affinity.
- The 508-row spreadsheet has no header row. Its eight numeric columns were compared against the **first eight docking modes** parsed from the original logs: **4,032 numeric cells matched exactly**, with four fully empty score rows corresponding to failed/no-score logs. The ninth mode was missing from the original workbook and is included in the newly parsed CSV.
- Original raw logs and poses are archived under `results/docking/`. The docking **notebook** was recovered and archived in `notebooks/docking/`; independent redocking and controls remain unconfirmed.

### Molecular dynamics

- The **original 67-cell MD analysis notebook** was recovered from [Colab](private source; available to authorized project members) and archived in `notebooks/molecular-dynamics/original_md_analysis_colab.ipynb`. See [static notebook audit](MD_ORIGINAL_NOTEBOOK_AUDIT.md). It uses `center_of_geometry()` for the plot labeled COM, without a periodic minimum-image correction.
- Production MDP, finishing GROMACS log, matching protein–ligand TPR and an extracted XTC were subsequently found. They establish **20 ns**, **310 K** and a 201-frame extract; see [independent MD reanalysis](../results/md/README.md). Complete reproducibility and trajectory-quality review still require work.
- The notebook references GROMACS **2024.4**.
- Equilibration commands use `/content/drive/MyDrive/GROMACS_BIOCODERS/gromacs` while production commands use `/content/drive/MyDrive/computer_vision/gromacs`: likely broken or inconsistent path.
- The workflow deletes `*.trr` files, which may remove information needed for reanalysis.
- It uses `-maxwarn 1` during equilibration preprocessing; warnings should be inspected and resolved rather than ignored.
- The supplied complex uses `ATOM` records for an `UNL` ligand in chain X (17 ligand heavy atoms); verify residue classification and parameterization before MD. A separate MOL2 includes additional hydrogens.

## Structure provenance

The project notes identify PDB **7DBJ**. The official RCSB record describes a human **LDHB** crystal structure at **1.55 Å**, in complex with NADH, oxamate and AXKO-0046. The biological assembly is a tetramer. Any use of an isolated chain or altered ligand environment requires an explicit modeling justification.

Source: https://www.rcsb.org/structure/7DBJ

## Before publishing as a complete reproducible portfolio project

- Cross-check all paper-derived genotype labels against individual GEO sample records, then rerun with the corrected 3-versus-9 grouping; never reuse historical 4-versus-8 p-values.
- Obtain count-level data and appropriate biological replicate information if inferential DEG claims are intended.
- Preserve input manifests and software versions; make all notebook paths configurable.
- Validate the now-recovered original docking notebook, receptor preparation and binding-site model. Raw logs and their score columns have been checked against the archived spreadsheet.
- Full-system GROMACS files and a 20 ns extracted trajectory are now available. Compare the recovered original analysis with the independently implemented, PBC-aware reanalysis and check full reproducibility.
- Review acknowledgments, authorship and redistribution permissions with the collaborators.
- Do not infer experimental therapeutic efficacy from docking or MD outputs.

## 2026-11-05 GROMACS recovery and independent trajectory check

A [GROMACS Drive folder](private source; available to authorized project members) contains actual 2024.4 production logs, .mdp, topology and solute-only .tpr/.xtc for the reported run. Our independent [reanalysis](../results/md/README.md) sampled 201 frames from 0–20 ns and found PBC-corrected protein–ligand COM distances of 7.43–9.55 Å and minimum heavy-atom distances of 2.87–3.43 Å. This establishes continued proximity over the analyzed frames, not binding thermodynamics. The ligand in this topology has 17 C and 12 H atoms, consistent with no conventional heteroatom-mediated protein–ligand hydrogen bonding.
