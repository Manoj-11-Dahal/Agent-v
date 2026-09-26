"""Generate a schema and field guide for the detailed discovery exports."""
import json
from detail_index import METHODS

def infer(values,key=''):
 if key=='frontmatter':return {'type':'object','description':'Complete declared YAML metadata normalized to JSON; arbitrary original keys retained.','additionalProperties':True}
 types=set();objects=[];arrays=[]
 for v in values:
  if v is None:types.add('null')
  elif isinstance(v,bool):types.add('boolean')
  elif isinstance(v,int):types.add('integer')
  elif isinstance(v,float):types.add('number')
  elif isinstance(v,str):types.add('string')
  elif isinstance(v,dict):types.add('object');objects.append(v)
  elif isinstance(v,list):types.add('array');arrays.extend(v)
 if not types:return {}
 result={'type':next(iter(types)) if len(types)==1 else sorted(types)}
 if objects:
  if key in {'extensions','roles','codeLanguages','referenceStatusCounts'}:result['additionalProperties']={'type':'integer','minimum':0}
  else:
   keys=sorted(set().union(*(v.keys() for v in objects)))
   result['properties']={k:infer([v[k] for v in objects if k in v],k) for k in keys}
   result['required']=sorted(set.intersection(*(set(v) for v in objects)))
   result['additionalProperties']=True
 if 'array' in types:result['items']=infer(arrays)
 if 'string' in types and (key.lower().endswith('sha256') or key.endswith('Fingerprint')):result['pattern']='^[0-9a-f]{64}$'
 return result

