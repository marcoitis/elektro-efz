#!/usr/bin/env python3
"""Offline asset-list and artifact checks. Cannot replace an actual iPhone flight-mode test."""
from pathlib import Path
import re
R=Path(__file__).resolve().parent.parent
sw=(R/'sw.js').read_text('utf8')
of=(R/'offline.js').read_text('utf8')
cache1=re.search(r"const CACHE='([^']+)'",sw).group(1)
cache2=re.search(r"const CACHE='([^']+)'",of).group(1)
assert cache1==cache2,(cache1,cache2)
paths1=re.findall(r"'((?:\./)[^']+)'",sw.split('const CORE=',1)[1].split('];',1)[0])
paths2=re.findall(r"'((?:\./)[^']+)'",of.split('const FILES=',1)[1].split('];',1)[0])
assert set(paths1)==set(paths2),(len(paths1),len(paths2),set(paths1)^set(paths2))
assert len(paths1)==len(set(paths1))
assert './kurskompass.html' in paths1
assert sum(x.startswith('./visuals/') for x in paths1)==178
assert sum(x.startswith('./learning-visuals/') for x in paths1)==178
site=R/'dist-v097-probe'
for url in paths1:
 file=R/('index.html' if url=='./' else url[2:])
 assert file.is_file(),file
 if site.exists():assert (site/('index.html' if url=='./' else url[2:])).exists(),url
print('PASS: offline and worker caches identical:',cache1,'with',len(paths1),'unique paths (178+178 SVGs and course compass)')
