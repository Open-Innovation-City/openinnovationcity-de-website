#!/usr/bin/env python3
"""
One-time migration script: replaces <header>...</header> in all HTML files
with a placeholder <header id="site-header"></header> and adds nav-loader.js.

Run once from the repository root:
    python3 inject-nav.py

After running, nav-de.html and nav-en.html are the single source of truth
for the navigation. This script can be kept for re-running or deleted.
"""

import re
import sys
from pathlib import Path

HEADER_RE = re.compile(r'<header>.*?</header>', re.DOTALL)
STYLE_BLOCK_RE = re.compile(
    r'\n?<style>\n/\* Static archive: desktop navigation layout \*/.*?</style>\n',
    re.DOTALL
)
PLACEHOLDER = '<header id="site-header"></header>'
SCRIPT_TAG = '<script src="/nav-loader.js"></script>\n'
SKIP_FILES = {'nav-de.html', 'nav-en.html'}

root = Path(__file__).parent
updated = 0
skipped = 0

for html_file in sorted(root.rglob('*.html')):
    if html_file.name in SKIP_FILES:
        continue

    try:
        text = html_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f'SKIP (read error): {html_file} — {e}', file=sys.stderr)
        skipped += 1
        continue

    if 'id="site-header"' in text:
        print(f'already migrated: {html_file.relative_to(root)}')
        skipped += 1
        continue

    if not HEADER_RE.search(text):
        print(f'no <header> found: {html_file.relative_to(root)}')
        skipped += 1
        continue

    # Remove the inline style block that is now baked into nav-de.html / nav-en.html
    text = STYLE_BLOCK_RE.sub('', text)

    # Replace <header>…</header> with placeholder
    text = HEADER_RE.sub(PLACEHOLDER, text, count=1)

    # Insert nav-loader.js before </body>
    if '</body>' in text:
        text = text.replace('</body>', SCRIPT_TAG + '</body>', 1)
    else:
        print(f'WARNING: no </body> in {html_file.relative_to(root)}')

    try:
        html_file.write_text(text, encoding='utf-8')
        print(f'updated: {html_file.relative_to(root)}')
        updated += 1
    except Exception as e:
        print(f'ERROR writing {html_file}: {e}', file=sys.stderr)

print(f'\nDone. {updated} files updated, {skipped} skipped.')
