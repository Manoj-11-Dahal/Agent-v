#!/usr/bin/env python3
"""Compact, read-only search and reference access for the categorized skill library.

Examples:
  python3 find.py "shared memory" --limit 5
  python3 find.py --category gpu-cuda --limit 10
  python3 find.py --skill godot-master --files
  python3 find.py --skill godot-master --read references/README.md

No skill code is executed. Missing references are reported, not silently ignored. Uses only Python's standard library.
"""
import argparse
import json
from pathlib import Path, PurePosixPath
import sys
import unicodedata
import zipfile
from index_codec import decode

ROOT=Path(__file__).resolve().parents[1]

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD',str(s).casefold()) if not unicodedata.combining(c)).replace('-',' ').replace('_',' ')

def brief(r):
    out={k:r[k] for k in ['name','category','description','path','packed','packedCount','missing','missingCount','availableFileCount','inventoryStatus','recordedWarning']}
    out['descriptionTruncated']=len(r['description'])>500
    if out['descriptionTruncated']:out['description']=r['description'][:500]+'…'
    return out

def safe_relative(value):
    p=PurePosixPath(value)
    if not value or not p.parts or p.is_absolute() or '..' in p.parts or '\\' in value or '\x00' in value:
        raise ValueError('Use a safe relative file path from the indexed file list.')
    return Path(*p.parts)

def read_reference(data,skill,relative,max_chars,start_line=1,end_line=None):
    safe_relative(relative)
    entry=next((f for f in skill['files'] if f['path']==relative),None)
    if entry is None:raise ValueError('File is not indexed for this skill. Use --skill NAME --files.')
    if entry['storage']=='missing':raise ValueError('Reference unavailable: the supporting-file ZIP was deleted. Restore this skill from its original source before using this file.')
    if entry['storage']=='bundle':
        from kali_library import read
        raw=read(skill['name'],relative).encode('utf-8')
    elif entry['storage']=='zip':
        member=skill['directory']+'/'+relative
        with zipfile.ZipFile(ROOT/data['archive']) as z:raw=z.read(member)
    else:
        directory=(ROOT/safe_relative(skill['directory'])).resolve()
        if not directory.is_relative_to(ROOT.resolve()):raise ValueError('Skill directory leaves the library root.')
        p=(directory/safe_relative(relative)).resolve()
        if not p.is_relative_to(directory):raise ValueError('Resolved path leaves the skill directory.')
        raw=p.read_bytes()
    try:content=raw.decode('utf-8')
    except UnicodeDecodeError:return {'skill':skill['name'],'file':relative,'storage':entry['storage'],'bytes':len(raw),'binary':True,'message':'Binary file: use an appropriate viewer. No content executed or extracted.'}
    lines=content.splitlines(keepends=True)
    if start_line>max(1,len(lines)):raise ValueError('Start line exceeds this file length.')
    stop=min(end_line or len(lines),len(lines));selected=''.join(lines[start_line-1:stop])
    return {'skill':skill['name'],'file':relative,'storage':entry['storage'],'characters':len(content),'startLine':start_line,'endLine':stop,'selectedCharacters':len(selected),'truncated':len(selected)>max_chars,'content':selected[:max_chars]}