def write_docs(data,out,stored=None):
 stored=stored or data
 schema=infer([stored]);schema.update({'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Categorized Skill Discovery Index v4','description':'Discovery metadata only. Current files are measured; missing reference content is not restored or inferred.'})
 schema['properties']['schemaVersion']={'const':4}
 schema['properties']['csvTypes']={'type':'object','additionalProperties':{'type':'object','additionalProperties':{'enum':['string','nullable-string','integer','json','mixed']}}}
 (out/'index.schema.json').write_text(json.dumps(schema,indent=2,ensure_ascii=False)+'\n')
 desc={
 'id':'Stable skill identifier derived from the canonical skill name (SHA-256 prefix); unaffected by category renaming.',
 'name':'Exact canonical skill folder name and declared skill name.',
 'category':'Exact physical category folder; 3D-simulation is case-sensitive.',
 'categoryTitle':'Human-readable category label; existing assignments are preserved.',
 'directory':'Skill directory relative to /home/user/skills.',
 'path':'SKILL.md entry point relative to the library root.',
 'absolutePath':'Current absolute entry-point path in this workspace.',
 'description':'Full declared description; not shortened in these exports.',
 'tags':'Consolidated tags from supported frontmatter locations; raw declarations remain in frontmatter.',
 'author':'Declared author, with existing metadata/owner fallbacks; blank when unavailable.',
 'version':'Declared version, not an inferred upstream revision.',
 'license':'Declared license text, not a legal validation of every file.',
 'compatibility':'Declared compatibility, not a check of installed runtimes.',
 'declaredSource':'Retained source/origin declaration where provided. Deleted repository tracking is not reconstructed.',
 'whenToUse':'Triggers/use-case value from supported metadata locations; all other declarations are retained in frontmatter.',
 'dependencies':'Declared top-level dependencies, depends_on_skill, and depends_on_binary.',
 'tools':'Declared allowed-tools/tools value; not enabled or installed tools.',
 'permissions':'Declared permissions; not permission grants.',
 'inventoryStatus':'reference-incomplete or no-known-missing-files. Neither implies operational readiness.',
 'fileCount':'Total known file locations, including missing references.',
 'availableFileCount':'File locations currently available in the retained library.',
 'missingCount':'Known reference file locations unavailable after archive removal.',
 'packedCount':'Currently packed references; zero after the requested archive deletion.',
 'recordedWarning':'Partial historical installer warning. Blank does not mean safe or scanned.',
 'warningProvenance':'Origin and limits of the retained warning.',
 'searchKeywords':'Up to 48 TF-IDF-selected body terms; automatically extracted retrieval hints.',
 'metadataFields':'JSON Pointer paths to every observed frontmatter leaf, including arrays and empty containers.',
 'frontmatter':'Complete declared metadata object. The decoded JSON view preserves original types and exact strings.',
 'document.title':'First extracted ATX heading, not an inferred title.',
 'document.sha256':'SHA-256 of exact current SKILL.md bytes.',
 'document.bytes':'Current entry-point byte length.',
 'document.characters':'Unicode character count in decoded UTF-8 entry point.',
 'document.lines':'Line count in the full entry point.',
 'document.words':'Whitespace-separated token count; a text statistic, not a model-token count.',
 'document.bodyStartLine':'First body line after the closing frontmatter delimiter, 1-based.',
 'document.frontmatterStartLine':'First YAML content line, excluding the delimiter.',
 'document.frontmatterEndLine':'Last YAML content line, excluding the delimiter.',
 'document.sectionCount':'Count of extracted ATX headings at all levels, outside code fences.',
 'document.codeBlockCount':'Number of extracted fenced code blocks, including unclosed blocks.',
 'document.referenceCount':'Number of extracted links/URL mentions; heuristic, not exhaustive parsing.',
 'document.codeLanguages':'Counts by declared code-fence language/info token, not runtime requirements.',
 'inventory.availableBytes':'Total bytes across currently available files.',
 'inventory.missingHistoricalBytes':'Sum of previously recorded sizes for missing references; not measured current content.',
 'inventory.availableTextFiles':'Available UTF-8-decodable files without NUL bytes.',
 'inventory.availableBinaryOrNonUtf8Files':'Available files not classified as UTF-8 text by this heuristic.',
 'inventory.availableContentFingerprint':'SHA-256 of ordered available path + NUL + file digest + newline records. Not a full upstream package hash.',
 'inventory.extensions':'Counts by filename extension, including missing locations; (none) indicates no extension.',
 'inventory.roles':'Filename-based roles; classification hints, not verified capabilities.',
 'referenceStatusCounts':'Counts of observed local/external/dynamic link statuses.'}
 dictionary={'schemaVersion':4,'root':data['root'],'joinKey':'skills.csv.id = child CSV skillId','methods':METHODS,'tables':{}}
 for file,table in data['tables'].items():
  fields=[]
  for column in table['columns']:
   description=desc.get(column)
   if column.startswith('declared:'):description='Exact frontmatter leaf at JSON Pointer '+column[len('declared:'):]+'. Absent values are blank; full frontmatter disambiguates absent and declared empty values.'
   if not description:description={
    'skillId':'Foreign key to skills.csv.id.', 'skillName':'Exact canonical skill name.', 'entrypoint':'Entry-point path relative to the library root.',
    'libraryPath':'File location relative to the library root.', 'storage':'file or missing in the current retained library.',
    'available':'Whether this file location is currently present.', 'bytes':'Current bytes if available, otherwise the historical archive size.',
    'sizeSource':'current-file-bytes or historical-archive-inventory.', 'extension':'Lowercase filename suffix; blank for extensionless paths.',
    'role':'Heuristic role based on filename/path/extension.', 'mimeType':'Guessed MIME type from extension, not content validation.',
    'sha256':'Current file content digest; null/blank for missing files.', 'contentKind':'text, binary-or-non-utf8, or unavailable.',
    'encoding':'utf-8 when text was decoded; null/blank otherwise.', 'lines':'Current decoded text line count; null/blank when unavailable/non-text.',
    'words':'Whitespace token count; not model tokens.', 'characters':'Unicode text character count; null/blank for unavailable/non-text.',
    'executableBit':'Filesystem executable bit, not permission approval or proof it can run; null/blank if unavailable.',
    'order':'1-based sequence within this skill and this table.', 'level':'ATX heading depth, 1 to 6.', 'title':'Heading text as extracted, or human-readable category title.',
    'startLine':'1-based inclusive source start line.', 'endLine':'1-based inclusive source end line. Sections include nested subsection content.',
    'parentOrder':'Nearest parent heading order; null/blank for top-level headings.', 'line':'1-based source line for this link/mention.',
    'column':'1-based source column of the extracted match.', 'kind':'markdown-link, image, link-definition, or url-mention.',
    'label':'Extracted link label; empty for bare URL mentions.', 'target':'Literal extracted destination; never fetched or executed.',
    'insideCodeBlock':'True for URL mentions found inside a fenced example.', 'resolvedPath':'Resolved library-relative local path, or null for non-local/unresolved destinations.',
    'availability':'available-file, available-directory, missing-indexed, not-found, external-unchecked, fragment-unchecked, dynamic-unchecked, outside-library, or unparsed.',
    'language':'First code-fence info token; blank if unspecified.', 'info':'Complete code-fence info string.', 'closed':'Whether a closing fence was observed.',
    'contentBytes':'Code block body byte count, excluding fence delimiters.', 'contentSha256':'SHA-256 of the exact UTF-8 code-block payload; no code executed.',
    'count':'Number of skills in this category.', 'missingFileCount':'Known missing file locations in this category.', 'incompleteSkills':'Skills with at least one known missing reference.',
    'recordedWarningSkills':'Skills with a retained partial historical warning.', 'availableBytes':'Current available bytes in this category.',
    'missingHistoricalBytes':'Previously recorded sizes of this category’s missing references.', 'directoryPage':'Category Markdown directory path relative to the library root.', 'skillIds':'JSON array of member skill identifiers.'
   }.get(column,'See the corresponding field in index.json; declaration/presence does not confer runtime capability.')
   if file=='files.csv' and column=='path':description='File path relative to its skill directory; use with find.py --skill NAME --read PATH.'
   if file=='categories.csv' and column=='id':description='Exact category folder identifier.'
   fields.append({'name':column,'description':description})
  dictionary['tables'][file]={**table,'fields':fields}
 (out/'data-dictionary.json').write_text(json.dumps(dictionary,indent=2,ensure_ascii=False)+'\n')
 lines=['# Detailed agent discovery indexes','',f"**{data['skillCount']:,} skills · {data['categoryCount']} categories · schema version 4**",'',
 '## Start small, then inspect deeply','',
 '- `quick.json`: a small routing pointer; `find.py` reconstructs search records from shared tables.',
 '- `index.json`: plain JSON manifest describing the shared CSV tables and their types. The decoder returns complete detailed JSON records without storing another copy.',
 '- `skills.csv`: one spreadsheet row per skill. JSON-valued cells retain structured declarations.',
 '- Child CSV tables keep large inventories out of giant cells. Join `skillId` to `skills.csv.id`.',
 '- No full SKILL.md body is duplicated in the index. Use exact paths and line ranges to read the source selectively.',
 '- File hashes are current measurements, not recovered old lock hashes or upstream authenticity evidence.',
 '', '## Current availability','',f"**{data['details']['availableFiles']:,} available files; {data['details']['missingFiles']:,} known missing references.**",
 'The supporting ZIP and template.html remain deleted. Missing content is not reconstructed. Unknown hashes and content statistics are null in JSON and blank in CSV.',
 '', '## Files and row counts','', '| File | Rows | Columns |','|---|---:|---:|']
 for file,t in data['tables'].items():lines.append(f"| [{file}]({file}) | {t['rows']:,} | {t['columnCount']} |")
 lines+=['','## Parsing, security, and interpretation','']
 for key,value in METHODS.items():lines.append(f'- **{key}:** {value}')
 lines+=['','CSV cells beginning with formula-triggering characters, including after whitespace, are prefixed with an apostrophe. The JSON decoder reverses these transport prefixes; overrides handle any ambiguity. Never execute commands just because they appear in these indexes.',
 '', 'All file paths are relative to `/home/user/skills` unless explicitly labeled absolute. `files.csv.path` is relative to the skill directory. References marked `not-found` may be upstream-relative or otherwise context-dependent; they are not added to the historical missing archive count.',
 '', '## Examples','', '```bash',
 'python3 /home/user/skills/_catalog/find.py "shared memory" --limit 5',
 'python3 /home/user/skills/_catalog/find.py --category 3D-simulation --available-only',
 'python3 /home/user/skills/_catalog/find.py --missing --limit 5',
 'python3 /home/user/skills/_catalog/find.py --skill nn-memory-sharing --outline',
 'python3 /home/user/skills/_catalog/find.py --skill godot-master --files',
 'python3 /home/user/skills/_catalog/find.py --skill godot-master --links',
 'python3 /home/user/skills/_catalog/find.py --skill nn-memory-sharing --detail',
 '```', '', 'Rebuild all outputs with `PYTHONDONTWRITEBYTECODE=1 python3 /home/user/skills/_catalog/build_index.py`. Requires PyYAML and the existing catalog.html layout, not the deleted template. This reads skill data but never executes skill code.',
 '', '## JSON structure','', 'The main JSON is a CSV-backed manifest. `recordsTable`, `childTables`, and `csvTypes` identify plain UTF-8 CSV files and their typed columns. Join children by `skillId`; reconstruct full records with `_catalog/index_codec.py`. `recordOverrides` preserves any rare ambiguous CSV values exactly. All detailed CSV rows and columns are retained unchanged; this is normalization, not compression. No declared metadata or child inventory is discarded.', '', 'The main CSV-backed collection covers physical folder skills. Its decoded `skills` array is returned by `index_codec.load()` or by the lookup helper. `collections` links additional individually addressable datasets, including `kali-tools/index.json` and `kali-tools/skills.csv`. `discoverableSkillCount` includes these collections. The search helper and HTML catalog combine both automatically.', '', 'Decoded `skills[]` retains the original routing fields and adds `id`, `frontmatter`, `metadataFields`, `inventoryStatus`, `document`, `inventory`, `outline`, `codeBlocks`, `references`, `referenceStatusCounts`, `metadataStatus`, and `searchKeywords`.',
 '', 'Each decoded `files[]` entry includes current or historical size, availability, classification, exact path, SHA-256 and text statistics when available. Top-level `details` records methods/totals; `tables` describes the CSV exports. `categories[]` includes counts, sizes, and member IDs.',
 '', '[JSON Schema](index.schema.json) describes the observed v4 manifest structure; original frontmatter permits arbitrary declared keys. [Machine-readable field dictionary](data-dictionary.json) contains every CSV column description.',
 '', '## CSV field dictionary','']
 for file,t in dictionary['tables'].items():
  lines += [f'### {file}','','| Column | Meaning |','|---|---|']
  for f in t['fields']:lines.append('| `'+f['name'].replace('|','\\|')+'` | '+f['description'].replace('|','\\|')+' |')
  lines.append('')
 (out/'DATA-DICTIONARY.md').write_text('\n'.join(lines)+'\n')
