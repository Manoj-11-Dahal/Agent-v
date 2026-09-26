#!/usr/bin/env python3
"""Build individually addressable Kali reference skills from collected public docs.
No tool installation, target requests, command evaluation, or skill execution.
"""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit
from collections import Counter
import csv, hashlib, json, re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];CACHE=ROOT/'_catalog/.cache/kali';DEST=ROOT/'kali-tools'
# These families get descriptive/defensive references, not deployable payload or evasion recipes.
RESTRICTED={'adaptixc2','armitage','backdoor-factory','beef-xss','covenant-kbx','empire','evilginx2','havoc','metasploit-framework','mimikatz','powersploit','shellter','sliver','starkiller','veil','unicorn-magic','av-evasion','pwncat','pwncat-cs'}
def dumps(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
def text(node):return node.get_text(' ',strip=True) if node else ''
def safe_cell(v):
 s=dumps(v) if not isinstance(v,str) else v
 return "'"+s if s.lstrip(' \t\r\n').startswith(('=','+','-','@')) or s.startswith(('\t','\r','\n')) else s

def sanitize_help(blocks,restricted):
 if restricted:return '', 'reference-only: operational transcript not republished for this high-risk tool family'
 signatures=[];synopses=[]
 for block in blocks:
  for line in block.splitlines():
   if re.match(r'(?i)^\s*(?:usage\s+)?examples?\b\s*[:\-]?',line):break
   usage=re.match(r'(?i)^\s*(?:usage|synopsis)\s*:\s*(.*)$',line)
   if usage and usage[1].strip():synopses.append(usage[1].strip())
   if not re.match(r'^\s*(?:-{1,2}[A-Za-z0-9?]|/[A-Za-z?])',line):continue
   signature=re.split(r'\s{2,}|\t',line.strip(),maxsplit=1)[0]
   parts=signature.split();safe=[]
   for token in parts:
    if token.startswith(('-', '/', '<', '[', '{', '=', '|')) or token.rstrip(',').isupper() or token.lower().rstrip(',') in {'file','filename','path','host','hostname','port','url','user','username','password','value','number','format','name','directory','seconds','interface','address','ip','target','count','command'}:safe.append(token)
    elif len(safe)==0:break
    else:break
   if safe:signatures.append(' '.join(safe))
 signatures=list(dict.fromkeys(signatures));synopses=list(dict.fromkeys(synopses))
 result='Extracted command-interface facts, not a verbatim manual or a tested invocation.\nCheck the official source for argument semantics, defaults and compatibility.\n'
 if synopses:result+='\nPublished synopsis patterns:\n'+'\n'.join(synopses)+'\n'
 if signatures:result+='\nObserved option signatures:\n'+'\n'.join(signatures)+'\n'
 return (result if signatures or synopses else ''), 'interface signatures extracted; explanatory prose, shell prompts and example recipes omitted' if signatures or synopses else 'no reliable interface signature extracted; consult the official source'

def main():
 collection=json.loads((CACHE/'collection.json').read_text());assert len(collection['results'])==collection['toolPages'] and not any(r['status']=='failed' for r in collection['results'])
 DEST.mkdir(exist_ok=True);sources=[];packages=[];skills=[];seen=set();content_file=DEST/'command-content.jsonl';lookup={}
 with content_file.open('wb') as content:
  for entry in collection['results']:
   slug=entry['slug'];quote_budget=[60];raw=(CACHE/(slug+'.html')).read_bytes();soup=BeautifulSoup(raw,'html.parser');main=soup.find('main');info=soup.find(id='packages-info');assert info is not None,slug
   maintext=text(main);version=re.search(r'\bversion:\s*(\S+)',maintext);arch=re.search(r'\barch:\s*(.*?)\s+(?:'+re.escape(slug)+r' Homepage|Homepage|Package Tracker)',maintext)
   cats=[text(a) for a in soup.select('#categories li a[href]')]
   metas=[text(a) for a in soup.select('#metapackages li a[href]')]
   links={}
   for a in (main or soup).find_all('a',href=True):
    label=text(a)
    if label.endswith('Homepage'):links['homepage']=a['href']
    elif label in ['Package Tracker','Source Code Repository']:links[label]=a['href']
   updated=re.search(r'Updated on:\s*([0-9A-Za-z-]+)',maintext)
   source={'id':slug,'url':entry['url'],'version':version[1] if version else '', 'architecture':arch[1] if arch else '', 'categories':list(dict.fromkeys(cats)),'metapackages':list(dict.fromkeys(metas)),'links':links,'updated':updated[1] if updated else '', 'pageSha256':hashlib.sha256(raw).hexdigest(),'retrievedAt':entry.get('fetchedAt',collection['collectedAt'])}
   sources.append(source);package=None;command=None
   def finish_command():
    nonlocal command
    if command is None:return
    restricted=slug in RESTRICTED
    help_text,help_policy=sanitize_help(command.pop('blocks'),restricted)
    original='\n\n'.join(command.pop('paragraphs')).strip()
    words=original.split();n=min(quote_budget[0],min(12,len(words)));quote_budget[0]-=n
    description=' '.join(words[:n])+('…' if n and n<len(words) else '') if n else ''
    payload={'description':description,'help':help_text,'helpPolicy':help_policy}
    b=(dumps(payload)+'\n').encode();offset=content.tell();content.write(b)
    display=command['command'];kind='command'
    stem=re.sub(r'[^a-z0-9]+','-',display.lower().replace('+','-plus-')).strip('-') or 'command'
    name=re.sub(r'[^a-z0-9]+','-',('kali-'+slug+'-'+stem).lower()).strip('-')
    if name in seen or len(name)>64:name=name[:51].rstrip('-')+'-'+hashlib.sha256((slug+'::'+command['anchor']).encode()).hexdigest()[:12]
    assert name not in seen;seen.add(name)
    option_names=sorted(set(re.findall(r'(?m)^\s*(?:-[A-Za-z0-9?],?\s*)?(--[A-Za-z0-9][\w-]*)',help_text)))
    short=description if description else 'Command '+display+' from Kali binary package '+package['name']+'; source project '+slug+'.'
    row={'name':name,'source':slug,'package':package['id'],'command':display,'anchor':command['anchor'],'kind':kind,'description':short,'mode':'reference-only' if restricted else 'bounded-authorized-use','helpPolicy':help_policy,'helpCharacters':len(help_text),'documentedLongOptions':option_names,'contentOffset':offset,'contentBytes':len(b),'contentSha256':hashlib.sha256(b).hexdigest()}
    skills.append(row);package['commandCount']+=1;lookup[(slug,command['anchor'])]=name;command=None
   def finish_package():
    nonlocal package
    if package is None:return
    finish_command();original=' '.join(package.pop('paragraphs')).strip();words=original.split();n=min(quote_budget[0],min(12,len(words)));quote_budget[0]-=n
    excerpt=' '.join(words[:n])+('…' if n and n<len(words) else '') if n else ''
    package['summary']=excerpt or 'Binary package '+package['name']+' from Kali source project '+slug+'.'
    package['description']='Binary package '+package['name']+' belongs to source project '+slug+'. Kali lists '+str(package['commandCount'])+' command headings and '+str(len(package['dependencies']))+' direct package dependencies. '+('Short attributed description excerpt: '+excerpt if excerpt else 'No descriptive quotation retained; follow the source link for the full package documentation.')
    if package['commandCount']==0:
     name=re.sub(r'[^a-z0-9]+','-',('kali-'+slug+'-'+package['name']+'-package').lower()).strip('-')
     if len(name)>64:name=name[:51].rstrip('-')+'-'+hashlib.sha256(package['id'].encode()).hexdigest()[:12]
     assert name not in seen;seen.add(name)
     skills.append({'name':name,'source':slug,'package':package['id'],'command':None,'anchor':package['anchor'],'kind':'package','description':package['summary'],'mode':'package-reference','helpPolicy':'No command heading is published for this binary package. No executable is invented.','helpCharacters':0,'documentedLongOptions':[],'contentOffset':None,'contentBytes':0,'contentSha256':None})
    packages.append(package);package=None
   for node in info.children:
    tag=getattr(node,'name',None)
    if tag=='h3':
     finish_package();label=text(node);package={'id':slug+'::'+node.get('id',label),'source':slug,'name':label,'anchor':node.get('id',label),'paragraphs':[],'summary':'','dependencies':[],'installedSize':'','installDeclaration':'','commandCount':0}
    elif tag=='h5':
     assert package is not None,(slug,text(node));finish_command();command={'command':text(node),'anchor':node.get('id',text(node)),'paragraphs':[],'blocks':[]}
    elif package is not None:
     if tag=='pre' and command is not None:command['blocks'].append(node.get_text())
     elif tag=='details' and 'Dependencies' in text(node):package['dependencies']=[text(li) for li in node.find_all('li')]
     elif tag in {'p','ul','ol','div','blockquote'}:
      value=text(node)
      if 'Installed size:' in value or 'How to install:' in value:
       codes=[text(c) for c in node.find_all('code')]
       if codes:package['installedSize']=codes[0]
       if len(codes)>1:package['installDeclaration']=codes[1]
      elif value:
       if command is not None:command['paragraphs'].append(value)
       else:package['paragraphs'].append(value);package['summary']=package['paragraphs'][0]
   finish_package()
   assert any(s['source']==slug for s in skills),slug
 index_soup=BeautifulSoup((CACHE/'all-tools.html').read_bytes(),'html.parser');expected=[];unmatched=[]
 for a in index_soup.find_all('a',href=True):
  if not a.get('title','').endswith(' command'):continue
  u=urlsplit(a['href']);m=re.match(r'^/tools/([^/]+)/$',u.path)
  if m:
   key=(m[1],u.fragment);expected.append(key)
   if key not in lookup:unmatched.append({'source':m[1],'anchor':u.fragment,'label':text(a)})
 assert not unmatched,unmatched[:20]
 inline=[]
 for span in index_soup.find_all('span',title=True):
  m=re.fullmatch(r'Includes (.+) command',span['title'])
  if not m:continue
  a=span.find_parent('a',href=True);slug=urlsplit(a['href']).path.strip('/').split('/')[-1]
  matched=[s for s in skills if s['source']==slug and s['command']==m[1]]
  assert matched,(slug,m[1]);inline.append((slug,m[1]))
 table={name:sorted(set().union(*(r.keys() for r in rows))) for name,rows in [('sources',sources),('packages',packages),('skills',skills)]}
 data={'schemaVersion':1,'storage':'columnar-json-and-byte-addressed-jsonl','generatedAt':datetime.now(timezone.utc).isoformat(),'listingUrl':collection['listingUrl'],'sourcePages':len(sources),'binaryPackages':len(packages),'commandSkills':sum(s['kind']=='command' for s in skills),'packageOnlySkills':sum(s['kind']=='package' for s in skills),'skillCount':len(skills),'explicitListingCommandLinks':len(set(expected)),'inlineListingCommands':len(set(inline)),'contentFile':'command-content.jsonl','rowSchemas':table,'sources':[[r.get(k) for k in table['sources']] for r in sources],'packages':[[r.get(k) for k in table['packages']] for r in packages],'skills':[[r.get(k) for k in table['skills']] for r in skills], 'notes':['Source-derived generated references, not individually hand-audited or executed.','Metadata and interface signatures are extracted as technical facts. Short description quotations are limited across each source page and attributed; full explanatory prose is not mirrored. Package software licenses are not inferred.','Operational recipes from the separate Tool Documentation section are not copied. High-risk families are descriptive/defensive references only.','All original tool pages and explicit/inline listing commands were mapped; package-only records cover binary packages without commands.','Published help and version metadata can differ; verify the actual installed build separately.','Each named skill can be read individually through _catalog/find.py. Standard folder-based loaders require explicit export of selected guides.']}
 (DEST/'index.json').write_text(dumps(data)+'\n')
 sm={s['id']:s for s in sources};pm={p['id']:p for p in packages}
 cols=['name','kind','sourceTool','binaryPackage','command','description','mode','version','architecture','categories','metapackages','packageDescription','dependencies','installedSize','installDeclaration','documentedLongOptions','helpCharacters','helpPolicy','sourceUrl','sourceUpdated','pageSha256','retrievedAt','homepage','contentOffset','contentBytes','contentSha256']
 with (DEST/'skills.csv').open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=cols);writer.writeheader()
  for s in skills:
   p=pm[s['package']];source=sm[s['source']]
   row={'name':s['name'],'kind':s['kind'],'sourceTool':s['source'],'binaryPackage':p['name'],'command':s['command'] or '', 'description':s['description'],'mode':s['mode'],'version':source['version'],'architecture':source['architecture'],'categories':source['categories'],'metapackages':source['metapackages'],'packageDescription':p['description'],'dependencies':p['dependencies'],'installedSize':p['installedSize'],'installDeclaration':p['installDeclaration'],'documentedLongOptions':s['documentedLongOptions'],'helpCharacters':s['helpCharacters'],'helpPolicy':s['helpPolicy'],'sourceUrl':source['url']+'#'+s['anchor'],'sourceUpdated':source['updated'],'pageSha256':source['pageSha256'],'retrievedAt':source['retrievedAt'],'homepage':source['links'].get('homepage',''),'contentOffset':s['contentOffset'],'contentBytes':s['contentBytes'],'contentSha256':s['contentSha256']}
   writer.writerow({k:safe_cell(v) if v is not None else '' for k,v in row.items()})
 report={k:data[k] for k in ['sourcePages','binaryPackages','commandSkills','packageOnlySkills','skillCount','explicitListingCommandLinks','inlineListingCommands']};report['collectionFailures']=0;report['unmatchedListingCommands']=unmatched;report['csvColumns']=cols
 (DEST/'coverage.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
