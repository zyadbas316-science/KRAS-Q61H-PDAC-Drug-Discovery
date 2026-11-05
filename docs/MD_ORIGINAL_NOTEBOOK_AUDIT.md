# Original MD analysis Colab — static audit

**Recovered source:** [ZS of MD_analysis_biotech_4th.ipynb](private source; available to authorized project members) in the linked [Colab Notebooks folder](private source; available to authorized project members).

**Curated copy:** [original_md_analysis_colab.ipynb](../notebooks/molecular-dynamics/original_md_analysis_colab.ipynb).

On 2026-11-05, this source contained **67 cells: 43 code cells, 24 markdown cells** and 41 saved code-cell outputs. For repository hygiene, the cached outputs and execution metadata were removed; the original code order and source were preserved. The notebook was **not executed** during this static audit, and it is **not** the same as the independently implemented `scripts/analyze_md.py`.

## Original analysis workflow

1. Colab package setup: MDAnalysis, mdakit-sasa, Plotly, RDKit, ProLIF.
2. GROMACS energy plots for minimization, NVT temperature and NPT pressure.
3. `gmx trjcat`, `gmx convert-tpr` and `gmx trjconv` to create extracted solute trajectory/topology.
4. 1D backbone and ligand RMSD; 2D RMSD distance matrix; C-alpha RMSF.
5. Protein–ligand hydrogen-bond counts, SASA, radius of gyration.
6. Protein–ligand geometric separation and ProLIF fingerprint/interaction plots.
7. Plot export to SVG/HTML/TIFF, and compressed archive creation.

The matching original GROMACS inputs and an extracted 201-frame, 0–20 ns system were independently located in the [project GROMACS folder](private source; available to authorized project members).

## Critical review findings

- **Reproducibility:** `DIR_sys1`, `DIR_sys2` and shell commands hardcode Colab `/content/drive/MyDrive/gromacs` and a separate GROMACS binary path; the notebook cannot be assumed portable.
- **PBC artifacts:** The cell headed "center of mass (COM)" actually calls `center_of_geometry()` for protein and ligand, subtracts the coordinates and takes a norm. It neither computes mass-weighted COM nor uses a periodic minimum-image distance. For this system, occasional raw separations above 100 Å were independently shown to be imaging artifacts; see [independent reanalysis](../results/md/README.md).
- **H-bonds:** The original algorithm selects donors/acceptors with atom-name patterns `S*/N*/O*/F*`, hydrogens `H*`, a 3 Å cutoff and 160-degree angle threshold. Validate chemical element/atom typing and the selection definitions. In this run the extracted ligand topology was found to contain C and H only; a zero conventional protein–ligand hydrogen-bond trace would not by itself show a computational failure.
- **Time axis:** Several plots convert frame number to ns by dividing by ten or constructing an assumed 0.1 ns grid. Instead use actual `trajectory.ts.time`; fixed expressions will silently mislabel other trajectories.
- **RMSD reference:** The notebook aligns to its first frame and also includes ligand RMSD in the same workflow; check PBC reconstruction, atom selections and reference fitting before interpreting ligand retention.
- **Frame selection:** ProLIF uses `end_frame = 200` and `trajectory[:200]`. With 201 frames, that excludes the last frame. Record this explicitly in any occupancy claims.
- **SASA and package versions:** SASA uses `SASAAnalysis(...).run(stop=500)` despite a 201-frame input; the effective range needs verification. Several Colab package installations use moving latest versions, so dependencies are not pinned for reproducibility.
- **Safety:** The original archive cell contains a commented-out `rm` cleanup command. Leave it disabled. Review shell commands and Drive mount destinations before running.

## Project separation

This linked folder also contains **other, separate computational projects** (for example, maize BiP2/BiP3 structural plots). Do not automatically merge those data or notebooks into the PDAC/LDHB Biocoders repository.

## Source dataset caution

The [GSE310675_TPM folder](private source; available to authorized project members) contains an older `metadata.csv` that labels **GSM9306530 / Pa14C** as `KRAS_Q61H`. Its [primary NCBI GEO record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM9306530) reports **KRAS G12D** instead. The older grouped DEG CSVs must not be treated as corrected results without rebuilding the genotype manifest.

## Next reproducibility steps

1. Keep the archival Colab for provenance; use an independently reviewed script for corrected PBC-aware calculations.
2. Add versioned environment and input manifests, and test the PBC correction for the matching extracted TPR/XTC.
3. Compare independent plots and per-frame values against original SVG and XVG outputs, documenting differences.
4. Recalculate binding contact occupancies and SASA with validated atom selections, then review conclusions before CV/public release.
