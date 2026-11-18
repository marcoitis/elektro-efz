#!/usr/bin/env python3
"""Structural checks for v0.9.3. This does NOT replace expert content review."""
import json,sys,re
from pathlib import Path
from xml.etree import ElementTree as ET
root=Path(__file__).resolve().parent.parent
items=json.loads((root/'lesson-workbooks.json').read_text('utf8'))
assert len(items)==178 and len({v['id'] for v in items})==178
assert sum(v['isNorm'] for v in items)==33
assert len(list((root/'workbooks').glob('*.md')))==178
assert len(list((root/'learning-visuals').glob('*.svg')))==178
for v in items:
 assert len(v['parts'])>=2,(v['id'],'missing technical paragraphs')
 assert len(v['quiz'])==3,(v['id'],'wrong quiz count')
 assert len(v['learningGoals'])>=2,(v['id'],'learning objectives')
 assert len(v['sessionPlan'])==6 and sum(item['minutes'] for item in v['sessionPlan'])==25,(v['id'],'guided session')
 assert v['ttsWords']>50,(v['id'],'missing scripts')
 assert v['editorialRelease'].startswith('OFFEN') or ('15–30-Minuten-Fachmanuskript erstellt' in v['editorialRelease'] and 1950<=v['ttsWords']<=3900 and v['fullManuscript']),v['id']
 assert v['technicalRelease'].startswith('OFFEN'),v['id']
 for q in v['quiz']:
  assert 0<=q['correct']<len(q['options'])
  assert len(q['why'])>=5
 path=root/'learning-visuals'/(v['id']+'.svg')
 ET.parse(path)
 assert (root/'workbooks'/(v['id']+'.md')).exists()
html=(root/'kurskompass.html').read_text('utf8')
assert html.count('"editorialRelease"')==178
assert '<script id="data" type="application/json">' in html
assert 'fullManuscript' in html and 'Keine unabhängige Normenfreigabe' in html
source=(root/'index.html').read_text('utf8')
assert 'kurskompass.html' in source
sw=(root/'sw.js').read_text('utf8')
assert './kurskompass.html' in sw and sw.count('./learning-visuals/')==178
print('OK – 178 Lernmappen, 178 spezifische SVG-Lernübersichten, 534 Quizfragen, Navigation und Offline-Katalog. Keine fachliche Einzelabnahme behauptet.')
