#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from pathlib import Path
import time
R=Path(__file__).resolve().parent.parent
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(('127.0.0.1',0),lambda *a,**kw:Quiet(*a,directory=str(R),**kw));Thread(target=srv.serve_forever,daemon=True).start()
port=srv.server_address[1]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width in [390,1360]:
  page=browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto((R/'index.html').as_uri(),wait_until='domcontentloaded')
  page.wait_for_selector('.year-card',timeout=15000)
  if width==390:page.click('#hamb')
  page.locator('.year-card[data-year="1"]').click()
  page.locator('[data-module="1.03"]').first.click()
  page.locator('[data-lesson="1.03-B"]').first.click()
  page.locator('[data-tab="folien"]').first.click()
  assert page.locator('.studio-review').count()==1
  page.locator('.studio-review summary').click()
  assert 'Skript erreicht rechnerisch' in page.locator('.studio-review').inner_text()
  # Move into first conceptual slide and verify custom image.
  page.locator('[data-st="next"]').click()
  page.wait_for_selector('.studio-individual-figure img',timeout=10000)
  u=page.locator('.studio-individual-figure img').get_attribute('src')
  assert u=='./visuals/1.03-B.svg',u
  assert page.locator('.studio-individual-figure img').evaluate('(n)=>n.complete&&n.naturalWidth>0'), 'image not loaded'
  page.screenshot(path=str(R/f'preview_v092_{width}.png'),full_page=True)
  assert not errors,errors
  print('Viewport',width,'OK','picture',u,'JS errors',len(errors))
  page.close()
 browser.close()
srv.shutdown()
