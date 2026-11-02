"""Regression coverage for the shipped OpenClaw installation, not the MCP backend."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]

class PackageTests(unittest.TestCase):
    def test_release_avoids_http_cwd_projection_and_ships_uploader(self):
        subprocess.run([sys.executable, str(ROOT / 'scripts/build-openclaw-bundle.py')], check=True)
        for filename, prefix in [('postroom-openclaw-0.1.1.zip', 'skills/postroom/'),
                                 ('postroom-skill-1.0.1.zip', '')]:
            path = ROOT / 'downloads' / filename
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                self.assertFalse(any(name.endswith('.mcp.json') for name in names))
                self.assertIn(prefix + 'SKILL.md', names)
                helper = archive.read(prefix + 'scripts/postroom-upload.py')
                self.assertEqual(helper, (ROOT / 'scripts/postroom-upload.py').read_bytes())
                compile(helper, filename, 'exec')
                self.assertFalse(any('__pycache__' in name or name.endswith('.pyc') for name in names))
                self.assertTrue(all(not name.startswith('/') and '..' not in Path(name).parts for name in names))
            expected = path.with_suffix('.zip.sha256').read_text().split()[0]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)
        bundle = ROOT / 'distributions/openclaw'
        self.assertNotIn('.mcp.json', json.loads((bundle / 'package.json').read_text())['files'])
        self.assertEqual((bundle / 'skills/postroom/SKILL.md').read_bytes(),
                         (ROOT / 'openclaw/postroom/SKILL.md').read_bytes())

    def test_archives_are_reproducible(self):
        build = [sys.executable, str(ROOT / 'scripts/build-openclaw-bundle.py')]
        subprocess.run(build, check=True, capture_output=True)
        paths = [ROOT / 'downloads' / name for name in
                 ['postroom-openclaw-0.1.1.zip', 'postroom-skill-1.0.1.zip']]
        before = [path.read_bytes() for path in paths]
        subprocess.run(build, check=True, capture_output=True)
        self.assertEqual(before, [path.read_bytes() for path in paths])

if __name__ == '__main__':
    unittest.main()
