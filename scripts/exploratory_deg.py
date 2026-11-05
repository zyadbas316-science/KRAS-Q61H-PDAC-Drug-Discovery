"""Exploratory Welch test on log2(TPM+1), not a clinical or count-based DEG model."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests


def test_expression(matrix_path: Path, metadata_path: Path, output_path: Path) -> dict:
    tpm = pd.read_csv(matrix_path, index_col='gene')
    meta = pd.read_csv(metadata_path)
    if not {'sample', 'group'}.issubset(meta.columns):
        raise ValueError('Metadata must contain sample and group columns')
    if not np.isfinite(tpm.to_numpy(dtype=float)).all() or (tpm < 0).any().any():
        raise ValueError('TPM matrix contains invalid values')
    mutant = meta.loc[meta.group == 'KRAS_Q61H', 'sample'].tolist()
    control = meta.loc[meta.group == 'Non_Q61H', 'sample'].tolist()
    if len(mutant) < 2 or len(control) < 2:
        raise ValueError('Welch test requires at least two samples in each group')
    if len(set(mutant + control)) != len(mutant) + len(control):
        raise ValueError('Metadata has duplicate sample assignments')
    if set(tpm.columns) != set(mutant + control):
        raise ValueError('Matrix and metadata sample sets differ')
    log_tpm = np.log2(tpm + 1.0)
    with np.errstate(invalid='ignore'):
        _, raw_p = ttest_ind(log_tpm[mutant].to_numpy(), log_tpm[control].to_numpy(),
                             axis=1, equal_var=False, nan_policy='omit')
    safe_p = np.where(np.isfinite(raw_p), raw_p, 1.0)
    q = multipletests(safe_p, method='fdr_bh')[1]
    delta = (log_tpm[mutant].mean(axis=1) - log_tpm[control].mean(axis=1)).to_numpy()
    result = pd.DataFrame({'gene': tpm.index, 'mean_log2_tpm_delta': delta,
                           'welch_pvalue': safe_p, 'bh_fdr': q})
    result.sort_values('welch_pvalue', inplace=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    return {'genes_tested': len(result), 'n_q61h': len(mutant), 'n_comparison': len(control),
            'fdr_below_0_05': int((q < 0.05).sum()), 'minimum_fdr': float(q.min())}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--matrix', type=Path, required=True)
    p.add_argument('--metadata', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    print(test_expression(a.matrix, a.metadata, a.output))


if __name__ == '__main__':
    main()
