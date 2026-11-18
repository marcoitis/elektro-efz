#!/usr/bin/env python3
"""Network-free browser DOM smoke tests. Uses set_content because navigation is sandbox-blocked."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64, re
R=Path(__file__).resolve().parent.parent
html=(R/'kurskompass.html').read_text('utf8')
for lid in ['1.03-A','1.04-A','1.04-B','N-S01']:
 svg=(R/'learning-visuals'/(lid+'.svg')).read_bytes()
 html=html.replace('./learning-visuals/'+lid+'.svg','data:image/svg+xml;base64,'+base64.b64encode(svg).decode())
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in [(390,844),(1280,900)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='load')
  for lid,titlepart in [('1.03-A','Spannung'),('1.04-A','Serien'),('1.04-B','Kirchhoff'),('N-S01','Verantwortung')]:
   page.evaluate('(id)=>show(id)',lid)
   assert titlepart.lower() in page.locator('main h1').inner_text().lower(),(lid,page.locator('main h1').inner_text())
   assert page.locator('.question').count()==3,lid
   page.locator('.question button[data-answer="0"]').click()
   assert page.locator('#answer-0').is_visible(),lid
   if lid!='N-S01':
    assert page.locator('details.long-lesson').count()==1,lid
    page.locator('details.long-lesson summary').click()
    assert page.locator('.full-script').is_visible()
    assert len(page.locator('.full-script').inner_text())>12000,lid
   assert page.locator('img.visual').evaluate('(im)=>im.complete && im.naturalWidth>0'),lid
  if errors:raise AssertionError(errors)
  page.evaluate("show('1.04-B')")
  page.screenshot(path=str(R/f'preview_v094_{"mobile" if width<500 else "desktop"}.png'),full_page=False)
  page.close()
 browser.close()
print('Browser tests PASS: 390 px + 1280 px, 3 long manuscripts, 1 norm lesson, quiz answers, SVG images; no page errors')
