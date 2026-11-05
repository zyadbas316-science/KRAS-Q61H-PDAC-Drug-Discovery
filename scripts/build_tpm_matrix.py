"""Assemble gene-level TPM sample files from GEO GSE310675.

Exploratory preprocessing only: this does not infer differential expression.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

SUFFIX = '_Gene_TPM.txt.gz'


def build_matrix(input_dir: Path, output_dir: Path, group_file: Path | None = None) -> dict:
    # Require an explicit, independently verified sample-to-group mapping.
    groups = {}
    if group_file is not None:
        mapping = pd.read_csv(group_file)
        if not {'accession', 'group'}.issubset(mapping.columns):
            raise ValueError('Group mapping needs accession and group columns')
        if mapping['accession'].duplicated().any():
            raise ValueError('Group mapping has duplicate accessions')
        if not mapping['group'].isin(['KRAS_Q61H', 'Non_Q61H']).all():
            raise ValueError('Invalid group name in mapping')
        groups = dict(zip(mapping['accession'], mapping['group']))
    paths = sorted(input_dir.glob('*' + SUFFIX))
    if not paths:
        raise FileNotFoundError(f'No files ending in {SUFFIX} found in {input_dir}')
    frames, metadata, summaries = [], [], []
    for path in paths:
        stem = path.name.removesuffix('.txt.gz')
        parts = stem.split('_')
        if len(parts) < 3 or not stem.endswith('_Gene_TPM'):
            raise ValueError(f'Unexpected GEO sample filename: {path.name}')
        line = parts[1]
        table = pd.read_csv(path, sep='\t', compression='gzip')
        if not {'Gene', 'TPM'}.issubset(table.columns):
            raise ValueError(f'Missing Gene/TPM columns: {path.name}')
        if table['Gene'].isna().any() or table['Gene'].duplicated().any():
            raise ValueError(f'Invalid or duplicate gene IDs in {path.name}')
        values = pd.to_numeric(table['TPM'], errors='raise')
        if not np.isfinite(values).all() or (values < 0).any():
            raise ValueError(f'Invalid TPM values in {path.name}')
        frames.append(pd.Series(values.to_numpy(), index=table['Gene'], name=stem))
        accession = parts[0]
        if group_file is not None and accession not in groups:
            raise ValueError(f'Missing verified group for {accession}')
        group = groups.get(accession, 'UNVERIFIED')
        metadata.append({'sample': stem, 'accession': accession, 'cell_line': line, 'group': group})
        summaries.append({'sample': stem, 'genes': int(len(values)), 'tpm_sum': float(values.sum())})
    matrix = pd.concat(frames, axis=1, join='inner')
    if matrix.empty or matrix.isna().any().any():
        raise ValueError('Empty merged matrix or missing TPM values')
    matrix.index.name = 'gene'
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(output_dir / 'TPM_matrix.csv')
    pd.DataFrame(metadata).to_csv(output_dir / 'metadata.csv', index=False)
    report = {'samples': len(paths), 'shared_genes': len(matrix), 'input_summaries': summaries,
              'warning': 'Groups are UNVERIFIED unless explicitly supplied using --groups-file from checked primary GEO metadata.'}
    (output_dir / 'tpm_qc.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input-dir', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--groups-file', type=Path, default=None)
    a = p.parse_args()
    print(json.dumps(build_matrix(a.input_dir, a.output_dir, a.groups_file), indent=2))


if __name__ == '__main__':
    main()
