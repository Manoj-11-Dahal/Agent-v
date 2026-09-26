#!/usr/bin/env python3
"""Validate all Kali reference records and generated text views; execute no Kali tools."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv, hashlib, json, re, subprocess, sys
import yaml
from kali_library import catalog, content, guide, read, details
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'kali-tools';CACHE=ROOT/'_catalog/.cache/kali'
def main():
 data=catalog();skills=data['skills'];sources=data['_sources'];packages=data['_packages'];names={r['name'] for r in skills}
 assert len(names)==len(skills)==3339
 assert len(sources)==780 and len(packages)==1489
 assert sum(r['kind']=='command' for r in skills)==2766
 assert sum(r['kind']=='package' for r in skills)==573
 assert all(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) and len(name)<=64 for name in names)
 command_counts=Counter(r['package'] for r in skills if r['kind']=='command')
 doc_keys=set();max_guide=0;quote_counts=Counter()
 for r in skills:
  assert r['source'] in sources and r['package'] in packages
  p=packages[r['package']];assert p['source']==r['source']
  if r['kind']=='command':
   doc_keys.add((r['source'],r['anchor']));c=content(r)
   assert len(c['help'])==r['helpCharacters'];quote_counts[r['source']]+=len(c['description'].split())
   if r['mode']=='reference-only':assert not c['help']
  else:assert p['commandCount']==0 and r['contentOffset'] is None and r['command'] is None
  g=guide(r['name']);max_guide=max(max_guide,len(g.encode()));lines=g.splitlines()
  end=next(i for i,line in enumerate(lines[1:],1) if line=='---');meta=yaml.safe_load('\n'.join(lines[1:end]))
  assert meta['name']==r['name'] and meta['source']==sources[r['source']]['url']+'#'+r['anchor']
  assert all(h in g for h in ['## Preflight contract','## Verification and interpretation','## Stop, evidence and cleanup'])
  for f in details(r['name'])['files']:
   raw=read(r['name'],f['path']).encode();assert len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256']
 for p in packages.values():
  assert p['commandCount']==command_counts[p['id']]
  if 'Short attributed description excerpt: ' in p['description']:quote_counts[p['source']]+=len(p['description'].split('Short attributed description excerpt: ',1)[1].split())
 assert max(quote_counts.values())<=60
 assert max_guide<100000
 with (BASE/'skills.csv').open(newline='') as f:reader=csv.DictReader(f);cols=reader.fieldnames;rows=list(reader)
 assert len(cols)==26 and len(rows)==3339 and {r['name'] for r in rows}==names
 for row in rows:
  r=data['_skills'][row['name']];p=packages[r['package']]
  assert row['sourceTool']==r['source'] and row['binaryPackage']==p['name']
  assert json.loads(row['dependencies'])==p['dependencies']
  assert json.loads(row['documentedLongOptions'])==r['documentedLongOptions']
  for value in row.values():assert not value.lstrip(' \t\r\n').startswith(('=','+','-','@'))
 cache_status='not present; recorded collection coverage retained'
 if CACHE.exists():
  from bs4 import BeautifulSoup
  seen_commands=set();seen_packages=set()
  for source in sources.values():
   raw=(CACHE/(source['id']+'.html')).read_bytes();assert hashlib.sha256(raw).hexdigest()==source['pageSha256']
   soup=BeautifulSoup(raw,'html.parser');info=soup.find(id='packages-info')
   seen_commands.update((source['id'],h['id']) for h in info.find_all('h5'))
   seen_packages.update(source['id']+'::'+h['id'] for h in info.find_all('h3'))
  assert seen_commands==doc_keys and seen_packages==set(packages)
  listing=BeautifulSoup((CACHE/'all-tools.html').read_bytes(),'html.parser');listed=set()
  for a in listing.find_all('a',href=True):
   if not a.get('title','').endswith(' command'):continue
   m=re.fullmatch(r'https://www\.kali\.org/tools/([^/]+)/#(.+)',a['href']);assert m
   key=(m[1],m[2]);assert key in doc_keys;listed.add(key)
  assert len(listed)==2342
  cache_status='all 780 page hashes, 2766 command headings, 1489 package headings and explicit directory links verified'
 cli=[sys.executable,str(ROOT/'_catalog/find.py')]
 def call(*args):return json.loads(subprocess.check_output(cli+list(args),text=True))
 assert call('--category','kali-tools','--limit','1')['matches']==3339
 assert call()['skills']==json.loads((ROOT/'_catalog/index.json').read_text())['discoverableSkillCount']
 assert call('--category','kali-tools','--tool','nmap','--limit','100')['matches']>0
 chosen='kali-nmap-nmap';out=call('--skill',chosen,'--read','SKILL.md');assert out['storage']=='bundle' and out['content']==guide(chosen)[:16000]
 assert call('--skill',chosen,'--read','HELP.txt')['content']==read(chosen,'HELP.txt')[:16000]
 assert call('--skill',chosen,'--outline')['outline']
 raw=subprocess.check_output(cli+['--skill',chosen,'--read','SKILL.md','--raw','--max-chars','100000'],text=True);assert raw==guide(chosen)
 blocked=subprocess.run(cli+['--skill',chosen,'--read','SKILL.md','--raw','--max-chars','10'],capture_output=True,text=True);assert blocked.returncode==2 and not blocked.stdout
 bad=subprocess.run(cli+['--skill',chosen,'--read','../index.json'],capture_output=True,text=True);assert bad.returncode==2
 # Verify no loose Kali command folders were secretly created.
 assert not list(BASE.glob('*/SKILL.md'))
 report={'checkedAt':datetime.now(timezone.utc).isoformat(),'sourcePages':780,'binaryPackages':1489,'commandSkills':2766,'packageOnlySkills':573,'individuallyAddressableSkills':3339,'interfaceReferencesAvailable':sum(r['helpCharacters']>0 for r in skills),'referenceOnlyCommands':sum(r['mode']=='reference-only' for r in skills),'generatedViewsChecked':sum(2 if r['kind']=='command' else 1 for r in skills),'maximumGuideBytes':max_guide,'csvRows':len(rows),'csvColumns':len(cols),'sourceVerification':cache_status,'contentHashesVerified':True,'metadataAndNamesValidated':True,'globalSearchAndReadChecksPassed':True,'sourceExcerptsWithinBudget':True,'kaliToolsExecuted':False,'securityToolsInstalled':False,'storage':'plain JSON and JSONL; no loose SKILL.md folders for this collection','rendererSha256':hashlib.sha256((ROOT/'_catalog/kali_library.py').read_bytes()).hexdigest()}
 (BASE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
