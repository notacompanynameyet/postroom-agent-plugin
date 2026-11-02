"""Build deterministic, reviewed OpenClaw bundle/skill ZIPs; no checkout metadata."""
from pathlib import Path
import hashlib
import zipfile
ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    (ROOT / 'distributions/openclaw', ROOT / 'downloads/postroom-openclaw-0.1.0.zip'),
    (ROOT / 'openclaw/postroom', ROOT / 'downloads/postroom-skill-1.0.0.zip'),
]
for source, destination in SOURCES:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob('*')):
            if path.is_symlink():
                raise ValueError(f'Symlink not allowed: {path}')
            if path.is_file():
                info = zipfile.ZipInfo(path.relative_to(source).as_posix(), (2026, 11, 2, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise ValueError('Archive integrity failed')
        print(destination.name, len(archive.namelist()), 'files')
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    destination.with_suffix(destination.suffix + '.sha256').write_text(f'{digest}  {destination.name}\n')
