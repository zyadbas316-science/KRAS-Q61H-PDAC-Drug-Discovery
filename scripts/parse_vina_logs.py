"""Extract ranked AutoDock Vina 1.2.x affinities from logs inside a .tgz archive."""
from __future__ import annotations
import argparse
import csv
import json
import re
import tarfile
from collections import Counter
from pathlib import Path

POSE_RE = re.compile(r'^\s*(\d+)\s+(-?\d+(?:\.\d+)?)\s+([-\d.]+)\s+([-\d.]+)\s*$')


def parse_archive(archive: Path, output_csv: Path) -> dict:
    rows, versions, settings = [], Counter(), Counter()
    with tarfile.open(archive, mode='r:gz') as tf:
        for member in tf:
            if not member.isfile() or not member.name.endswith('.log'):
                continue
            with tf.extractfile(member) as file_obj:
                text = file_obj.read().decode('utf-8', errors='replace')
            match = re.search(r'AutoDock Vina v([\d.]+)', text)
            versions[match.group(1) if match else 'unknown'] += 1
            center = re.search(r'Grid center:\s*X\s*([-\d.]+)\s*Y\s*([-\d.]+)\s*Z\s*([-\d.]+)', text)
            box = re.search(r'Grid size\s*:\s*X\s*([-\d.]+)\s*Y\s*([-\d.]+)\s*Z\s*([-\d.]+)', text)
            exhaustive = re.search(r'Exhaustiveness:\s*(\d+)', text)
            settings[str((center.groups() if center else None,
                          box.groups() if box else None,
                          exhaustive.group(1) if exhaustive else None))] += 1
            scores = []
            for line in text.splitlines():
                m = POSE_RE.fullmatch(line)
                if m:
                    scores.append(float(m.group(2)))
            if len(scores) > 9:
                raise ValueError('More than nine docking modes; update the output schema')
            rows.append({'conformer_log': Path(member.name).stem,
                         'n_modes': len(scores),
                         **{f'pose_{i+1:02d}_kcal_mol': x for i, x in enumerate(scores)}})
    if not rows:
        raise ValueError('Archive has no Vina .log files')
    rows.sort(key=lambda x: x.get('pose_01_kcal_mol', float('inf')))
    cols = ['conformer_log', 'n_modes'] + [f'pose_{i:02d}_kcal_mol' for i in range(1, 10)]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(rows)
    result = {'total_logs': len(rows), 'logs_with_modes': sum(bool(x['n_modes']) for x in rows),
              'logs_without_modes': sum(not x['n_modes'] for x in rows),
              'versions': dict(versions), 'grid_and_exhaustiveness': dict(settings)}
    output_csv.with_suffix('.audit.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(parse_archive(a.archive, a.output), indent=2))


if __name__ == '__main__':
    main()