def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('query',nargs='*');p.add_argument('--category');p.add_argument('--limit',type=int,default=8)
    p.add_argument('--skill');p.add_argument('--files',action='store_true');p.add_argument('--read',dest='read_file')
    p.add_argument('--max-chars',type=int,default=16000)
    p.add_argument('--raw',action='store_true',help='For --read only: emit exact text, failing rather than silently truncating.')
    p.add_argument('--outline',action='store_true',help='Include full line-numbered heading outline for an exact skill.')
    p.add_argument('--links',action='store_true',help='Include extracted links and availability for an exact skill.')
    p.add_argument('--detail',action='store_true',help='Return the full detailed record, including all child inventories.')
    status=p.add_mutually_exclusive_group()
    status.add_argument('--missing',action='store_true',help='Find skills with known missing references.')
    status.add_argument('--available-only',action='store_true',help='Find skills with no known missing files; not a runtime-readiness claim.')
    p.add_argument('--has-warning',action='store_true',help='Filter by retained partial historical installer warnings.')
    p.add_argument('--tag');p.add_argument('--tool')
    p.add_argument('--start-line',type=int,default=1);p.add_argument('--end-line',type=int)
    p.add_argument('--file-match',help='Filter an explicit --files inventory by a filename substring.')
    args=p.parse_args()
    if args.raw and not args.read_file:p.error('--raw requires --read')
    if not 1<=args.limit<=100:p.error('--limit must be between 1 and 100')
    if not 1<=args.max_chars<=100000:p.error('--max-chars must be between 1 and 100000')
    if (args.files or args.read_file or args.outline or args.links or args.detail) and not args.skill:p.error('--files, --read, --outline, --links and --detail require --skill')
    if args.start_line<1 or (args.end_line is not None and args.end_line<args.start_line):p.error('Line range must be positive and ordered.')
    if (args.start_line!=1 or args.end_line is not None) and not args.read_file:p.error('Line ranges require --read.')
    if args.file_match and not args.files:p.error('--file-match requires --files.')
    if args.skill and (args.query or args.category or args.missing or args.available_only or args.has_warning or args.tag or args.tool):p.error('Search filters cannot be combined with an exact --skill selection.')
    index=ROOT/'_catalog'/('index.json' if args.skill else 'quick.json')
    if not index.exists():index=ROOT/'_catalog/index.json'
    data=decode(json.loads(index.read_text()),index.parent,skill_name=args.skill)
    if not args.skill and (ROOT/'kali-tools/index.json').exists():
        from kali_library import routing_records
        extra=routing_records();existing={r['name'] for r in data['skills']};extra=[r for r in extra if r['name'] not in existing]
        data['skills']+=extra;data['categories'].append({'id':'kali-tools','title':'Kali Tools','count':len(extra)})
        data['skillCount']=len(data['skills'])
    if args.skill:
        skill=next((r for r in data['skills'] if r['name']==args.skill),None)
        if skill is None and (ROOT/'kali-tools/index.json').exists():
            from kali_library import details
            skill=details(args.skill)
        if not skill:p.error('Unknown skill name. Search first for its exact name.')
        if args.read_file:out=read_reference(data,skill,args.read_file,args.max_chars,args.start_line,args.end_line)
        else:
            include={'files':args.files or args.detail,'outline':args.outline or args.detail,'references':args.links or args.detail,'codeBlocks':args.detail}
            out={k:v for k,v in skill.items() if k not in include or include[k]}
            if args.file_match:out['files']=[f for f in out['files'] if norm(args.file_match) in norm(f['path'])]
    elif not any([args.query,args.category,args.missing,args.available_only,args.has_warning,args.tag,args.tool]):
        out={'skills':data['skillCount'],'categories':data['categories'],'usage':'Pass keywords and optional --category/--tag/--tool/--missing/--available-only. Use --skill for one record; add --outline, --links, --files, --detail or --read with optional line ranges.'}
    else:
        if args.category and args.category not in {c['id'] for c in data['categories']}:p.error('Unknown category id.')
        q=norm(' '.join(args.query));tokens=q.split();ranked=[]
        for r in data['skills']:
            if args.category and r['category']!=args.category:continue
            if args.missing and not r['missing']:continue
            if args.available_only and r['missing']:continue
            if args.has_warning and not r['recordedWarning']:continue
            if args.tag and norm(args.tag) not in [norm(t) for t in r['tags']]:continue
            if args.tool and norm(args.tool) not in norm(json.dumps(r['tools'])):continue
            fields=[(norm(r['name']),14),(norm(' '.join(r['tags'])),6),(norm(r['category']+' '+r['categoryTitle']),4),(norm(r['description']),2),(norm(json.dumps(r['tools'])),1),(norm(' '.join(r.get('headings',[]))),2),(norm(' '.join(r.get('searchKeywords',[]))),1),(norm(r.get('searchText','')),1),(norm(json.dumps(r.get('dependencies',{}))),1),(norm(json.dumps(r.get('whenToUse',[]))),1),(norm(r.get('author','')+' '+r.get('compatibility','')),1)]
            if not all(any(t in s for s,w in fields) for t in tokens):continue
            score=sum(w for s,w in fields for t in tokens if t in s)+(100 if q and norm(r['name'])==q else 0)
            ranked.append((score,r))
        ranked.sort(key=lambda pair:(-pair[0],pair[1]['name'].casefold()))
        out={'query':' '.join(args.query),'category':args.category,'matches':len(ranked),'returned':min(args.limit,len(ranked)),'results':[brief(r) for _,r in ranked[:args.limit]]}
    if args.raw:
        if 'content' not in out:raise ValueError('Raw text unavailable for this file.')
        if out.get('truncated'):raise ValueError('Raw output would be truncated; increase --max-chars or select a smaller line range.')
        print(out['content'],end='')
    else:print(json.dumps(out,indent=2,ensure_ascii=False))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,FileNotFoundError,zipfile.BadZipFile) as e:
        print('Error: '+str(e),file=sys.stderr);sys.exit(2)
