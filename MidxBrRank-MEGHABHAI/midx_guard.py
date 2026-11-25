"""Checks for the compiled MIDx Termux distribution; not tamper-proof."""
import hashlib
import importlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
HOME = Path('/data/data/com.termux/files/home').resolve()
PREFIX = Path('/data/data/com.termux/files/usr').resolve()
MODULES = {'httpx':'httpx', 'google-play-scraper':'google_play_scraper',
           'pycryptodome':'Crypto', 'protobuf-decoder':'protobuf_decoder',
           'protobuf':'google.protobuf', 'requests':'requests', 'aiohttp':'aiohttp', 'urllib3':'urllib3'}


def verify():
    if not os.environ.get('PREFIX') or Path(os.environ['PREFIX']).resolve() != PREFIX:
        raise RuntimeError('Run this program from the Termux app.')
    try:
        ROOT.relative_to(HOME)
    except ValueError:
        raise RuntimeError('Move this folder to Termux private home (~/), not shared storage.')
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    for name, expected in manifest.items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Compiled module missing or modified: ' + name)


def missing_requirements():
    missing = []
    for raw in (ROOT / 'requirements.txt').read_text(encoding='utf-8').splitlines():
        name = raw.strip()
        if not name or name.startswith('#'):
            continue
        if name not in MODULES:
            raise ValueError('Unsupported requirement entry: ' + name)
        try:
            importlib.metadata.version(name)
            spec = importlib.util.find_spec(MODULES[name])
        except (importlib.metadata.PackageNotFoundError, ImportError, ModuleNotFoundError, ValueError):
            spec = None
        if spec is None:
            missing.append(name)
    return missing


def ensure_requirements():
    missing = missing_requirements()
    if not missing:
        return
    print('  Missing requirements: ' + ', '.join(missing), flush=True)
    print('  Installing requirements for this Python interpreter...', flush=True)
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(ROOT / 'requirements.txt')], check=True)
    importlib.invalidate_caches()
    missing = missing_requirements()
    if missing:
        raise RuntimeError('Requirements still unavailable after installation: ' + ', '.join(missing))
