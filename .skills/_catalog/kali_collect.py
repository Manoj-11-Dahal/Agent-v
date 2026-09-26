#!/usr/bin/env python3
"""Collect public Kali documentation only; never install or execute Kali tools."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib, json, re, threading, time, urllib.request, urllib.error
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];CACHE=ROOT/'_catalog/.cache/kali';CACHE.mkdir(parents=True,exist_ok=True)
UA='SkillLibraryDocumentationReview/1.0';lock=threading.Lock();last=[0.0]
def retrieve(slug):
 path=CACHE/(slug+'.html');url='https://www.kali.org/tools/'+slug+'/'
 if path.exists():return {'slug':slug,'url':url,'status':'cached','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 for attempt in range(4):
  try:
   with lock:
    delay=max(0,.25-(time.monotonic()-last[0]));time.sleep(delay);last[0]=time.monotonic()
   req=urllib.request.Request(url,headers={'User-Agent':UA})
   with urllib.request.urlopen(req,timeout=45) as response:
    raw=response.read();status=response.status
   if b'packages-and-binaries' not in raw and slug!='all-tools':raise ValueError('Expected tool-documentation marker not present')
   path.write_bytes(raw)
   return {'slug':slug,'url':url,'status':'fetched','httpStatus':status,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'fetchedAt':datetime.now(timezone.utc).isoformat()}
  except Exception as e:
   if attempt==3:return {'slug':slug,'url':url,'status':'failed','error':str(e)}
   time.sleep(2**attempt)
def main():
 result=retrieve('all-tools');assert result['status']!='failed',result
 soup=BeautifulSoup((CACHE/'all-tools.html').read_bytes(),'html.parser')
 slugs=sorted({m[1] for a in soup.find_all('a',href=True) if (m:=re.fullmatch(r'https://www\.kali\.org/tools/([^/#]+)/',a['href'])) and m[1] not in {'all-tools','top-100'}})
 print('Collecting',len(slugs),'public documentation pages; up to four requests per second.',flush=True)
 results=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  jobs={pool.submit(retrieve,slug):slug for slug in slugs}
  for future in as_completed(jobs):
   result=future.result();results.append(result)
   if len(results)%25==0 or result['status']=='failed':print('Progress',len(results),'/',len(slugs),'failures',sum(r['status']=='failed' for r in results),flush=True)
 report={'listingUrl':'https://www.kali.org/tools/all-tools/','collectedAt':datetime.now(timezone.utc).isoformat(),'toolPages':len(slugs),'results':sorted(results,key=lambda r:r['slug'])}
 (CACHE/'collection.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Collection finished:',len(results),'pages;',sum(r['status']=='failed' for r in results),'failures.',flush=True)
if __name__=='__main__':main()
