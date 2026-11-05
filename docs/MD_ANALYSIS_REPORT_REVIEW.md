# MD analysis report — source-based review

**Source:** [sm md.docx](https://docs.google.com/document/d/1t1weETh3QJBb8csODA1BhkFmf0bXMYyz/edit)

**Status:** The original MD analysis Colab notebook was **recovered on 2026-11-05** and [archived](../notebooks/molecular-dynamics/original_md_analysis_colab.ipynb), with a [static source audit](MD_ORIGINAL_NOTEBOOK_AUDIT.md). On the same date an original GROMACS folder with logs, topology and a matching 201-frame protein–ligand trajectory was located. The original report numbers below remain distinct from the **independently recalculated values** at [results/md/README.md](../results/md/README.md).

## Measurements described in the report

| Analysis | Reported result | Verification status |
| --- | --- | --- |
| Production MD | approximately 20 ns | **Verified** from production .mdp, finishing GROMACS log and 0–20 ns 201-frame extracted trajectory |
| Protein backbone RMSD | initial rise followed by plateau | Independently recalculated Cα fit-to-first-frame RMSD; median 5.82 Å (not equivalent to report's 2D RMSD) |
| Ligand RMSD | fluctuating without an irreversible large jump | Requires trajectory, alignment and atom selection |
| 2D RMSD | post-initial values commonly around 1–3 Å | Requires original matrix and settings |
| C-alpha RMSF | usually 1–3 Å, with some 4–6 Å peaks | Requires raw per-residue data |
| Radius of gyration | approximately 20.5–22.5 Å; later approximately 20.7–21.0 Å | Requires raw timeseries |
| Protein–ligand H-bonds | reported zero throughout | **Important:** check selection definitions, donor/acceptor typing, distance and angle thresholds before interpreting absence |
| SASA | approximately 16,500–18,000 Å² | Requires atom selection and algorithm details |
| Protein–ligand COM | often 7–9.5 Å, occasional values around 102–106 Å | **Independently confirmed** raw range 7.43–106.69 Å and minimum-image-corrected range 7.43–9.55 Å |
| Residue contacts | report discusses GLN100, ARG106, ASN138, HSD193, ILE242 and ILE252 | Requires contact cutoffs, definitions and raw trajectory |

## Critical scientific qualifications

1. The report's introduction and methods describe **KRAS protein/inhibitor simulation**, whereas the project source materials identify **LDHB** as a ligand-screening target. Confirm the actual protein in the simulated complex before drawing any disease-mechanism conclusions.
2. A stable protein RMSD or radius of gyration alone does not prove stable **ligand binding**; interpret alongside protein-fitted ligand RMSD, minimum heavy-atom distance, residue contacts and correctly PBC-handled metrics.
3. A flat zero-hydrogen-bond trace could mean absent hydrogen bonding or an analysis configuration problem. It is not sufficient to attribute binding to hydrophobic interactions.
4. The report's proposed explanations for large COM-distance excursions are plausible, **not proven** without checking the raw positions and periodic cell.
5. The raw values, scripts, runtime, thermostat/barostat input settings and plots should be checked independently before publication.

## Recovery plan

- The previous [Colab reference](original private Colab source) is inaccessible, but a recovered [working source notebook](original private Colab source) supplies the original MD analysis implementation. This source has been statically reviewed; it was not rerun.
- GROMACS `.tpr`, `.xtc`, `.mdp` and `.log` were located for the documented 20 ns system. Additional trajectories, complete run inputs, and provenance still require validation.
- A **new independently labeled** Python analysis workflow now exists at [`scripts/analyze_md.py`](../scripts/analyze_md.py); it is not the missing original notebook.
- Protein/ligand RMSD, Cα RMSF, Rg, corrected COM and residue contacts have been recalculated. SASA, hydrogen-bond selection details and complete run validation remain open.

The source report is retained in Google Drive. Its complete text has not been copied here.
