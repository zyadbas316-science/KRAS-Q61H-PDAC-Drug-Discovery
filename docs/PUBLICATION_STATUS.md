# Publication and evidence status

**Release type:** Public-facing, clean-history computational research portfolio.

**Scientific status:** **Exploratory / not validated**. Public availability does not imply peer review, biochemical inhibition, corrected DEG validation, comprehensive notebook execution, or a completed Q1 manuscript.

### Completed or available
- Source dataset identified (GSE310675); corrected paper-derived KRAS Figure 2 manifest (three Q61H / nine others).
- Core Python source and synthetic unit tests; GitHub Actions workflow.
- Archived curated notebooks; structural records, subset of docking scores, MD inputs and documented geometric reanalysis.
- MIT software license with third-party exclusions and citation metadata.
- New repository without historical Git commits or original private Colab links.

### Further work required for scientific publication
- Independently verify GEO per-sample mutation/genotype and experimental design; acquire suitable counts / replicates for statistical inference.
- Re-run corrected differential-expression and enrichment with defensible controls, thresholds and multiple-testing adjustment.
- Validate LDHB prioritization against independent datasets and biological knowledge.
- Reconstruct screened ligand identifiers, chemical structures, receptor state, docking poses and controls.
- Reproduce and verify MD parameters, ligand topology/identity and trajectories; quantify uncertainty and replicate where justified.
- Credit actual contributors and source datasets precisely; validate scientific figures before inclusion in a manuscript.

### Not distributed in this first release
- Unreviewed binary `results/docking/docked_poses.tgz` and `original_score_workbook.xlsx`.
- Full input datasets, trajectories, checkpoint files and other large simulation outputs.
- Previously linked private collaborative Drive/Colab file identifiers.

**Security note:** The old repository remains private. This new repository uses a fresh Git history and is curated from the current files. The documented pattern checks are not equivalent to a professional penetration test or exhaustive provenance audit.
