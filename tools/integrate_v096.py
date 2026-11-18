#!/usr/bin/env python3
"""Idempotent integration of editorial_v096 content, without changing stored lesson IDs."""
from pathlib import Path
R=Path(__file__).resolve().parent.parent
substitutions={
 'tools/install_editorial_samples.py': [('editorial_v092\',\'editorial_v094\',\'editorial_v095','editorial_v092\',\'editorial_v094\',\'editorial_v095\',\'editorial_v096'),('v0.9.5','v0.9.6')],
 'tools/create_long_slides.py': [("* (R/'editorial_v095').glob('*.txt')", "* (R/'editorial_v095').glob('*.txt'), * (R/'editorial_v096').glob('*.txt')")],
 'tools/create_quality_matrix.py': [("'editorial_v092','editorial_v094','editorial_v095'", "'editorial_v092','editorial_v094','editorial_v095','editorial_v096'"), ("('editorial_v094','editorial_v095')", "('editorial_v094','editorial_v095','editorial_v096')"), ("'0.9.5-preflight'","'0.9.6-preflight'"),('Version 0.9.5','Version 0.9.6')],
 'tools/create_178_workbooks.py': [("'editorial_v092','editorial_v094','editorial_v095'", "'editorial_v092','editorial_v094','editorial_v095','editorial_v096'"), ("('editorial_v094','editorial_v095')", "('editorial_v094','editorial_v095','editorial_v096')")],
 'tools/quality_check_multimedia.py': [("('editorial_v092','editorial_v094','editorial_v095')", "('editorial_v092','editorial_v094','editorial_v095','editorial_v096')"),('15 long editorial scripts.','21 long editorial scripts.')],
 'tools/build_course_compass.py': [('v0.9.5','v0.9.6')],
 'tools/build_site.py': [("'version':'0.9.5'", "'version':'0.9.6'")],
 'index.html': [('v0.9.5','v0.9.6')],
 'app.js': [('v0.9.5','v0.9.6')],
 'sw.js': [('elektro-efz-shell-v095-physics-lessons-1','elektro-efz-shell-v096-materials-plans-1'), ("version:'0.9.5'", "version:'0.9.6'")],
 '.github/workflows/publish.yml': [('v0.9.5','v0.9.6'),('python tools/create_schematics_v095.py','python tools/create_schematics_v095.py\n          python tools/create_schematics_v096.py'),('python tools/verify_physics_v095.py','python tools/verify_physics_v095.py\n          python tools/verify_materials_docs_v096.py')]
}
for rel,sub in substitutions.items():
 p=R/rel;s=p.read_text('utf8')
 for old,new in sub:
  if new in s:continue
  if old not in s: raise RuntimeError(f'Expected marker missing in {rel}: {old}')
  s=s.replace(old,new)
 p.write_text(s,encoding='utf8')
# Previous v0.9.5 manuscript unintentionally duplicated one paragraph.
p=R/'editorial_v095/1.10-B.txt';paragraphs=p.read_text('utf8').split('\n\n');seen=set();out=[]
for paragraph in paragraphs:
 if len(paragraph)>150 and paragraph in seen: continue
 out.append(paragraph)
 if len(paragraph)>150:seen.add(paragraph)
p.write_text('\n\n'.join(out),encoding='utf8')
print('Integrate v0.9.6 completed')
