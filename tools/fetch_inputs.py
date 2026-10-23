"""Fetch original benchmark inputs and reproduce hash-bound derived artifacts.

Does not change certificates, manifests, scores, or accepted frontiers.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import tempfile
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'external-inputs.json').read_text())


def checked(path, expected):
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected


def install(path, data, expected):
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f'Input hash mismatch: {path.relative_to(ROOT)}; accepted evidence was not changed')
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        stream.write(data)
        temporary = Path(stream.name)
    os.replace(temporary, path)


def download(row):
    path = ROOT / row['path']
    if checked(path, row['sha256']):
        return
    for attempt in range(3):
        try:
            request = urllib.request.Request(row['url'], headers={'User-Agent': 'Mozilla/5.0 (DiscoveryAtHome research input fetch)'})
            with urllib.request.urlopen(request, timeout=45) as response:
                data = response.read(20_000_001)
            if len(data) > 20_000_000:
                raise ValueError('Input exceeds bounded download size')
            install(path, data, row['sha256'])
            print('Fetched and verified', row['path'], flush=True)
            return
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def derive(row):
    path = ROOT / row['path']
    if checked(path, row['sha256']):
        return
    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary) / Path(row['path']).name
        if row['recipe'] == 'scipy-csc':
            from scipy.io import mmread
            from scipy.sparse import csc_matrix, save_npz
            matrix = csc_matrix(mmread(ROOT / row['source']))
            matrix.eliminate_zeros()
            matrix.sort_indices()
            save_npz(target, matrix)
            data = target.read_bytes()
        elif row['recipe'] == 'hanoi-design':
            import wntr
            network = wntr.network.WaterNetworkModel(str(ROOT / row['source']))
            network.options.hydraulic.accuracy = 1e-8
            network.options.hydraulic.trials = 200
            network.options.hydraulic.unbalanced = 'STOP'
            network.options.hydraulic.unbalanced_value = 0
            network.options.hydraulic.demand_model = 'DDA'
            network.options.time.duration = 0
            for _, pipe in network.pipes():
                pipe.diameter = 1.016
            wntr.network.write_inpfile(network, str(target), units='CMH', version=2.2)
            # WNTR's three provenance comments contain the source path and wall time.
            # Restore the archived comments to reproduce its original byte hash.
            lines = target.read_text().splitlines(keepends=True)
            assert all(line.startswith(';') for line in lines[:3])
            data = (''.join(row['frozen_comment_header']) + ''.join(lines[3:])).encode()
        else:
            raise ValueError('Unknown derivation recipe')
        install(path, data, row['sha256'])
        print('Reconstructed and verified', row['path'], flush=True)


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(download, MANIFEST['downloads']))
    for row in MANIFEST['derived']:
        derive(row)
    print('All required external inputs match frozen hashes. Upstream terms still apply.')
