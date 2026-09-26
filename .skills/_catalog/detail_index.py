"""Detailed read-only enrichment and normalized CSV exports for build_index.py.
Only library data is read; no skill code, commands, or external links are executed.
"""
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit, unquote
import csv, hashlib, json, math, mimetypes, re
import yaml

METHODS = {
 'content': 'Hashes and text statistics are computed from available file bytes. Missing references have historical sizes but null hashes and content statistics.',
 'markdown': 'Line-based extraction of ATX headings, fenced code blocks, inline links, link definitions and HTTP(S) mentions; not a complete CommonMark parser. Line numbers are 1-based and inclusive.',
 'keywords': 'Up to 48 automatically selected TF-IDF terms from entry-point body text; retrieval hints, not declared capabilities or exhaustive full-text indexing.',
 'references': 'Local destinations checked for presence within the library only. External URLs, fragments and dynamic destinations are not validated or fetched.',
 'metadata': 'All YAML frontmatter fields retained. YAML-specific dates/sets and non-finite numbers normalized to JSON-compatible values. No missing authors, versions, licenses or origins are invented.',
 'readiness': 'No-known-missing-files means inventory presence only; not runtime readiness, permission approval, security certification, or a completeness guarantee against upstream.',
 'csv': 'UTF-8, RFC-style CSV quoting; lists/objects encoded as compact JSON. Dangerous spreadsheet strings are prefixed with an apostrophe. The decoded JSON view preserves exact original string values; the manifest defines typed CSV decoding and any necessary overrides.'
}
STOP=set('the and for that this with from have will your into when which are use using used can not but all any you should must these those then their they only also each more some such than through about after before under over has was were been being how what where does do its our out per new return returns example examples code file files true false none null skill skills following include including set get see run make need needs please default'.split())
def j(v): return json.dumps(v,ensure_ascii=False,separators=(',',':'),allow_nan=False)
def normal(v):
 if isinstance(v,dict):return {str(k):normal(x) for k,x in v.items()}
 if isinstance(v,(list,tuple,set)):return [normal(x) for x in v]
 if isinstance(v,float) and not math.isfinite(v):return str(v)
 if v is None or isinstance(v,(str,int,float,bool)):return v
 return str(v)
def leaves(v,p=''):
 if isinstance(v,dict) and v:
  for k,x in v.items():yield from leaves(x,p+'/'+k.replace('~','~0').replace('/','~1'))
 else:yield p,v

def role(path):
 p=Path(path);s=p.suffix.lower();parts=set(p.parts)
 if path=='SKILL.md':return 'entrypoint'
 if p.name.lower().startswith(('license','copying','notice')):return 'license-or-notice'
 if s in {'.py','.sh','.bash','.js','.ts','.mjs','.cjs','.ps1','.bat','.cmd'}:return 'script-or-source'
 if parts & {'references','reference','docs','documentation'}:return 'reference'
 if s in {'.png','.jpg','.jpeg','.svg','.webp','.gif','.ico','.mp3','.wav','.mp4','.glb','.gltf','.blend','.fbx','.obj','.stl','.ttf','.woff','.woff2'}:return 'asset'
 if s in {'.json','.yaml','.yml','.toml','.ini','.cfg','.conf','.xml'}:return 'configuration-or-data'
 if s in {'.md','.txt','.rst','.html','.pdf'}:return 'document'
 return 'other'

