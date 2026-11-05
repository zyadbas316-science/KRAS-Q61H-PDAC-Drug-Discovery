# Data provenance

This folder holds small project coordinate files, but **not the full raw research datasets**. Files are archival inputs, not independently validated simulations.

## Data sources

| Data | Public source / status |
| --- | --- |
| Gene-level TPM for 12 PDAC cell lines | NCBI GEO series **GSE310675** (GSM9306522–GSM9306533); original 12 gz files used for the independent review |
| Reference LDHB crystal structure | RCSB PDB **7DBJ**; 1.55 Å, 2021 public release |
| ZINC candidate compounds | See original ligand notebook and ZINC; exact complete ID list and licensing need checking |
| Project complex and ligand coordinates | `structures/BESTCOMPLEX.pdb` and `structures/BESTLIGAND.mol2`; from project source folder |
| Docking score spreadsheet and pose archive | Included under `results/docking/`; 508 logs, 504 with scored modes, 4 missing scores |
| MD trajectories | Not included; original run files and analysis need verification |

- GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE310675
- Structure: https://www.rcsb.org/structure/7DBJ

### Notes

- Raw GEO samples were examined for QC, but are not duplicated in this repository.
- Docking Vina logs and original pose files are included in one compressed 2.9 MB archive for reproducibility; parse them with `scripts/parse_vina_logs.py`.
- The project PDB includes `UNL` chain X ligand ATOM records: check structure compatibility before simulation.
- Large MD output and raw downloads should remain outside Git; add hashes, manifests and retrieval instructions.
- Avoid uploading access tokens, Colab account data and collaborator private information.
