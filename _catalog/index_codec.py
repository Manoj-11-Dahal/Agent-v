"""Plain CSV-backed JSON index, with backwards-compatible v3 decoding.
No compression or archive extraction. All detailed CSV cells remain unchanged.
"""
from pathlib import Path
import csv, json, re
BASE=Path(__file__).resolve().parent
CHILDREN={'files.csv':'files','sections.csv':'outline','references.csv':'references','code-blocks.csv':'codeBlocks'}

def _unescape(value):
 if value.startswith("'"):
  rest=value[1:]
  if rest.lstrip(' \t\r\n').startswith(('=','+','-','@')) or rest.startswith(('\t','\r','\n')):return rest
 return value

def _kind(v):
 if v is None:return 'null'
 if isinstance(v,bool):return 'boolean'
 if isinstance(v,int):return 'integer'
 if isinstance(v,float):return 'number'
 if isinstance(v,str):return 'string'
 return 'json'

def _type(values):
 kinds={_kind(v) for v in values}
 if kinds=={'string'}:return 'string'
 if kinds<={'string','null'}:return 'nullable-string'
 if 'string' in kinds:return 'mixed'
 if kinds=={'integer'}:return 'integer'
 return 'json'

def _value(raw,kind):
 raw=_unescape(raw)
 if kind=='string':return raw
 if kind=='nullable-string':return raw if raw else None
 if kind=='integer':return int(raw)
 if raw=='':return None if kind!='mixed' else ''
 try:return json.loads(raw)
 except json.JSONDecodeError:
  if kind=='mixed':return raw
  raise

def _safe_table(base,name):
 p=(base/name).resolve()
 if p.parent!=base.resolve() or p.suffix!='.csv':raise ValueError('CSV manifest references must stay in the catalog directory.')
 return p

def _records(data,base,skill_name=None,routing=False):
 schemas=data['csvTypes'];records=[]
 with _safe_table(base,'skills.csv').open(newline='',encoding='utf-8') as f:
  for source in csv.DictReader(f):
   if skill_name and source['name']!=skill_name:continue
   r={'document':{},'inventory':{}}
   for k,kind in schemas['skills.csv'].items():
    v=_value(source[k],kind)
    if k.startswith('document.'):r['document'][k[9:]]=v
    elif k.startswith('inventory.'):r['inventory'][k[10:]]=v
    else:r[k]=v
   r.update(packed=bool(r['packedCount']),missing=bool(r['missingCount']),files=[],outline=[],references=[],codeBlocks=[])
   r['metadataStatus']={'fieldCount':len(r['metadataFields']),'authorDeclared':bool(r['author']),'versionDeclared':bool(r['version']),'licenseDeclared':bool(r['license']),'sourceTracking':'declared-only; previous lock removed','warningCoverage':'partial historical installer observations; not re-audited'}
   records.append(r)
 byid={r['id']:r for r in records}
 for filename,key in CHILDREN.items():
  if routing and key!='outline':continue
  with _safe_table(base,filename).open(newline='',encoding='utf-8') as f:
   for source in csv.DictReader(f):
    r=byid.get(source['skillId'])
    if r is None:continue
    item={k:_value(source[k],kind) for k,kind in schemas[filename].items() if k!='skillId'}
    if key=='files':item['libraryPath']=r['directory']+'/'+item['path']
    r[key].append(item)
 for r in records:
  r['headings']=[h['title'] for h in r['outline']]
  patch=data.get('recordOverrides',{}).get(r['id'],{})
  r.update(patch.get('set',{}))
  for key in patch.get('remove',[]):r.pop(key,None)
 return records

