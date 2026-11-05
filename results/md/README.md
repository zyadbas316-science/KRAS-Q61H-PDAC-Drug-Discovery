# Independent MD trajectory reanalysis

This is a **new exploratory calculation** from the original project system, not recovered original MD analysis code. The original `sm md.docx` remains a separate report.

**Source folder:** [GROMACS project files on Google Drive](private source; available to authorized project members)

## Actual source artifacts

- [step5_production.mdp](private source; available to authorized project members): 10,000,000 steps at 0.002 ps = **20 ns**, target 310 K.
- [step5_production.part0009.log](private source; available to authorized project members): GROMACS **2024.4**, reaches approximately **20 ns**, ends with `Finished mdrun`.
- [step5_production_SOLU.tpr](private source; available to authorized project members): extracted protein-ligand topology used for this analysis.
- [all_noPBC.xtc](private source; available to authorized project members): matching extracted 201-frame trajectory, **0–20 ns**.
- [topol.top](private source; available to authorized project members): CHARMM-GUI topology includes protein `PROA` and ligand `UNL` plus ions and TIP3P water.

The original source files remain in Drive. The trajectory/TPR are intentionally **not committed** to GitHub.

## Recalculated metrics

Distances are Å; medians are taken over 201 frames, with 0.1 ns spacing.

| Metric | Median | Observed minimum–maximum |
| --- | ---: | ---: |
| Protein Cα RMSD vs first frame, rigid-body fitted | 5.82 | 0.00–6.44 |
| Ligand heavy-atom RMSD, protein fitted and ligand re-imaged | 3.71 | 0.00–4.72 |
| Protein radius of gyration | 20.87 | 20.53–22.44 |
| Protein–ligand COM distance, raw | 8.62 | 7.43–106.69 |
| Protein–ligand COM distance, PBC minimum image | 8.60 | 7.43–9.55 |
| Closest protein–ligand heavy-atom distance, re-imaged | 3.17 | 2.87–3.43 |
| Protein residues within 4 Å of ligand | 12 | 8–16 |

**Contact occupancy** (fraction of frames with at least one protein heavy atom within 4 Å of a ligand heavy atom): ASN138 **100%**, HSD193 **99.0%**, ILE252 **98.0%**, ARG106 **97.5%**, ASP166 **91.5%**, GLN100 **88.1%**.

The ligand contains **17 carbons and 12 hydrogens** in the analyzed topology; no conventional N/O heteroatom hydrogen-bond donor/acceptor groups are present. This makes a zero count under ordinary protein–ligand hydrogen-bond definitions chemically unsurprising, but hydrogen-bond analysis methods still need to be documented.

## How the numerical check was performed

Using [`scripts/analyze_md.py`](../../scripts/analyze_md.py), with Python, MDAnalysis, NumPy, SciPy and pandas:

```bash
python -m pip install -r requirements-md.txt
python scripts/analyze_md.py \
  --tpr /path/to/step5_production_SOLU.tpr \
  --xtc /path/to/all_noPBC.xtc \
  --output results/md/local-reanalysis
```

The script writes a per-frame CSV, residue RMSF CSV, residue contact occupancy CSV and summary JSON to the specified output directory. These results should be independently rerun, tested and checked against reference selections before journal publication.

## Scientific limitations and next checks

- **No full-solvent resimulation was performed.** The analysis uses a 201-frame extracted solute trajectory.
- The source trajectory named `all_noPBC.xtc` still exhibits **whole-box ligand image shifts** in some frames; our metrics explicitly re-image the ligand using minimum-image protein–ligand COM displacement.
- Protein RMSD relative to the very first frame includes equilibration/relaxation; it is **not directly comparable** to pairwise 2D RMSD or RMSD fitted to a later reference.
- Near-contact distances across these 20 ns support **persistent spatial association** in this run; they do not establish a dissociation free energy, clinical efficacy, or experimental validation.
- The original report incorrectly describes KRAS protein MD in several passages; the project includes the **LDHB** protein complex, so the actual topology and biological interpretation should be reviewed.
- SASA, hydrogen-bond geometry, restraints, MD parameters, RMSF selections, ligand identity and independent replicas still need further review.

Note: links to the shared folder may require owner permission.
