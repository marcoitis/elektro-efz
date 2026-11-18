#!/usr/bin/env python3
"""Integrate six subject-authored 1.07/1.08 manuscripts into existing offline PWA without changing IDs or storage."""
from pathlib import Path
R=Path(__file__).resolve().parent.parent
for name in ('tools/install_editorial_samples.py','tools/create_quality_matrix.py','tools/create_178_workbooks.py','tools/quality_check_multimedia.py'):
 p=R/name;s=p.read_text('utf8')
 if "'editorial_v096','editorial_v097'" not in s:
  s=s.replace("'editorial_v096'", "'editorial_v096','editorial_v097'")
 p.write_text(s,'utf8')
p=R/'tools/create_long_slides.py';s=p.read_text('utf8')
if "* (R/'editorial_v097').glob('*.txt')" not in s:
 s=s.replace("* (R/'editorial_v096').glob('*.txt')", "* (R/'editorial_v096').glob('*.txt'), * (R/'editorial_v097').glob('*.txt')")
p.write_text(s,'utf8')
# Version labels must be unambiguous; no content-ID changes.
for name in ('tools/install_editorial_samples.py','tools/create_quality_matrix.py','tools/build_course_compass.py','tools/build_site.py','index.html','app.js','sw.js','offline.js'):
 p=R/name;s=p.read_text('utf8').replace('v0.9.6','v0.9.7').replace("'version':'0.9.6'", "'version':'0.9.7'").replace("version:'0.9.6'", "version:'0.9.7'")
 if name=='sw.js':s=s.replace('elektro-efz-shell-v096-materials-plans-1','elektro-efz-shell-v097-montage-measurement-1')
 if name=='offline.js':s=s.replace('elektro-efz-shell-v095-physics-lessons-1','elektro-efz-shell-v097-montage-measurement-1')
 if name=='app.js':
  old="!['0.9.1','0.9.2'].includes(info.version)"
  assert old in s,'expected old audio-manifest whitelist'
  s=s.replace(old,"!/^0\\.9\\.[1-9]\\d*$/.test(String(info.version))")
 p.write_text(s,'utf8')
p=R/'tools/quality_check_multimedia.py';s=p.read_text('utf8').replace('21 long editorial scripts.','27 long editorial scripts.')
p.write_text(s,'utf8')
p=R/'tools/create_quality_matrix.py';t=p.read_text('utf8').replace("'0.9.6-preflight'","'0.9.7-preflight'").replace('Version 0.9.6','Version 0.9.7');p.write_text(t,'utf8')
import re
sw=(R/'sw.js').read_text('utf8')
off=(R/'offline.js').read_text('utf8')
core=re.search(r'const CORE=(\[.*?\]);\nself\.addEventListener',sw,re.S)
files=re.search(r'const FILES=(\[.*?\]);\nconst root=',off,re.S)
assert core and files
(R/'offline.js').write_text(off[:files.start(1)]+core.group(1)+off[files.end(1):],'utf8')
p=R/'.github/workflows/publish.yml';s=p.read_text('utf8').replace('v0.9.6','v0.9.7')
if 'python tools/create_schematics_v097.py' not in s:s=s.replace('python tools/create_schematics_v096.py','python tools/create_schematics_v096.py\n          python tools/create_schematics_v097.py')
if 'python tools/verify_montage_measurement_v097.py' not in s:s=s.replace('python tools/verify_materials_docs_v096.py','python tools/verify_materials_docs_v096.py\n          python tools/verify_montage_measurement_v097.py')
if 'python tools/verify_offline_v097.py' not in s:s=s.replace('python tools/verify_montage_measurement_v097.py', 'python tools/verify_montage_measurement_v097.py\n          python tools/verify_offline_v097.py')
p.write_text(s,'utf8')
print('v0.9.7 integration complete')
