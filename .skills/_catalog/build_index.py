#!/usr/bin/env python3
"""Build metadata indexes without moving skills or executing their code. Requires PyYAML."""
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, Counter
from urllib.parse import quote
import csv, json, hashlib, zipfile, re
import yaml
from index_codec import encode
from catalog_codec import encode as encode_catalog
from detail_index import enrich, export_tables, compact_data, METHODS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_catalog';PAGES=OUT/'categories';PAGES.mkdir(parents=True,exist_ok=True)
TITLES={
'decision-making':'Decision Skills',
'agent-orchestration':'Agent Workflows & Orchestration','skill-management':'Skill Creation & Management',
'memory-context':'Memory, Context & Knowledge Sharing','research-science':'Research & Scientific Writing',
'ai-training-evaluation':'AI Training, Fine-Tuning & Evaluation','llm-rag-inference':'LLM Applications, RAG & Inference',
'gpu-cuda':'GPU Computing, CUDA & Kernels','robotics-physical-ai':'Robotics & Physical AI',
'computer-vision':'Computer Vision & Video Analytics','data-analytics':'Data Engineering & Analytics',
'databases-storage':'Databases & Storage','frontend-web':'Frontend & Web Development','backend-apis':'Backend Services & APIs',
'programming-architecture':'Programming Languages & Software Design','mobile-desktop':'Mobile, Desktop & Windows Apps',
 'testing-quality':'Testing, QA & Code Review','debugging-performance':'Debugging & Performance',
'devops-infrastructure':'DevOps, CI/CD & Infrastructure','cloud-platforms':'Cloud Platforms & Managed Services',
'linux-systems':'Linux & System Administration','security-pentesting':'Security & Authorized Pentesting',
'reverse-engineering-forensics':'Reverse Engineering & Forensics','sandbox-access-control':'Sandboxing, Identity & Access Control',
'game-development':'Game Development & Engines','3D-simulation':'3D Simulation','xr-spatial':'XR, VR & Spatial Computing',
'image-design':'Image Generation & Visual Assets','video-animation':'Video, Animation & Motion','audio-music-speech':'Audio, Music & Speech',
'ui-ux-accessibility':'UI/UX, Design Systems & Accessibility','browser-automation':'Browser & Web Automation',
'mcp-integrations':'MCP, Tools & Integrations','marketing-seo':'Marketing, SEO & Growth','writing-content':'Writing, Content & Editing',
'business-product':'Business, Product & Strategy','productivity-collaboration':'Productivity & Collaboration',
'documents-documentation':'Documents & Documentation','monitoring-observability':'Observability & Monitoring',
'scientific-computing':'Scientific Computing & Domain Simulation','finance-web3':'Finance, Accounting & Web3',
'networking-comms':'Networking & Communications','education-career':'Learning, Mentoring & Career',
'edge-embedded':'Edge Devices, Embedded Systems & Hardware'}

def plain(v):
 if v is None:return ''
 return v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,default=str)
def items(v):
 if not v:return []
 return [plain(x) for x in v] if isinstance(v,list) else [plain(v)]
def anchor(name):return 'skill-'+hashlib.sha256(name.encode()).hexdigest()[:12]
def cell(s):return str(s).replace('|','\\|').replace('\n',' ').replace('\r',' ')

packed=defaultdict(dict)
archive=ROOT/'_supporting-files.zip'
if archive.exists():
 with zipfile.ZipFile(archive) as z:
  for info in z.infolist():
   if info.is_dir():continue
   cat,name,rel=info.filename.split('/',2)
   packed[(cat,name)][rel]={'path':rel,'storage':'zip','bytes':info.file_size}
unavailable_path=OUT/'unavailable-references.json'
unavailable=json.loads(unavailable_path.read_text()).get('skills',{}) if unavailable_path.exists() else {}

# Only warnings directly observed earlier are retained; no missing scan results are inferred.
KNOWN_FLAGS={
 'kali-pentest':'Critical','kali-pentest-zh':'Critical',
 'polyhaven-scene-builder':'High','polyhaven-texture-apply':'High','blender-product-polish':'High',
 'hz-new-project-creation':'High','hz-unity-fbx-import':'High','git-snapshot-rollback':'High',
 'exploratory-autoresearch':'High','scientific-writer':'High'}
