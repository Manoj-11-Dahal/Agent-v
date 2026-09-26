#!/usr/bin/env python3
"""Validate generated discovery indexes without executing any skill code.
Optional --baseline accepts a path-to-SHA256 JSON map captured before index changes.
Uses PyYAML via detail_index; validates JSON Schema too when jsonschema is available.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from urllib.parse import unquote
import argparse, ast, csv, hashlib, json, re, subprocess, sys
import yaml
from detail_index import normal, leaves, csv_value, parse_doc
from index_codec import decode
from catalog_codec import decode as decode_catalog

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_catalog'
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--baseline',type=Path);parser.add_argument('--allow-additions',action='store_true');args=parser.parse_args()
 if args.allow_additions and not args.baseline:parser.error('--allow-additions requires --baseline')
 stored=json.loads((OUT/'index.json').read_text());data=decode(stored);skills=data['skills'];byid={r['id']:r for r in skills}
 assert data['schemaVersion']==4 and len(skills)==data['skillCount']==len(byid)
 actual={str(p.relative_to(ROOT)) for p in ROOT.glob('*/*/SKILL.md') if not p.parent.parent.name.startswith('_')}
 assert actual=={r['path'] for r in skills}
 assert len(data['categories'])==data['categoryCount']==len({r['category'] for r in skills})
 assert (ROOT/'3D-simulation').is_dir() and not (ROOT/'3d-cad-simulation').exists()
 assert not (ROOT/'_supporting-files.zip').exists() and not (OUT/'template.html').exists()
 hashes={};available=missing=0
 for r in skills:
  raw=(ROOT/r['path']).read_bytes();text=raw.decode();lines=text.splitlines(keepends=True)
  close=next(i for i,v in enumerate(lines[1:],1) if v.strip()=='---')
  assert normal(yaml.safe_load(''.join(lines[1:close])))==r['frontmatter']
  assert r['document']['sha256']==hashlib.sha256(raw).hexdigest()
  assert r['document']['lines']==len(lines)
  assert r['fileCount']==len(r['files'])
  for f in r['files']:
   p=ROOT/f['libraryPath'];assert p.resolve().is_relative_to(ROOT)
   if f['storage']=='missing':
    assert not p.exists() and not f['available'] and f['sha256'] is None
    assert all(f[k] is None for k in ['encoding','lines','words','characters','executableBit']);missing+=1
   else:
    b=p.read_bytes();h=hashlib.sha256(b).hexdigest();hashes[f['libraryPath']]=h
    assert f['available'] and f['bytes']==len(b) and f['sha256']==h;available+=1
  assert r['missingCount']==sum(f['storage']=='missing' for f in r['files'])
  assert r['availableFileCount']==sum(f['available'] for f in r['files'])
  for h in r['outline']:
   assert 1<=h['startLine']<=h['endLine']<=len(lines)
   assert lines[h['startLine']-1].lstrip().startswith('#'*h['level'])
   if h['parentOrder'] is not None:
    parent=r['outline'][h['parentOrder']-1];assert parent['level']<h['level'] and parent['endLine']>=h['endLine']
  for block in r['codeBlocks']:
   end=block['endLine']-1 if block['closed'] else block['endLine']
   payload=''.join(lines[block['startLine']:end]).encode()
   assert len(payload)==block['contentBytes'] and hashlib.sha256(payload).hexdigest()==block['contentSha256']
 assert available==data['details']['availableFiles'] and missing==data['missingReferenceFiles']==data['details']['missingFiles']
 if args.baseline:
  baseline=json.loads(args.baseline.read_text())
  assert all(path in hashes and hashes[path]==digest for path,digest in baseline.items()),'Previously retained skill content changed or disappeared.'
  if not args.allow_additions:assert baseline==hashes,'Unexpected additions to canonical skill content.'
 for cat in data['categories']:
  rs=[r for r in skills if r['category']==cat['id']]
  assert len(rs)==cat['count'] and {r['id'] for r in rs}==set(cat['skillIds'])
  assert sum(r['missingCount'] for r in rs)==cat['missingFileCount']
 csv_totals={}
 for name,t in data['tables'].items():
  with (OUT/name).open(newline='') as f:
   reader=csv.DictReader(f);assert reader.fieldnames==t['columns'];rows=list(reader)
  assert len(rows)==t['rows'];csv_totals[name]=len(rows)
  for row in rows:
   assert None not in row
   for value in row.values():assert not value.lstrip(' \t\r\n').startswith(('=','+','-','@'))
  if name=='skills.csv':
   assert {r['id'] for r in rows}==set(byid)
   for row in rows:
    r=byid[row['id']];assert json.loads(row['frontmatter'])==r['frontmatter']
    for pointer,value in leaves(r['frontmatter']):assert row['declared:'+pointer]==csv_value('null' if value is None else value)
  elif name!='categories.csv':
   key={'files.csv':'files','sections.csv':'outline','references.csv':'references','code-blocks.csv':'codeBlocks'}[name]
   counts=Counter(row['skillId'] for row in rows);assert set(counts)<=set(byid)
   for r in skills:assert counts[r['id']]==len(r[key])
   expected=({'skillId':r['id'],**v} for r in skills for v in r[key])
   for row,item in zip(rows,expected):assert row=={k:csv_value(item.get(k)) for k in t['columns']}
 quick=decode(json.loads((OUT/'quick.json').read_text()));assert {r['id'] for r in quick['skills']}==set(byid)
 assert quick['generatedAt']==data['generatedAt']
 for r in quick['skills']:
  full=byid[r['id']]
  for k,v in r.items():
   if k!='searchText':assert full[k]==v
 for p in [ROOT/'QUICK-INDEX.md',OUT/'DATA-DICTIONARY.md',*(OUT/'categories').glob('*.md')]:
  for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if link.startswith(('http:','https:','#','mailto:')):continue
   if p.parent.name=='categories' and not link.startswith('../../'):continue
   assert (p.parent/unquote(link.split('#')[0])).exists(),(p,link)
 html=(ROOT/'catalog.html').read_text();m=re.search(r'<script\b[^>]*\bid=[\"\']index-data[\"\'][^>]*>(.*?)</script>',html,re.S);assert m
 embedded=decode_catalog(json.loads(m[1]));assert embedded['generatedAt']==data['generatedAt'] and len(embedded['skills'])==data.get('discoverableSkillCount',len(skills))
 for r in embedded['skills']:
  if r.get('bundled'):
   from kali_library import catalog
   assert r['name'] in catalog()['_skills'];continue
  full=next(v for v in skills if v['name']==r['name']);assert r['path']==full['path'] and r['fileCount']==full['fileCount'] and r['detailsDeferred']
  assert 'frontmatter' not in r
 for p in OUT.glob('*.py'):ast.parse(p.read_text())
 cli=[sys.executable,str(OUT/'find.py')]
 def call(*args):return json.loads(subprocess.check_output(cli+list(args),text=True))
 assert 'nn-memory-sharing' in [r['name'] for r in call('shared memory','--category','memory-context','--limit','5')['results']]
 assert call('nn memory sharing','--limit','1')['results'][0]['name']=='nn-memory-sharing'
 assert call('--tag','3dsmax','--limit','1')['matches']>0
 assert call('--tool','Bash','--limit','1')['matches']>0
 assert call('--category','3D-simulation','--limit','1')['matches']==sum(r['category']=='3D-simulation' for r in skills)
 assert call('--missing','--limit','1')['matches']==sum(r['missing'] for r in skills)
 assert call('--available-only','--limit','1')['matches']==sum(not r['missing'] for r in skills)+sum(c['skills'] for c in data.get('collections',[]))
 assert call('--has-warning','--limit','1')['matches']==sum(bool(r['recordedWarning']) for r in skills)
 s=next(r for r in skills if r['name']=='nn-memory-sharing')
 assert call('--skill',s['name'],'--outline')['outline']==s['outline']
 assert call('--skill',s['name'],'--links')['references']==s['references']
 assert call('--skill',s['name'],'--detail')==s
 out=call('--skill',s['name'],'--read','SKILL.md','--start-line','10','--end-line','15')
 assert out['content']==''.join((ROOT/s['path']).read_text().splitlines(keepends=True)[9:15])
 bad=next(r for r in skills if r['missing']);ref=next(f['path'] for f in bad['files'] if not f['available'])
 for cli_args,phrase in [(['--skill',bad['name'],'--read',ref],'Reference unavailable'),(['--skill',s['name'],'--read','../SKILL.md'],'safe relative')]:
  result=subprocess.run(cli+cli_args,text=True,capture_output=True);assert result.returncode==2 and phrase in result.stderr
 assert all('references/' in f['path'] for f in call('--skill','godot-master','--files','--file-match','references/')['files'])
 # Synthetic parser checks: code headings ignored, nested sections retain correct ranges.
 heads,blocks,refs=parse_doc('# Root\n## Child\n```sh\n# not heading\necho hi\n```\n# Next\n[x](https://example.com)\n',1)
 assert [h['title'] for h in heads]==['Root','Child','Next'] and heads[0]['endLine']==6 and heads[1]['parentOrder']==1
 assert len(blocks)==1 and blocks[0]['closed'] and len(refs)==1
 schema_status='not run: jsonschema unavailable'
 try:
  import jsonschema
  schema=json.loads((OUT/'index.schema.json').read_text());jsonschema.Draft202012Validator.check_schema(schema);jsonschema.Draft202012Validator(schema).validate(stored);schema_status='passed'
 except ImportError:pass
 report={'checkedAt':datetime.now(timezone.utc).isoformat(),'schemaVersion':4,'skills':len(skills),'discoverableSkills':data.get('discoverableSkillCount',len(skills)),'categories':len(data['categories']),'availableFilesHashed':available,'missingReferences':missing,'csvRows':csv_totals,'jsonSchemaValidation':schema_status,'canonicalContentComparedToBaseline':bool(args.baseline),'additionsAllowed':args.allow_additions,'newFileCountSinceBaseline':len(set(hashes)-set(baseline)) if args.baseline else None,'checks':['Exact skill and category coverage','Full frontmatter preservation','Available-file SHA-256 and missing-null checks','CSV headers, rows, foreign keys and values','Section ranges and code-block payload hashes','Compact routing projection and catalog payload','Documentation navigation','CLI searches, filters, outlines, links, details and line-range reads','Missing-file and traversal rejection','Synthetic Markdown parsing and CSV formula protection'],'uiScope':'Embedded catalog data verified; no new visual browser test performed.'}
 (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