def parse_doc(text,body_start):
 lines=text.splitlines(keepends=True);headings=[];blocks=[];fence=None;masked=set()
 for i,line in enumerate(lines,1):
  if i<body_start:continue
  m=re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$',line.rstrip('\r\n'))
  if fence:
   masked.add(i)
   if m and m[1][0]==fence['char'] and len(m[1])>=fence['length'] and not m[2].strip():
    block=fence['block'];block.update(endLine=i,closed=True)
    payload=''.join(lines[block['startLine']:i-1]).encode('utf-8')
    block.update(contentBytes=len(payload),contentSha256=hashlib.sha256(payload).hexdigest());blocks.append(block);fence=None
   continue
  if m:
   masked.add(i);info=m[2].strip()
   fence={'char':m[1][0],'length':len(m[1]),'block':{'order':len(blocks)+1,'language':info.split()[0] if info else '', 'info':info,'startLine':i}}
   continue
  h=re.match(r'^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$',line.rstrip('\r\n'))
  if h:headings.append({'order':len(headings)+1,'level':len(h[1]),'title':h[2],'startLine':i})
 if fence:
  block=fence['block'];payload=''.join(lines[block['startLine']:]).encode('utf-8')
  block.update(endLine=len(lines),closed=False,contentBytes=len(payload),contentSha256=hashlib.sha256(payload).hexdigest());blocks.append(block)
 stack=[]
 for h in headings:
  while stack and stack[-1]['level']>=h['level']:stack.pop()['endLine']=h['startLine']-1
  h['parentOrder']=stack[-1]['order'] if stack else None;stack.append(h)
 for h in stack:h['endLine']=len(lines)
 refs=[];seen=set()
 for i,line in enumerate(lines,1):
  if i<body_start:continue
  hits=[]
  if i not in masked:
   for m in re.finditer(r'(!?)\[([^\]\n]*)\]\(\s*(<[^>]*>|[^\s)]+)(?:\s+[^)]*)?\)',line):
    hits.append((m.start(),'image' if m[1] else 'markdown-link',m[2],m[3].strip('<>')))
   m=re.match(r'^ {0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)',line)
   if m:hits.append((m.start(),'link-definition',m[1],m[2].strip('<>')))
  for m in re.finditer(r'https?://[^\s<>`"\]\)]+',line):hits.append((m.start(),'url-mention','',m[0].rstrip('.,;')))
  for col,kind,label,dest in sorted(hits,key=lambda x:(x[0],x[1]=='url-mention')):
   if (i,dest) in seen:continue
   seen.add((i,dest));refs.append({'order':len(refs)+1,'line':i,'column':col+1,'kind':kind,'label':label,'target':dest,'insideCodeBlock':i in masked})
 return headings,blocks,refs

def resolve_ref(ref,directory,root,known_missing):
 target=ref['target'];ref.update(resolvedPath=None,availability='unchecked')
 if not target or target.startswith('#'):ref['availability']='fragment-unchecked';return
 if any(v in target for v in ('${','{{','<','>','`')):ref['availability']='dynamic-unchecked';return
 try:u=urlsplit(target)
 except ValueError:ref['availability']='unparsed';return
 if u.scheme or u.netloc:ref['availability']='external-unchecked';return
 try:
  path=(directory/unquote(u.path)).resolve()
  if not path.is_relative_to(root):ref['availability']='outside-library';return
  rel=path.relative_to(root).as_posix();ref['resolvedPath']=rel
  ref['availability']='available-file' if path.is_file() else 'available-directory' if path.is_dir() else 'missing-indexed' if rel in known_missing else 'not-found'
 except (ValueError,OSError):ref['availability']='unparsed'