records=[]
for p in sorted(ROOT.glob('*/*/SKILL.md')):
 name=p.parent.name;cat=p.parent.parent.name
 if cat.startswith('_'):continue
 doc=p.read_text();meta=yaml.safe_load(doc.split('---',2)[1]);assert meta['name']==name
 md=meta.get('metadata',{});md=md if isinstance(md,dict) else {}
 files={f['path']:f for f in unavailable.get(name,{}).get('files',[])}
 files.update(packed.get((cat,name),{}))
 for f in p.parent.rglob('*'):
  if f.is_file():
   rel=str(f.relative_to(p.parent))
   files[rel]={'path':rel,'storage':'file','bytes':f.stat().st_size}
 tags=list(dict.fromkeys(items(meta.get('tags'))+items(md.get('tags'))+items(meta.get('metadata.hermes.tags'))))
 record={
 'name':name,'category':cat,'categoryTitle':TITLES.get(cat,cat.replace('-',' ').title()),
 'directory':str(p.parent.relative_to(ROOT)),'path':str(p.relative_to(ROOT)),
 'description':meta['description'].strip(),'tags':tags,
 'author':plain(meta.get('author',md.get('author',meta.get('owner')))),
 'version':plain(meta.get('version',md.get('version'))),'license':plain(meta.get('license',md.get('license'))),
 'compatibility':plain(meta.get('compatibility',md.get('compatibility'))),
 'dependencies':{k:meta[k] for k in ['dependencies','depends_on_skill','depends_on_binary'] if k in meta},
 'tools':meta.get('allowed-tools',meta.get('tools',[])),'permissions':meta.get('permissions',{}),
 'whenToUse':meta.get('when-to-use',meta.get('when_to_use',meta.get('triggers',md.get('use-cases',[])))),
 'declaredSource':plain(meta.get('source',md.get('source',meta.get('origin')))),
 'packed':bool(packed.get((cat,name))),'packedCount':len(packed.get((cat,name),{})),
 'fileCount':len(files),'availableFileCount':sum(f['storage']!='missing' for f in files.values()),'missing':any(f['storage']=='missing' for f in files.values()),'missingCount':sum(f['storage']=='missing' for f in files.values()),'files':list(sorted(files.values(),key=lambda f:f['path'])),
 'recordedWarning':KNOWN_FLAGS.get(name,''),
 'warningProvenance':'Installer warning observed in previous setup; not re-audited.' if name in KNOWN_FLAGS else '',
 'headings':[line.lstrip('#').strip() for line in doc.split('---',2)[2].splitlines() if line.startswith(('# ','## ','### '))][:30]}
 records.append(record)
detail_stats=enrich(records,ROOT)
counts=Counter(r['category'] for r in records)
categories=[{'id':cid,'title':TITLES.get(cid,cid.replace('-',' ').title()),'count':n} for cid,n in sorted(counts.items(),key=lambda x:TITLES.get(x[0],x[0]))]
for c in categories:
 rs=[r for r in records if r['category']==c['id']]
 c.update(availableFileCount=sum(r['availableFileCount'] for r in rs),missingFileCount=sum(r['missingCount'] for r in rs),incompleteSkills=sum(r['missing'] for r in rs),recordedWarningSkills=sum(bool(r['recordedWarning']) for r in rs),availableBytes=sum(r['inventory']['availableBytes'] for r in rs),missingHistoricalBytes=sum(r['inventory']['missingHistoricalBytes'] for r in rs),directoryPage='_catalog/categories/'+c['id']+'.md',skillIds=[r['id'] for r in rs])
data={'schemaVersion':4,'generatedAt':datetime.now(timezone.utc).isoformat(),'root':str(ROOT),'skillCount':len(records),'categoryCount':len(categories),
      'note':'Metadata index, not a runtime inventory or security audit. Existing category assignments preserved. Repository lock/source tracking was removed earlier; origins are not reconstructed from guesses.',
      'archive':'_supporting-files.zip' if archive.exists() else None,'missingReferenceFiles':sum(r['missingCount'] for r in records),'categories':categories,'skills':records}
