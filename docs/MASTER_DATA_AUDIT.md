# Biocoders Master Data Audit — v0.1

**Scope:** PDAC / KRAS mutation / LDHB target / virtual screening / GROMACS molecular dynamics. **Audit date:** 2026-11-06. **State:** discovery and provenance audit, **not** full independent validation or a claim of publication readiness.

## Objective and distinct deliverables

| Track | Deliverable | Acceptance criterion |
|---|---|---|
| Scientific publication | Corrected analysis, figures, methods, supplementary materials, defensible interpretation | Every numerical result traced to an input, exact software/version, analysis method and parameter set; statistical assumptions checked; genotype and chemical identity validated; novelty assessed independently |
| Reproducible GitHub | Clean, documented, runnable analysis repository | Separate source data and derived results; versioned scripts/environments; one-command or documented workflow; test on a clean environment; no secrets, giant trajectory binaries or ambiguous licensing |
| CV / portfolio | Concise project description, methods and contributions | Claims limited to verified work; distinguish original contributions from team work; links point to maintained repo; no unsubstantiated inhibitor/therapeutic efficacy claims |

## Inventory — verified Google Drive locations (direct children only)

| ID | Drive folder | Direct entries observed | Key artifacts and status |
|---|---|---:|---|
| SRC-01 | [Biocoders root](private source; available to authorized project members) | 2 folders | `Material` and `What we did`; nested directories separately inventoried |
| SRC-02 | [What we did](private source; available to authorized project members) | 6 | Collaborative contributions Google Doc and five contributor subfolders; team attribution still requires agreement |
| SRC-03 | [User's project subfolder](private source; available to authorized project members) | 6 | Contributions Doc, project report, `7DBJ.pdb`, ligand folder and TPM folder |
| SRC-04 | [TPM files](private source; available to authorized project members) | 12 | Twelve compressed per-sample GEO TPM files, GSM9306522–GSM9306533 |
| SRC-05 | [GSE310675_TPM](private source; available to authorized project members) | 17 | Twelve duplicated/related TPM files, `TPM_matrix.csv`, `metadata.csv`, three exploratory DEG CSVs |
| SRC-06 | [Ligands](private source; available to authorized project members) | 135 | Mostly named ZINC SDF files; number of unique ligands not yet established |
| SRC-07 | [Docking source](private source; available to authorized project members) | 31 | Docked pose archive, PDBQT receptor, ligand PDB files, docking subfolders; includes `compsBip2.xlsx`, which is likely unrelated and must be screened |
| SRC-08 | [Other docking source](private source; available to authorized project members) | 3 | `All_ligands.sdf` (20 SDF records observed in prior read), `prot.pdb`, notebook checkpoints |
| SRC-09 | [Other docking source](private source; available to authorized project members) | 146 | Additional docking results, `comps2ca.xlsx`, poses and 100+ ligand PDB files; **not yet confirmed same target/workflow** |
| SRC-10 | [GROMACS](private source; available to authorized project members) | 121 | Original MDP, TPR, XTC, EDR, log, GRO, topology and figures; contains backup versions and huge files; **no wholesale GitHub upload** |
| SRC-11 | [Colab Notebooks](private source; available to authorized project members) | 13 | Recovered 67-cell MD analysis notebook, miscellaneous unnamed notebooks; identity/relevance of each still needs tagging |
| EXCLUDE-01 | [Converted PDB models](private source; available to authorized project members) | 5 | Maize zein models; **separate research project, do not merge** |

**Inventory caveats:** Direct counts are folder-entry counts, not distinct scientific datasets, usable scripts or valid observations. Some folders contain duplicates, backups, subfolders and unrelated work. Nested descendants are **not yet exhaustively counted**. Some source locations were previously inaccessible, so this is a partial inventory.

## Source classification

| Artifact | Category | Role | Verification / risk |
|---|---|---|---|
| NCBI GEO GSE310675 per-sample TPM | Public original processed data | Expression input | Source accession and sample metadata must be cross-checked; TPM is not raw counts |
| `TPM_matrix.csv` | Derived input matrix | PCA / exploratory expression | Rebuild from 12 source files and compare checksum / column ordering |
| `metadata.csv` | User-derived sample annotation | Defines comparison groups | **Blocking error:** Pa14C / GSM9306530 marked Q61H in archived metadata; NCBI sample says G12D |
| `DEG_TPM_ttest_FDR*.csv`, `DEG_limma_like.csv` | Derived analysis | Old DEG claims | **Quarantine from final results** until grouping and model are corrected; no independent significance established |
| Enrichment plots and notebooks | Derived analysis | Pathway claims | Five up / five down input was challenged by supervisor; methodology to be rebuilt |
| `7DBJ.pdb` | Protein structure | LDHB reference | Confirm chain, cofactors, ligands, biological assembly and prepared receptor mapping |
| ZINC SDF library | Chemical inputs | Virtual screening | Deduplicate structures; record source IDs and provenance |
| Docking PDBQT, logs, pose archives | Computation artifacts | Ranking and poses | Receptor, box, protonation, score extraction, control and selected-pose lineage need validation |
| `BESTLIGAND.mol2` | MD ligand structure | MD parameterization | Prior RDKit match suggests 3-methylfluoranthene, **but ZINC provenance and selected docking pose are not established** |
| `step5_production.mdp`, final log | Original simulation settings / execution evidence | MD provenance | 20 ns, 310 K, GROMACS 2024.4; final log reaches 20.0026 ns |
| `step5_production_SOLU.tpr` and `all_noPBC.xtc` | Extracted MD analysis inputs | 201-frame, 0–20 ns analysis | Independent PBC-aware reanalysis exists; raw COM trace contains image artifacts |
| `ZS of MD_analysis_biotech_4th.ipynb` | Original analysis code | Archived notebook | Recovered and statically audited; no clean execution verified |
| `Report all.docx` supervisor comments | Review source | Revision requirements | Seven comments previously extracted; map each to a fix and evidence |

## Immediate scientific blockers (ordered)

**P0.1 Genotype manifest:** Download/inspect all 12 primary GEO sample annotations. Create `sample_manifest.tsv` with GSM, cell line, KRAS mutation, citation URL, grouping rationale and verification status. **Do not rerun a pre-existing 4-vs-8 split unchanged.**

**P0.2 Design and statistical feasibility:** Determine whether raw counts and biological replicates are available. Assess independence, group composition and confounders. If only 12 cell-line TPM profiles exist, distinguish exploratory cross-cell-line associations from robust differential expression claims; do not promise significant DEGs.

**P0.3 Enrichment:** Freeze the old top-5-gene ORA. Decide ORA with a justified gene universe or a carefully designed ranked analysis after validating statistical inputs. Report null results if warranted.

**P0.4 Target and ligand chain:** Establish biological evidence for LDHB, verify PDB 7DBJ preparation and the exact ZINC -> docking -> MD ligand structure path. A high docking score and 20 ns proximity do not demonstrate inhibition.

**P0.5 Reproducibility:** Build dependency lockfiles, provenance checksums, exact commands, tests, figures and provenance manifests. Distinguish archived original notebooks from corrected workflows.

**P0.6 Supervisor report:** Correct KRAS mechanistic explanation, first-author/year citations, fold-change/p-value criteria, enrichment methods, protein rationale, ligand identity and the KRAS-vs-LDHB MD labeling inconsistency.

## Proposed working tree (do not relocate original Drive data)

```text
data_manifest/
  source_inventory.tsv
  sample_manifest.tsv
  ligand_provenance.tsv
  checksums.sha256
scripts/
  01_validate_samples.py
  02_build_expression_matrix.py
  03_expression_qc.py
  04_exploratory_statistics.py
  05_enrichment.py
  06_validate_ligands.py
  analyze_md.py
results/
  transcriptomics/
  enrichment/
  docking/
  md/
docs/
  MASTER_DATA_AUDIT.md
  SUPERVISOR_FEEDBACK_ACTION_PLAN.md
  METHODS_DECISIONS.md
  PUBLICATION_READINESS.md
```

This is a **target structure**, not a claim these files all exist.

## Evidence status legend

- **Located** = name and accessible source path verified.
- **Inspected** = actual contents reviewed.
- **Reproduced** = rerun from documented inputs with matching outputs.
- **Validated** = independent scientific, statistical and chemical checks passed.
- **Publication-ready** = sufficient method, interpretation, provenance and authorship review complete.

Most artifacts are **located**; several are **inspected**; MD geometry has a limited independent **reanalysis**. The end-to-end pipeline is **not yet reproduced or validated**.

## Next audit milestone

Create a corrected 12-sample GEO genotype manifest with source URLs and a discrepancy table, then verify the TPM matrix shape and sample column mapping. Stop before any final DEG/ORA claim until the sample manifest and statistical design are accepted.

**Privacy and attribution:** Keep repository private pending explicit user authorization for public release; preserve collaborator credit, project ownership, licensing, and source permissions.