def enrich(records,root):
 root=root.resolve();known_missing={r['directory']+'/'+f['path'] for r in records for f in r['files'] if f['storage']=='missing'}
 terms={};df=Counter()
 for r in records:
  directory=root/r['directory'];raw=(root/r['path']).read_bytes();text=raw.decode('utf-8');lines=text.splitlines(keepends=True)
  assert lines[0].strip()=='---',r['path']
  end=next(i for i,line in enumerate(lines[1:],1) if line.strip()=='---');body_start=end+2
  meta=normal(yaml.safe_load(''.join(lines[1:end])))
  r.update(id='skill-'+hashlib.sha256(r['name'].encode()).hexdigest()[:16],absolutePath=str(root/r['path']),frontmatter=meta,metadataFields=sorted(p for p,v in leaves(meta)),inventoryStatus='reference-incomplete' if r['missing'] else 'no-known-missing-files')
  heads,blocks,refs=parse_doc(text,body_start)
  for ref in refs:resolve_ref(ref,directory,root,known_missing)
  r.update(outline=heads,codeBlocks=blocks,references=refs,headings=[h['title'] for h in heads])
  r['document']={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'characters':len(text),'lines':len(lines),'words':len(re.findall(r'\S+',text)),'bodyStartLine':body_start,'frontmatterStartLine':2,'frontmatterEndLine':end,'title':heads[0]['title'] if heads else '', 'sectionCount':len(heads),'codeBlockCount':len(blocks),'referenceCount':len(refs),'codeLanguages':dict(Counter(b['language'] or 'unspecified' for b in blocks))}
  bag=Counter(t.casefold().strip('./-') for t in re.findall(r'[^\W_][\w.+#/-]{2,47}', ''.join(lines[end+1:]),flags=re.UNICODE))
  bag=Counter({t:n for t,n in bag.items() if t not in STOP and len(t)>2 and not t.isnumeric() and not re.fullmatch(r'[a-f0-9]{16,}',t)})
  terms[r['name']]=bag;df.update(bag.keys())
  for f in r['files']:
   f.update(libraryPath=r['directory']+'/'+f['path'],extension=Path(f['path']).suffix.lower(),role=role(f['path']),mimeType=mimetypes.guess_type(f['path'])[0] or 'application/octet-stream',available=f['storage']!='missing',sha256=None,encoding=None,lines=None,words=None,characters=None,executableBit=None,contentKind='unavailable')
   f['sizeSource']='historical-archive-inventory' if not f['available'] else 'current-file-bytes'
   if f['storage']=='file':
    p=directory/f['path'];assert p.resolve().is_relative_to(root),str(p)
    b=p.read_bytes();f.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),executableBit=bool(p.stat().st_mode & 0o111))
    try:
     st=b.decode('utf-8')
     if '\x00' in st:raise UnicodeDecodeError('utf-8',b,0,1,'NUL byte')
     f.update(encoding='utf-8',contentKind='text',lines=len(st.splitlines()),words=len(re.findall(r'\S+',st)),characters=len(st))
    except UnicodeDecodeError:f['contentKind']='binary-or-non-utf8'
   elif f['storage']=='zip':raise ValueError('Archive content enrichment requires an explicit implementation; no archive is currently retained.')
  available=[f for f in r['files'] if f['available']]
  r['inventory']={'availableBytes':sum(f['bytes'] for f in available),'missingHistoricalBytes':sum(f['bytes'] for f in r['files'] if not f['available']),'availableTextFiles':sum(f['contentKind']=='text' for f in available),'availableBinaryOrNonUtf8Files':sum(f['contentKind']=='binary-or-non-utf8' for f in available),'extensions':dict(Counter(f['extension'] or '(none)' for f in r['files'])),'roles':dict(Counter(f['role'] for f in r['files'])),'availableContentFingerprint':hashlib.sha256(''.join(f['path']+'\0'+f['sha256']+'\n' for f in available).encode()).hexdigest()}
  r['referenceStatusCounts']=dict(Counter(v['availability'] for v in refs))
  r['metadataStatus']={'fieldCount':len(r['metadataFields']),'authorDeclared':bool(r['author']),'versionDeclared':bool(r['version']),'licenseDeclared':bool(r['license']),'sourceTracking':'declared-only; previous lock removed','warningCoverage':'partial historical installer observations; not re-audited'}
 for r in records:
  scores={t:(1+math.log(n))*math.log(1+len(records)/(1+df[t])) for t,n in terms[r['name']].items()}
  r['searchKeywords']=sorted(scores,key=lambda t:(-scores[t],t))[:48]
 return {'availableFiles':sum(r['availableFileCount'] for r in records),'missingFiles':sum(r['missingCount'] for r in records),'availableBytes':sum(r['inventory']['availableBytes'] for r in records),'missingHistoricalBytes':sum(r['inventory']['missingHistoricalBytes'] for r in records),'sections':sum(len(r['outline']) for r in records),'codeBlocks':sum(len(r['codeBlocks']) for r in records),'references':sum(len(r['references']) for r in records),'hashAlgorithm':'SHA-256','methods':METHODS}

