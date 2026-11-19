#!/usr/bin/env python3
"""Static CI web server with HTTP 206 byte ranges, like production MP3 CDNs.

SimpleHTTPRequestHandler on Python 3.11 returns a full 200 response for range
requests. WebKit's HTML5 media engine requires correct 206 ranges for seeking
within MP3. Use this server in browser tests to validate real media controls.
"""
import argparse
import mimetypes
import os
import re
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial

class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        filepath=self.translate_path(self.path)
        if not os.path.isfile(filepath):
            return super().send_head()
        data=open(filepath,'rb')
        try:
            length=os.fstat(data.fileno()).st_size
            value=self.headers.get('Range','')
            # Browsers request single byte ranges, including "bytes=0-".
            m=re.fullmatch(r'bytes=(\d*)-(\d*)',value)
            if not m:
                data.close()
                return super().send_head()
            a,b=m.groups()
            if a:
                start=int(a)
                end=int(b) if b else length-1
            elif b:
                start=max(0,length-int(b))
                end=length-1
            else:
                data.close()
                return super().send_head()
            if start>=length or end<start or length==0:
                self.send_response(416)
                self.send_header('Content-Range',f'bytes */{length}')
                self.send_header('Content-Length','0')
                self.end_headers()
                data.close()
                return None
            end=min(end,length-1)
            data.seek(start)
            self.send_response(206)
            self.send_header('Content-type',self.guess_type(filepath))
            self.send_header('Accept-Ranges','bytes')
            self.send_header('Content-Range',f'bytes {start}-{end}/{length}')
            self.send_header('Content-Length',str(end-start+1))
            self.send_header('Cache-Control','no-cache')
            self.end_headers()
            self._range_remaining=end-start+1
            return data
        except Exception:
            data.close()
            raise
    def copyfile(self,source,outputfile):
        if not hasattr(self,'_range_remaining'):
            return super().copyfile(source,outputfile)
        remaining=self._range_remaining
        while remaining>0:
            block=source.read(min(65536,remaining))
            if not block:break
            try:outputfile.write(block)
            except BrokenPipeError:break
            remaining-=len(block)
    def end_headers(self):
        # Even for 200 metadata responses, advertise range capability.
        if not hasattr(self,'_range_remaining'):
            self.send_header('Accept-Ranges','bytes')
        super().end_headers()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',default='dist')
    p.add_argument('--port',type=int,default=8787)
    a=p.parse_args()
    handler=partial(Handler,directory=a.root)
    with ThreadingHTTPServer(('127.0.0.1',a.port),handler) as srv:
        print(f'HTTP Range server: {a.root} :{a.port}',flush=True)
        srv.serve_forever()
if __name__=='__main__':main()
