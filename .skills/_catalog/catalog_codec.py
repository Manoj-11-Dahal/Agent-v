"""Small self-contained HTML catalog payload using plain JSON rows and shared defaults.
Full child inventories stay in the shared CSV index and remain available through find.py.
"""
DROP={'files','headings','categoryTitle','directory','path','fileCount','missing','packed'}
def encode(data):
 categories=[{k:c[k] for k in ('id','title','count')} for c in data['categories']]
 bycategory={c['id']:i for i,c in enumerate(categories)};rows=[]
 for original in data['skills']:
  s=dict(original);bundled=bool(s.get('bundled'))
  directory='kali-tools' if bundled else s['category']+'/'+s['name']
  path='kali-tools/index.json#'+s['name'] if bundled else directory+'/SKILL.md'
  assert directory==s['directory'] and path==s['path']
  assert s['fileCount']==s['availableFileCount']+s['missingCount']
  assert bool(s['missing'])==bool(s['missingCount']) and bool(s['packed'])==bool(s['packedCount'])
  row={k:v for k,v in s.items() if k not in DROP};row['bundled']=bundled;row['category']=bycategory[s['category']];rows.append(row)
 columns=sorted(set().union(*(s.keys() for s in rows)));defaults={}
 for k in columns:
  v=rows[0].get(k)
  if all(r.get(k)==v for r in rows):defaults[k]=v
 columns=[k for k in columns if k not in defaults]
 return {**{k:v for k,v in data.items() if k not in ('skills','categories')},'storageFormat':'shared-default-catalog','detailMode':'shared-index-lookup','categories':categories,'columns':columns,'defaults':defaults,'rows':[[r.get(k) for k in columns] for r in rows]}

def decode(data):
 if data.get('storageFormat')!='shared-default-catalog':return data
 records=[]
 for values in data['rows']:
  r={**data['defaults'],**dict(zip(data['columns'],values))};c=data['categories'][r['category']]
  r['category']=c['id'];r['categoryTitle']=c['title'];r['directory']='kali-tools' if r['bundled'] else r['category']+'/'+r['name']
  r['path']='kali-tools/index.json#'+r['name'] if r['bundled'] else r['directory']+'/SKILL.md'
  r.update(fileCount=r['availableFileCount']+r['missingCount'],missing=bool(r['missingCount']),packed=bool(r['packedCount']),files=[],headings=[],detailsDeferred=True)
  records.append(r)
 return {**data,'skills':records}