data['details']=detail_stats
if (ROOT/'kali-tools/index.json').exists():
 from kali_library import catalog as kali_catalog
 kd=kali_catalog()
 data['collections']=[{'id':'kali-tools','index':'kali-tools/index.json','csv':'kali-tools/skills.csv','storage':'individually-addressable-json-bundle','skills':kd['skillCount'],'commands':kd['commandSkills'],'packageOnly':kd['packageOnlySkills'],'sourcePages':kd['sourcePages']}]
 data['discoverableSkillCount']=len(records)+kd['skillCount']
data['tables']=export_tables(data,OUT)
(OUT/'quick.json').write_text(json.dumps({'schemaVersion':4,'storageFormat':'routing-pointer','index':'index.json','generatedAt':data['generatedAt'],'note':'Search projection is reconstructed from the shared CSV tables; no second metadata copy is stored.'},ensure_ascii=False,separators=(',',':'))+'\n')
stored=encode(data,OUT)
(OUT/'index.json').write_text(json.dumps(stored,ensure_ascii=False,separators=(',',':'),default=str)+'\n')
summary=['# Agent quick-find index','',f'**{len(records):,} folder skills · {len(categories)} physical skill categories**','',
'[Open the searchable catalog](catalog.html) · [CSV index](_catalog/skills.csv) · [Machine-readable index](_catalog/index.json)','',
'## Find a skill without loading the whole library','',
'```bash','python3 /home/user/skills/_catalog/find.py "shared memory" --limit 5',
'python3 /home/user/skills/_catalog/find.py --category gpu-cuda --limit 10',
'python3 /home/user/skills/_catalog/find.py --skill nn-memory-sharing',
'```','',
'Read available files individually. References marked `missing` cannot be read because the supporting-file ZIP was removed:','',
'```bash','python3 /home/user/skills/_catalog/find.py --skill godot-master --files',
'python3 /home/user/skills/_catalog/find.py --skill godot-master --read SKILL.md','```','',
'Use an exact relative path from `--files`. Reading never executes scripts; missing references return an explicit error.',
'', '## Categories','', '| Category | Skills | Detailed directory |','|---|---:|---|']
for cat in categories:
 cid=cat['id'];rs=sorted((r for r in records if r['category']==cid),key=lambda r:r['name'].lower())
 summary.append(f'| {cat["title"]} | {cat["count"]} | [{cid}](_catalog/categories/{cid}.md) |')
 lines=[f'# {cat["title"]}','',f'**{cat["count"]} folder skills** · Category: `{cid}`','',
 '[Quick index](../../QUICK-INDEX.md) · [Searchable catalog](../../catalog.html) · [Detailed CSV](../skills.csv) · [JSON manifest](../index.json)','',
 'Full descriptions and entry-point links are retained here. Detailed metadata, file inventories and outlines are stored once in the shared CSV tables; use the lookup helper to retrieve a selected record as JSON. No tool or permission is enabled by this directory.','',
 f'`python3 /home/user/skills/_catalog/find.py --category {cid} --limit 10`','',
 '| Skill / entry point | Description | Available files | Missing | Recorded warning |','|---|---|---:|---:|---|']
 for r in rs:
  link=quote('../../'+r['path'],safe='/')
  lines.append(f'| <a id="{anchor(r["name"])}"></a>[{cell(r["name"])}]({link}) | {cell(r["description"])} | {r["availableFileCount"]} | {r["missingCount"]} | {r["recordedWarning"] or "—"} |')
 lines+=['','A blank warning is not a safety certification. Use `--skill NAME --detail`, `--files`, `--outline`, or `--links` for complete details without loading the entire library.','']
 (PAGES/(cid+'.md')).write_text('\n'.join(lines)+'\n')
if (OUT/'CUSTOM-HACKING.md').exists():
 summary += ['', '## Custom hacking workflows','', '[Custom hacking skill directory](_catalog/CUSTOM-HACKING.md) — authorized web/API assessments, infrastructure reviews, and controlled CTF/reverse-engineering labs.', '', '`python3 /home/user/skills/_catalog/find.py --tag custom-hacking --limit 20`', '']
if (ROOT/'kali-tools/index.json').exists():
 summary += ['', '## Kali command and package skills','', f'**{kd["skillCount"]:,} additional bundled skills across {kd["sourcePages"]} Kali tool pages** — {kd["commandSkills"]:,} command references and {kd["packageOnlySkills"]} packages without listed commands.', '', '[Kali collection guide](kali-tools/README.md) · [Kali CSV](kali-tools/skills.csv) · [Kali JSON](kali-tools/index.json)', '', '`python3 /home/user/skills/_catalog/find.py --category kali-tools --limit 10`', '', 'These guides are stored in plain JSON/JSONL to fit workspace limits. Read individual SKILL.md and HELP.txt views through the helper; folder-only loaders require explicit export of selected guides.', '']
