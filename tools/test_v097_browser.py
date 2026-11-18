#!/usr/bin/env python3
"""Render the six v0.9.7 edited manuscripts on 390px and 1280px. No safety certification."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64
R=Path(__file__).resolve().parent.parent
IDS=['1.07-A','1.07-B','1.07-C','1.08-A','1.08-B','1.08-C']
html=(R/'kurskompass.html').read_text('utf8')
for id in IDS:
 f=R/'learning-visuals'/(id+'.svg')
 uri='data:image/svg+xml;base64,'+base64.b64encode(f.read_bytes()).decode('ascii')
 html=html.replace('./learning-visuals/'+id+'.svg',uri)
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in ((390,844),(1280,900)):
  page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='load')
  for lid in IDS:
   page.evaluate('(id)=>show(id)',lid)
   assert lid in page.locator('main .hero').inner_text(),lid
   assert page.locator('.question').count()==3,lid
   assert page.locator('details.long-lesson').count()==1,lid
   page.locator('details.long-lesson summary').click()
   txt=page.locator('.full-script').inner_text()
   assert len(txt.split())>=1950,(lid,len(txt.split()))
   assert page.locator('img.visual').evaluate('(im)=>im.complete && im.naturalWidth>0'),lid
   page.locator('.question button[data-answer="0"]').first.click()
   assert page.locator('#answer-0').is_visible(),lid
   assert page.locator('.session-item').count()==6,lid
   assert 'Keine unabhängige Normenfreigabe' in page.locator('#viewer').inner_text(),lid
  assert not errors,errors
  page.evaluate("show('1.08-B')")
  page.screenshot(path=str(R/f'preview_v097_{"mobile" if w<500 else "desktop"}.png'),full_page=False)
  page.close()
 browser.close()
print('PASS v0.9.7: 6 lesson scripts, SVGs, quiz, notes and session checklists; mobile and desktop; no JS errors')
