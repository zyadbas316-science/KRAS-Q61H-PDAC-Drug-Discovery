# Curated original Colab notebooks

| Notebook | Source topic | Current state |
| --- | --- | --- |
| `transcriptomics/kras_q61h_tpm_exploration.ipynb` | GEO TPM and candidate genes | Reviewed; statistical conclusions provisional |
| `ligand-screening/collect_zinc_ligands.ipynb` | Ligand SDF downloads | Reviewed; requires input ID list |
| `enrichment/enrichment_exploration.ipynb` | GO/KEGG/Reactome | Reviewed; fixed exploratory gene lists |
| `docking/protein_140_ligand_docking.ipynb` | Original Vina docking pipeline | Curated; destructive cleanup disabled; inputs and execution not validated |
| `molecular-dynamics/gromacs_colab_workflow.ipynb` | GROMACS Colab preparation/run | Archived source; input paths inconsistent; run inputs now partially verified |
| `molecular-dynamics/original_md_analysis_colab.ipynb` | **Recovered original MD analysis** | Archived 67-cell source, output-free; not certified to run; [audit](../docs/MD_ORIGINAL_NOTEBOOK_AUDIT.md) |

These notebooks preserve original code cells in their original order. Cached outputs, execution counts and incidental metadata were removed. Four direct-download file identifiers in the MD notebook were redacted. **They are not certified to run end-to-end** and have not been executed as part of the audit.

Please see [scientific audit](../docs/SCIENTIFIC_AUDIT.md) for errors and interpretations. The original docking **and MD analysis notebooks have both been recovered and curated** from their Colab source files. The separately implemented `scripts/analyze_md.py` is a new independent analysis rather than an original source notebook.