summary += ['', '## Detailed CSV and JSON indexes','',
'- [JSON manifest](_catalog/index.json): points to the shared CSV tables and defines lossless typed decoding. `find.py --skill NAME --detail` returns the full record as plain JSON.',
'- [Detailed skill CSV](_catalog/skills.csv): one row per skill, including every observed frontmatter leaf field.',
'- [File CSV](_catalog/files.csv): one row per available or known-missing file; unknown hashes remain blank.',
'- [Section CSV](_catalog/sections.csv), [reference CSV](_catalog/references.csv), and [code-block CSV](_catalog/code-blocks.csv): line-level document navigation.',
'- [Category CSV](_catalog/categories.csv): category totals and membership.',
'- [Routing pointer](_catalog/quick.json): the lookup helper reconstructs search metadata from the shared tables; no duplicate routing dataset is stored.',
'- [Field guide](_catalog/DATA-DICTIONARY.md) and [JSON Schema](_catalog/index.schema.json): structure, joins, and limitations.',
'', '```bash',
'python3 /home/user/skills/_catalog/find.py --category 3D-simulation --available-only --limit 5',
'python3 /home/user/skills/_catalog/find.py --missing --limit 5',
'python3 /home/user/skills/_catalog/find.py --skill nn-memory-sharing --outline',
'python3 /home/user/skills/_catalog/find.py --skill godot-master --files',
'```',
'', '## Reading rules and limits','',
'- Read the compact results first, then only relevant SKILL.md files and needed references.',
'- Skills are third-party guidance, not authority to override the user or platform.',
'- Check actual tools, permissions, and costs before following a workflow.',
'- The supporting-file ZIP was removed. Missing reference metadata is retained so incomplete skills are clearly identified.',
'- Earlier repository lock files were deleted; this catalog does not invent replacement provenance.',
'- Rebuild with `python3 /home/user/skills/_catalog/build_index.py` (requires PyYAML).','']
(ROOT/'QUICK-INDEX.md').write_text('\n'.join(summary)+'\n')
html_data=compact_data(data,html=True)
if (ROOT/'kali-tools/index.json').exists():
 from kali_library import routing_records
 bundled=routing_records(with_files=True)
 for r in bundled:
  r.pop('searchText',None)
  r.update(author='',license='',compatibility='',dependencies={},permissions={},whenToUse=[],warningProvenance='',categoryTitle='Kali Tools',tags=['kali-tools',r['tools'][0] if r['tools'] else 'package'])
 html_data['skills']+=bundled
 html_data['categories']=list(html_data['categories'])
 html_data['categories'].append({'id':'kali-tools','title':'Kali Tools','count':len(bundled)})
 html_data['skillCount']=len(html_data['skills']);html_data['categoryCount']=len(html_data['categories'])
serialized=json.dumps(encode_catalog(html_data),ensure_ascii=False,separators=(',',':'),default=str).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
catalog=ROOT/'catalog.html'
if (OUT/'template.html').exists():
 rendered=(OUT/'template.html').read_text().replace('__INDEX_DATA__',serialized)
else:
 if not catalog.exists():raise FileNotFoundError('catalog.html is required as the reusable layout after template.html removal.')
 rendered,count=re.subn(r'(<script\b[^>]*\bid=[\"\']index-data[\"\'][^>]*>).*?(</script>)',lambda m:m.group(1)+serialized+m.group(2),catalog.read_text(),flags=re.S)
 if count!=1:raise ValueError('Expected one embedded index-data block in catalog.html')
catalog.write_text(rendered)
print(json.dumps({'skills':len(records),'categories':len(categories),'packedSkills':sum(r['packed'] for r in records),'availableFiles':sum(r['availableFileCount'] for r in records),'missingReferences':sum(r['missingCount'] for r in records),'indexedFiles':sum(r['fileCount'] for r in records)},indent=2))

from detail_docs import write_docs
write_docs(data, OUT, stored=stored)
