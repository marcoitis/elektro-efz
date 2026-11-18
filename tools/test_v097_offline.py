#!/usr/bin/env python3
"""Local Chrome smoke test for static standalone and service worker cache; not device/Piper testing."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import subprocess,time,os
ROOT=Path(__file__).resolve().parent.parent
preview=ROOT.parent/'Elektro_EFZ_v0.9.7_Unterricht_Offline_Vorschau.html'
s=preview.read_text('utf8')
assert s.count('data:image/svg+xml;base64,')>=178
assert 'v0.9.7' in s
port=8769
server=subprocess.Popen(['python','-m','http.server',str(port),'--bind','127.0.0.1','--directory',str(ROOT/'dist-v097-probe')],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
try:
 time.sleep(1)
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  page=browser.new_page()
  page.set_content(s,wait_until='load')
  page.evaluate("show('1.08-B')")
  assert page.locator('details.long-lesson').count()==1
  assert page.locator('img.visual').evaluate('(im)=>im.complete && im.naturalWidth>0')
  page.close()
  context=browser.new_context(service_workers='allow')
  page=context.new_page()
  issues=[];page.on('pageerror',lambda err:issues.append(str(err)))
  url=f'http://127.0.0.1:{port}/index.html'
  page.goto(url,wait_until='load',timeout=30000)
  # IndexedDB and page UI use current path and pass through SW precache asynchronously.
  assert 'Elektro' in page.title()
  page.evaluate("() => navigator.serviceWorker.ready.then(()=>true)")
  # Wait until the service worker has installed the new cache and it is populated.
  page.wait_for_function("() => caches.has('elektro-efz-shell-v097-montage-measurement-1')",timeout=30000)
  count=page.evaluate("async () => (await caches.open('elektro-efz-shell-v097-montage-measurement-1')).keys().then(x=>x.length)")
  assert count>=360,count
  context.set_offline(True)
  page.reload(wait_until='load',timeout=30000)
  assert 'Elektro' in page.title()
  assert not issues,issues
  print('PASS: standalone 178 embedded SVGs; worker cached',count,'files; offline Chromium reload successful; no JavaScript errors')
  context.close();browser.close()
finally:
 server.terminate()
 try:server.wait(timeout=5)
 except subprocess.TimeoutExpired:server.kill()
