"""Independent geometric MD reanalysis, not the original Colab analysis code.

Inputs: matching solute-only .tpr and PBC-processed .xtc.
Units are Angstrom for distances and nanoseconds for time.
Requires MDAnalysis, scipy, numpy, pandas.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import MDAnalysis as mda
import numpy as np
import pandas as pd
from MDAnalysis.analysis.align import rotation_matrix
from MDAnalysis.lib.distances import minimize_vectors
from scipy.spatial.distance import cdist


def analyze(tpr: Path, xtc: Path, output: Path, cutoff: float = 4.0) -> dict:
    universe = mda.Universe(str(tpr), str(xtc), topology_format="TPR", format="XTC")
    protein = universe.select_atoms("protein")
    ca = protein.select_atoms("name CA")
    ligand = universe.select_atoms("resname UNL")
    protein_heavy = protein.select_atoms("not element H")
    ligand_heavy = ligand.select_atoms("not element H")
    if not len(ca) or not len(ligand_heavy):
        raise ValueError("Missing protein C-alpha atoms or UNL heavy atoms")
    universe.trajectory[0]
    reference_ca = ca.positions.astype(np.float64).copy()
    ref_center = reference_ca.mean(axis=0)
    prot_com_ref, lig_com_ref = protein.center_of_mass(), ligand.center_of_mass()
    delta_ref = lig_com_ref - prot_com_ref
    shift_ref = minimize_vectors(delta_ref[None, :], universe.trajectory.ts.dimensions)[0] - delta_ref
    reference_ligand = ligand_heavy.positions.astype(np.float64).copy() + shift_ref
    resid_to_name = {r.ix: f"{r.resname}{r.resid}" for r in protein.residues}
    contact_counts = Counter()
    timeseries, aligned_ca = [], []

    for frame in universe.trajectory:
        current_ca = ca.positions.astype(np.float64)
        mobile_center = current_ca.mean(axis=0)
        rotation, _ = rotation_matrix(current_ca - mobile_center, reference_ca - ref_center)
        fitted_ca = (current_ca - mobile_center) @ rotation.T + ref_center
        aligned_ca.append(fitted_ca)
        protein_com, ligand_com = protein.center_of_mass(), ligand.center_of_mass()
        delta = ligand_com - protein_com
        delta_minimum = minimize_vectors(delta[None, :], frame.dimensions)[0]
        ligand_near = ligand_heavy.positions.astype(np.float64) + delta_minimum - delta
        fitted_ligand = (ligand_near - mobile_center) @ rotation.T + ref_center
        atom_distances = cdist(protein_heavy.positions, ligand_near)
        residue_indices = set(protein_heavy.resindices[atom_distances.min(axis=1) <= cutoff])
        for rid in residue_indices:
            contact_counts[resid_to_name[rid]] += 1
        timeseries.append({
            "time_ns": float(frame.time) / 1000,
            "protein_ca_rmsd_A": float(np.sqrt(np.mean(np.sum((fitted_ca - reference_ca) ** 2, axis=1)))),
            "ligand_heavy_rmsd_protein_fit_A": float(np.sqrt(np.mean(np.sum((fitted_ligand - reference_ligand) ** 2, axis=1)))),
            "protein_rg_A": float(protein.radius_of_gyration()),
            "ligand_protein_com_direct_A": float(np.linalg.norm(delta)),
            "ligand_protein_com_minimage_A": float(np.linalg.norm(delta_minimum)),
            "min_heavy_atom_distance_A": float(atom_distances.min()),
            "contacting_residues_4A": int(len(residue_indices))
        })

    df = pd.DataFrame(timeseries)
    pos = np.asarray(aligned_ca)
    rmsf = np.sqrt(np.mean(np.sum((pos - pos.mean(axis=0)) ** 2, axis=2), axis=0))
    occupancy = pd.DataFrame([
        {"residue": name, "fraction_frames_within_cutoff": count / len(df)}
        for name, count in contact_counts.items()
    ]).sort_values("fraction_frames_within_cutoff", ascending=False)
    output.mkdir(parents=True, exist_ok=True)
    df.to_csv(output / "md_timeseries.csv", index=False)
    pd.DataFrame({"resid": ca.resids, "resname": ca.resnames, "ca_rmsf_A": rmsf}).to_csv(output / "ca_rmsf.csv", index=False)
    occupancy.to_csv(output / "residue_contact_occupancy.csv", index=False)
    report = {
        "source": "computed from matching solute-only TPR and extracted XTC",
        "frames": len(df),
        "time_end_ns": float(df.time_ns.iloc[-1]),
        "protein_ca_atoms": len(ca),
        "ligand_formula_counts": dict(Counter(ligand.elements)),
        "ligand_reimaging": "minimum-image protein-ligand COM displacement",
        "caution": "Exploratory geometric descriptors; not docking validation, binding free energy or proof of biological efficacy.",
        "summary": {k: {"median": float(df[k].median()), "min": float(df[k].min()), "max": float(df[k].max())} for k in df.columns if k != "time_ns"},
        "rmsf_median_A": float(np.median(rmsf)),
        "contacts": occupancy.head(15).to_dict(orient="records")
    }
    (output / "md_summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tpr", required=True, type=Path)
    parser.add_argument("--xtc", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze(args.tpr, args.xtc, args.output), indent=2))


if __name__ == "__main__":
    main()
