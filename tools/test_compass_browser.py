from pathlib import Path
from playwright.sync_api import sync_playwright
import threading,http.server,socketserver,os,time,subprocess
root=Path(__file__).resolve().parent.parent
class H(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
os.chdir(root)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),H)
threading.Thread(target=server.serve_forever,daemon=True).start()
url='http://127.0.0.1:'+str(server.server_address[1])
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in [(390,844),(1365,900)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(url+'/kurskompass.html#1.03-B',wait_until='load')
  assert page.locator('main h1').inner_text().startswith('Ohmsches Gesetz'),page.locator('main h1').inner_text()
  assert page.locator('img.visual').evaluate('(img)=>img.complete && img.naturalWidth>0')
  assert page.locator('.question').count()==3
  page.get_by_text('Antwort und Begründung anzeigen').first.click()
  assert page.locator('#answer-0').is_visible()
  page.locator('#journal').fill('Testnotiz behalten!')
  page.reload();assert page.locator('#journal').input_value()=='Testnotiz behalten!'
  page.goto(url+'/kurskompass.html#N-S01',wait_until='load')
  assert page.locator('main h1').count()==1
  assert page.locator('img.visual').evaluate('(img)=>img.complete && img.naturalWidth>0')
  page.screenshot(path=str(root/('preview_v093_mobile.png' if width<500 else 'preview_v093_desktop.png')),full_page=False)
  assert not errors,errors
  page.close()
 # Main app still running
 page=browser.new_page(viewport={'width':1365,'height':850});errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
 page.goto(url+'/index.html',wait_until='load');page.wait_for_timeout(1800)
 assert page.locator('a[href="./kurskompass.html"]').count()==1
 assert 'ELEKTRO' in page.locator('body').inner_text()
 assert not errors,errors
 print('OK – iPhone viewport + desktop, lessons from both sources, SVG, quiz answers, local journal persistence; main app loaded.')
 browser.close()
server.shutdown()