def encode(data,base=None):
 """Build a small manifest and prove it reconstructs every detailed record exactly."""
 base=Path(base or BASE);records=data['skills'];schemas={}
 main_columns=[k for k in data['tables']['skills.csv']['columns'] if not k.startswith('declared:')]
 def field(r,k):
  if k.startswith('document.'):return r['document'][k[9:]]
  if k.startswith('inventory.'):return r['inventory'][k[10:]]
  return r[k]
 schemas['skills.csv']={k:_type(field(r,k) for r in records) for k in main_columns}
 for filename,key in CHILDREN.items():
  items=[v for r in records for v in r[key]]
  schemas[filename]={k:('string' if k=='skillId' else _type(v.get(k) for v in items)) for k in data['tables'][filename]['columns']}
 out={k:v for k,v in data.items() if k not in {'skills','rowSchemas','storageFormat'}}
 out.update(schemaVersion=4,storageFormat='csv-backed-json-index',recordsTable='skills.csv',childTables=CHILDREN,csvTypes=schemas,recordOverrides={})
 actual=_records(out,base)
 assert len(actual)==len(records)
 for expected,recovered in zip(records,actual):
  assert expected['id']==recovered['id']
  changes={k:v for k,v in expected.items() if k not in recovered or recovered[k]!=v}
  removed=sorted(set(recovered)-set(expected))
  if changes or removed:out['recordOverrides'][expected['id']]={'set':changes,'remove':removed}
 # Overrides preserve rare CSV string/type ambiguities instead of silently changing values.
 for recovered in actual:
  patch=out['recordOverrides'].get(recovered['id'],{});recovered.update(patch.get('set',{}))
  for k in patch.get('remove',[]):recovered.pop(k,None)
 assert actual==records,'Lossless index reconstruction failed.'
 out['decodingNote']='Detailed records reside once in the plain CSV tables. Use index_codec.load() or find.py for complete JSON views. csvTypes defines typed cells; recordOverrides preserves any ambiguous CSV values exactly. No skill content is removed.'
 return out

def _leaves(value):
 if isinstance(value,dict) and value:
  for v in value.values():yield from _leaves(v)
 else:yield value

def routing_projection(data):
 records=[]
 keep=['name','category','categoryTitle','path','description','tags','tools','packed','packedCount','missing','missingCount','availableFileCount','recordedWarning']
 def tokens(text):return set(re.findall(r'[^\W_][\w.+#:/-]*',text.casefold().replace('-',' ').replace('_',' ')))
 def j(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'),allow_nan=False)
 for r in data['skills']:
  v={k:r[k] for k in keep};v.update(id=r['id'],inventoryStatus=r['inventoryStatus'])
  declared=' '.join(j(value) for value in _leaves(r['frontmatter']))
  extra=tokens(declared+' '+' '.join(r['headings'])+' '+' '.join(r['searchKeywords']))-tokens(j(v))
  v['searchText']=' '.join(sorted(extra));records.append(v)
 return {**{k:data[k] for k in ['schemaVersion','generatedAt','root','skillCount','categoryCount','note','archive','missingReferenceFiles','categories']},'skills':records}

def decode(data,base=None,skill_name=None,routing=False):
 base=Path(base or BASE)
 if data.get('storageFormat')=='routing-pointer':
  raw=json.loads((base/'index.json').read_text());return routing_projection(decode(raw,base,routing=True))
 if data.get('storageFormat')=='csv-backed-json-index':
  return {**data,'skills':_records(data,base,skill_name,routing)}
 if data.get('storageFormat')!='columnar-child-records':return data
 # Read older v3 snapshots without an extra dependency.
 out={**data,'skills':[]}
 for skill in data['skills']:
  row=dict(skill)
  for key in CHILDREN.values():row[key]=[dict(zip(data['rowSchemas'][key],r)) for r in skill.get(key,[])]
  row['description']=row['frontmatter']['description'].strip();row['headings']=[h['title'] for h in row['outline']]
  def pointers(value,prefix=''):
   if isinstance(value,dict) and value:
    for k,v in value.items():yield from pointers(v,prefix+'/'+k.replace('~','~0').replace('/','~1'))
   else:yield prefix
  row['metadataFields']=sorted(pointers(row['frontmatter']));out['skills'].append(row)
 return out

def load(path,skill_name=None,routing=False):
 path=Path(path);return decode(json.loads(path.read_text()),path.parent,skill_name,routing)
