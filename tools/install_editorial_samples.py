#!/usr/bin/env python3
"""Install genuinely hand-edited long manuscripts only; never pad other lessons."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
EDITED = {p.stem: p for folder in ('editorial_v092','editorial_v094','editorial_v095','editorial_v096','editorial_v097') for p in (R/folder).glob('*.txt')}
for p in EDITED.values():
 words=len(p.read_text(encoding='utf-8').split())
 if words<1950 or words>3900:raise ValueError(f'{p.name} is not in 15-30 min editorial range: {words} words')
 (R/'tts_scripts'/p.name).write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
 print('Installed',p.stem,words,'~',round(words/130,1),'min')
lect={p.stem:p.read_text(encoding='utf-8') for p in sorted((R/'tts_scripts').glob('*.txt'))}
assert len(lect)==178
(R/'lecture-scripts.js').write_text('/* Elektro EFZ v0.9.7: individually edited manuscripts; not norm-certified. */\nwindow.ElektroLectures='+json.dumps(lect,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
