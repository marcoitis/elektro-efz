#!/usr/bin/env python3
"""Mobile+desktop DOM smoke tests for all six v0.9.5 long lessons (no network)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64
R=Path(__file__).resolve().parent.parent
IDS={'1.09-A':'Elektrische Felder','1.09-B':'Magnetfelder','1.09-C':'RC-Zeitkonstante','1.10-A':'Periodendauer','1.10-B':'Effektivwert','1.10-C':'Energiewandlung'}
html=(R/'kurskompass.html').read_text('utf8')
for lid in IDS:
 svg=(R/'learning-visuals'/(lid+'.svg')).read_bytes()
 html=html.replace('./learning-visuals/'+lid+'.svg','data:image/svg+xml;base64,'+base64.b64encode(svg).decode())
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in ((390,844),(1280,900)):
  page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='load')
  for lid,topic in IDS.items():
   page.evaluate('(id)=>show(id)',lid)
   assert topic.lower() in page.locator('main h1').inner_text().lower(),lid
   assert page.locator('.question').count()==3,lid
   assert page.locator('details.long-lesson').count()==1,lid
   page.locator('details.long-lesson summary').click()
   assert page.locator('.full-script').is_visible(),lid
   assert len(page.locator('.full-script').inner_text())>11000,lid
   assert page.locator('img.visual').evaluate('(im)=>im.complete && im.naturalWidth>0'),lid
   page.locator('.question button[data-answer="0"]').first.click()
   assert page.locator('#answer-0').is_visible(),lid
  assert not errors,errors
  page.evaluate("show('1.09-C')")
  page.screenshot(path=str(R/f'preview_v095_{"mobile" if w<500 else "desktop"}.png'),full_page=False)
  page.close()
 browser.close()
print('PASS v0.9.5 browser: 6 manuscript lessons, 6 SVG images, 3 quiz answers each, mobile+desktop, no JavaScript errors')