BASE=['id','name','category','categoryTitle','directory','path','absolutePath','description','tags','author','version','license','compatibility','declaredSource','whenToUse','dependencies','tools','permissions','inventoryStatus','fileCount','availableFileCount','missingCount','packedCount','recordedWarning','warningProvenance','searchKeywords','metadataFields','frontmatter']
DOCUMENT=['title','sha256','bytes','characters','lines','words','bodyStartLine','frontmatterStartLine','frontmatterEndLine','sectionCount','codeBlockCount','referenceCount','codeLanguages']
INVENTORY=['availableBytes','missingHistoricalBytes','availableTextFiles','availableBinaryOrNonUtf8Files','availableContentFingerprint','extensions','roles']
FILE_FIELDS=['path','libraryPath','storage','available','bytes','sizeSource','extension','role','mimeType','sha256','contentKind','encoding','lines','words','characters','executableBit']
TABLE_COLUMNS={
 'files.csv':['skillId']+[k for k in FILE_FIELDS if k!='libraryPath'],
 'sections.csv':['skillId','order','level','title','startLine','endLine','parentOrder'],
 'references.csv':['skillId','order','line','column','kind','label','target','insideCodeBlock','resolvedPath','availability'],
 'code-blocks.csv':['skillId','order','language','info','startLine','endLine','closed','contentBytes','contentSha256']}

def csv_value(v):
 if v is None:return ''
 if not isinstance(v,str):v=j(v)
 if v.lstrip(' \t\r\n').startswith(('=','+','-','@')) or v.startswith(('\t','\r','\n')):v="'"+v
 return v

def write_csv(path,cols,rows):
 count=0;maxcell=0
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
  for row in rows:
   row={k:csv_value(row.get(k)) for k in cols};maxcell=max(maxcell,*(len(v) for v in row.values()));w.writerow(row);count+=1
 return {'file':path.name,'rows':count,'columns':cols,'columnCount':len(cols),'largestCellCharacters':maxcell,'bytes':path.stat().st_size}

def export_tables(data,out):
 records=data['skills'];declared=sorted({p for r in records for p in r['metadataFields']})
 cols=BASE+['document.'+k for k in DOCUMENT]+['inventory.'+k for k in INVENTORY]+['referenceStatusCounts']+['declared:'+p for p in declared]
 def main_rows():
  for r in records:
   row={k:r[k] for k in BASE};row.update({'document.'+k:r['document'][k] for k in DOCUMENT});row.update({'inventory.'+k:r['inventory'][k] for k in INVENTORY});row['referenceStatusCounts']=r['referenceStatusCounts']
   row.update({'declared:'+p:(j(v) if v is None else v) for p,v in leaves(r['frontmatter'])});yield row
 manifest={'skills.csv':write_csv(out/'skills.csv',cols,main_rows())}
 for filename,key in [('files.csv','files'),('sections.csv','outline'),('references.csv','references'),('code-blocks.csv','codeBlocks')]:
  def rows():
   for r in records:
    for item in r[key]:yield {'skillId':r['id'],'skillName':r['name'],'category':r['category'],'entrypoint':r['path'],**item}
  manifest[filename]=write_csv(out/filename,TABLE_COLUMNS[filename],rows())
 cc=['id','title','count','availableFileCount','missingFileCount','incompleteSkills','recordedWarningSkills','availableBytes','missingHistoricalBytes','directoryPage','skillIds']
 manifest['categories.csv']=write_csv(out/'categories.csv',cc,data['categories'])
 return manifest

COMPACT_KEYS=['name','category','categoryTitle','directory','path','description','tags','author','version','license','compatibility','dependencies','tools','permissions','whenToUse','declaredSource','packed','packedCount','fileCount','availableFileCount','missing','missingCount','recordedWarning','warningProvenance','headings']
def compact_data(data,html=False):
 records=[]
 for r in data['skills']:
  v={k:r[k] for k in COMPACT_KEYS}
  if html:v['files']=[{k:f[k] for k in ['path','storage','bytes']} for f in r['files']]
  else:
   keep=['name','category','categoryTitle','path','description','tags','tools','packed','packedCount','missing','missingCount','availableFileCount','recordedWarning']
   v={k:r[k] for k in keep}
   v.update(id=r['id'],inventoryStatus=r['inventoryStatus'])
   def tokens(text):return set(re.findall(r'[^\W_][\w.+#:/-]*',text.casefold().replace('-',' ').replace('_',' ')))
   declared=' '.join(j(value) for pointer,value in leaves(r['frontmatter']))
   extra=tokens(declared+' '+' '.join(r['headings'])+' '+' '.join(r['searchKeywords']))-tokens(j(v))
   v['searchText']=' '.join(sorted(extra))
  records.append(v)
 return {**{k:data[k] for k in ['schemaVersion','generatedAt','root','skillCount','categoryCount','note','archive','missingReferenceFiles','categories']},'skills':records}
