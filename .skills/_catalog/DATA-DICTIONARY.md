# Detailed agent discovery indexes

**2,955 skills · 44 categories · schema version 4**

## Start small, then inspect deeply

- `quick.json`: a small routing pointer; `find.py` reconstructs search records from shared tables.
- `index.json`: plain JSON manifest describing the shared CSV tables and their types. The decoder returns complete detailed JSON records without storing another copy.
- `skills.csv`: one spreadsheet row per skill. JSON-valued cells retain structured declarations.
- Child CSV tables keep large inventories out of giant cells. Join `skillId` to `skills.csv.id`.
- No full SKILL.md body is duplicated in the index. Use exact paths and line ranges to read the source selectively.
- File hashes are current measurements, not recovered old lock hashes or upstream authenticity evidence.

## Current availability

**8,657 available files; 7,138 known missing references.**
The supporting ZIP and template.html remain deleted. Missing content is not reconstructed. Unknown hashes and content statistics are null in JSON and blank in CSV.

## Files and row counts

| File | Rows | Columns |
|---|---:|---:|
| [skills.csv](skills.csv) | 2,955 | 158 |
| [files.csv](files.csv) | 15,795 | 16 |
| [sections.csv](sections.csv) | 40,352 | 7 |
| [references.csv](references.csv) | 22,270 | 10 |
| [code-blocks.csv](code-blocks.csv) | 18,397 | 9 |
| [categories.csv](categories.csv) | 44 | 11 |

## Parsing, security, and interpretation

- **content:** Hashes and text statistics are computed from available file bytes. Missing references have historical sizes but null hashes and content statistics.
- **markdown:** Line-based extraction of ATX headings, fenced code blocks, inline links, link definitions and HTTP(S) mentions; not a complete CommonMark parser. Line numbers are 1-based and inclusive.
- **keywords:** Up to 48 automatically selected TF-IDF terms from entry-point body text; retrieval hints, not declared capabilities or exhaustive full-text indexing.
- **references:** Local destinations checked for presence within the library only. External URLs, fragments and dynamic destinations are not validated or fetched.
- **metadata:** All YAML frontmatter fields retained. YAML-specific dates/sets and non-finite numbers normalized to JSON-compatible values. No missing authors, versions, licenses or origins are invented.
- **readiness:** No-known-missing-files means inventory presence only; not runtime readiness, permission approval, security certification, or a completeness guarantee against upstream.
- **csv:** UTF-8, RFC-style CSV quoting; lists/objects encoded as compact JSON. Dangerous spreadsheet strings are prefixed with an apostrophe. The decoded JSON view preserves exact original string values; the manifest defines typed CSV decoding and any necessary overrides.

CSV cells beginning with formula-triggering characters, including after whitespace, are prefixed with an apostrophe. The JSON decoder reverses these transport prefixes; overrides handle any ambiguity. Never execute commands just because they appear in these indexes.

All file paths are relative to `/home/user/skills` unless explicitly labeled absolute. `files.csv.path` is relative to the skill directory. References marked `not-found` may be upstream-relative or otherwise context-dependent; they are not added to the historical missing archive count.

## Examples

```bash
python3 /home/user/skills/_catalog/find.py "shared memory" --limit 5
python3 /home/user/skills/_catalog/find.py --category 3D-simulation --available-only
python3 /home/user/skills/_catalog/find.py --missing --limit 5
python3 /home/user/skills/_catalog/find.py --skill nn-memory-sharing --outline
python3 /home/user/skills/_catalog/find.py --skill godot-master --files
python3 /home/user/skills/_catalog/find.py --skill godot-master --links
python3 /home/user/skills/_catalog/find.py --skill nn-memory-sharing --detail
```

Rebuild all outputs with `PYTHONDONTWRITEBYTECODE=1 python3 /home/user/skills/_catalog/build_index.py`. Requires PyYAML and the existing catalog.html layout, not the deleted template. This reads skill data but never executes skill code.

## JSON structure

The main JSON is a CSV-backed manifest. `recordsTable`, `childTables`, and `csvTypes` identify plain UTF-8 CSV files and their typed columns. Join children by `skillId`; reconstruct full records with `_catalog/index_codec.py`. `recordOverrides` preserves any rare ambiguous CSV values exactly. All detailed CSV rows and columns are retained unchanged; this is normalization, not compression. No declared metadata or child inventory is discarded.

The main CSV-backed collection covers physical folder skills. Its decoded `skills` array is returned by `index_codec.load()` or by the lookup helper. `collections` links additional individually addressable datasets, including `kali-tools/index.json` and `kali-tools/skills.csv`. `discoverableSkillCount` includes these collections. The search helper and HTML catalog combine both automatically.

Decoded `skills[]` retains the original routing fields and adds `id`, `frontmatter`, `metadataFields`, `inventoryStatus`, `document`, `inventory`, `outline`, `codeBlocks`, `references`, `referenceStatusCounts`, `metadataStatus`, and `searchKeywords`.

Each decoded `files[]` entry includes current or historical size, availability, classification, exact path, SHA-256 and text statistics when available. Top-level `details` records methods/totals; `tables` describes the CSV exports. `categories[]` includes counts, sizes, and member IDs.

[JSON Schema](index.schema.json) describes the observed v4 manifest structure; original frontmatter permits arbitrary declared keys. [Machine-readable field dictionary](data-dictionary.json) contains every CSV column description.

## CSV field dictionary

### skills.csv

| Column | Meaning |
|---|---|
| `id` | Stable skill identifier derived from the canonical skill name (SHA-256 prefix); unaffected by category renaming. |
| `name` | Exact canonical skill folder name and declared skill name. |
| `category` | Exact physical category folder; 3D-simulation is case-sensitive. |
| `categoryTitle` | Human-readable category label; existing assignments are preserved. |
| `directory` | Skill directory relative to /home/user/skills. |
| `path` | SKILL.md entry point relative to the library root. |
| `absolutePath` | Current absolute entry-point path in this workspace. |
| `description` | Full declared description; not shortened in these exports. |
| `tags` | Consolidated tags from supported frontmatter locations; raw declarations remain in frontmatter. |
| `author` | Declared author, with existing metadata/owner fallbacks; blank when unavailable. |
| `version` | Declared version, not an inferred upstream revision. |
| `license` | Declared license text, not a legal validation of every file. |
| `compatibility` | Declared compatibility, not a check of installed runtimes. |
| `declaredSource` | Retained source/origin declaration where provided. Deleted repository tracking is not reconstructed. |
| `whenToUse` | Triggers/use-case value from supported metadata locations; all other declarations are retained in frontmatter. |
| `dependencies` | Declared top-level dependencies, depends_on_skill, and depends_on_binary. |
| `tools` | Declared allowed-tools/tools value; not enabled or installed tools. |
| `permissions` | Declared permissions; not permission grants. |
| `inventoryStatus` | reference-incomplete or no-known-missing-files. Neither implies operational readiness. |
| `fileCount` | Total known file locations, including missing references. |
| `availableFileCount` | File locations currently available in the retained library. |
| `missingCount` | Known reference file locations unavailable after archive removal. |
| `packedCount` | Currently packed references; zero after the requested archive deletion. |
| `recordedWarning` | Partial historical installer warning. Blank does not mean safe or scanned. |
| `warningProvenance` | Origin and limits of the retained warning. |
| `searchKeywords` | Up to 48 TF-IDF-selected body terms; automatically extracted retrieval hints. |
| `metadataFields` | JSON Pointer paths to every observed frontmatter leaf, including arrays and empty containers. |
| `frontmatter` | Complete declared metadata object. The decoded JSON view preserves original types and exact strings. |
| `document.title` | First extracted ATX heading, not an inferred title. |
| `document.sha256` | SHA-256 of exact current SKILL.md bytes. |
| `document.bytes` | Current entry-point byte length. |
| `document.characters` | Unicode character count in decoded UTF-8 entry point. |
| `document.lines` | Line count in the full entry point. |
| `document.words` | Whitespace-separated token count; a text statistic, not a model-token count. |
| `document.bodyStartLine` | First body line after the closing frontmatter delimiter, 1-based. |
| `document.frontmatterStartLine` | First YAML content line, excluding the delimiter. |
| `document.frontmatterEndLine` | Last YAML content line, excluding the delimiter. |
| `document.sectionCount` | Count of extracted ATX headings at all levels, outside code fences. |
| `document.codeBlockCount` | Number of extracted fenced code blocks, including unclosed blocks. |
| `document.referenceCount` | Number of extracted links/URL mentions; heuristic, not exhaustive parsing. |
| `document.codeLanguages` | Counts by declared code-fence language/info token, not runtime requirements. |
| `inventory.availableBytes` | Total bytes across currently available files. |
| `inventory.missingHistoricalBytes` | Sum of previously recorded sizes for missing references; not measured current content. |
| `inventory.availableTextFiles` | Available UTF-8-decodable files without NUL bytes. |
| `inventory.availableBinaryOrNonUtf8Files` | Available files not classified as UTF-8 text by this heuristic. |
| `inventory.availableContentFingerprint` | SHA-256 of ordered available path + NUL + file digest + newline records. Not a full upstream package hash. |
| `inventory.extensions` | Counts by filename extension, including missing locations; (none) indicates no extension. |
| `inventory.roles` | Filename-based roles; classification hints, not verified capabilities. |
| `referenceStatusCounts` | Counts of observed local/external/dynamic link statuses. |
| `declared:/acknowledgments` | Exact frontmatter leaf at JSON Pointer /acknowledgments. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/allowed-tools` | Exact frontmatter leaf at JSON Pointer /allowed-tools. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/argument` | Exact frontmatter leaf at JSON Pointer /argument. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/argument-hint` | Exact frontmatter leaf at JSON Pointer /argument-hint. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/author` | Exact frontmatter leaf at JSON Pointer /author. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/category` | Exact frontmatter leaf at JSON Pointer /category. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/compatibility` | Exact frontmatter leaf at JSON Pointer /compatibility. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/context` | Exact frontmatter leaf at JSON Pointer /context. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/data_classification` | Exact frontmatter leaf at JSON Pointer /data_classification. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/dependencies` | Exact frontmatter leaf at JSON Pointer /dependencies. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/depends_on_binary` | Exact frontmatter leaf at JSON Pointer /depends_on_binary. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/depends_on_skill` | Exact frontmatter leaf at JSON Pointer /depends_on_skill. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/description` | Exact frontmatter leaf at JSON Pointer /description. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/disable-model-invocation` | Exact frontmatter leaf at JSON Pointer /disable-model-invocation. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/effort` | Exact frontmatter leaf at JSON Pointer /effort. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/evals` | Exact frontmatter leaf at JSON Pointer /evals. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/infer` | Exact frontmatter leaf at JSON Pointer /infer. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/license` | Exact frontmatter leaf at JSON Pointer /license. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata.hermes.tags` | Exact frontmatter leaf at JSON Pointer /metadata.hermes.tags. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/abstract` | Exact frontmatter leaf at JSON Pointer /metadata/abstract. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/agents` | Exact frontmatter leaf at JSON Pointer /metadata/agents. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/argument-hint` | Exact frontmatter leaf at JSON Pointer /metadata/argument-hint. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/artifact` | Exact frontmatter leaf at JSON Pointer /metadata/artifact. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/author` | Exact frontmatter leaf at JSON Pointer /metadata/author. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/author_contact` | Exact frontmatter leaf at JSON Pointer /metadata/author_contact. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/author_url` | Exact frontmatter leaf at JSON Pointer /metadata/author_url. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/blast-radius` | Exact frontmatter leaf at JSON Pointer /metadata/blast-radius. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/category` | Exact frontmatter leaf at JSON Pointer /metadata/category. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/classification` | Exact frontmatter leaf at JSON Pointer /metadata/classification. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/compatibility` | Exact frontmatter leaf at JSON Pointer /metadata/compatibility. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/compatible_with` | Exact frontmatter leaf at JSON Pointer /metadata/compatible_with. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/data-classification` | Exact frontmatter leaf at JSON Pointer /metadata/data-classification. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/data_classification` | Exact frontmatter leaf at JSON Pointer /metadata/data_classification. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/date` | Exact frontmatter leaf at JSON Pointer /metadata/date. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/docs` | Exact frontmatter leaf at JSON Pointer /metadata/docs. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/domain` | Exact frontmatter leaf at JSON Pointer /metadata/domain. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/endpoint-openapi-schemas` | Exact frontmatter leaf at JSON Pointer /metadata/endpoint-openapi-schemas. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/environment` | Exact frontmatter leaf at JSON Pointer /metadata/environment. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/frameworks` | Exact frontmatter leaf at JSON Pointer /metadata/frameworks. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/github-url` | Exact frontmatter leaf at JSON Pointer /metadata/github-url. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/hsb_ip_version` | Exact frontmatter leaf at JSON Pointer /metadata/hsb_ip_version. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/interactive` | Exact frontmatter leaf at JSON Pointer /metadata/interactive. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/kind` | Exact frontmatter leaf at JSON Pointer /metadata/kind. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/languages` | Exact frontmatter leaf at JSON Pointer /metadata/languages. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/min-flare-version` | Exact frontmatter leaf at JSON Pointer /metadata/min-flare-version. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/min_compat_rev` | Exact frontmatter leaf at JSON Pointer /metadata/min_compat_rev. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/next_skill` | Exact frontmatter leaf at JSON Pointer /metadata/next_skill. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/organization` | Exact frontmatter leaf at JSON Pointer /metadata/organization. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/output-format` | Exact frontmatter leaf at JSON Pointer /metadata/output-format. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/owner` | Exact frontmatter leaf at JSON Pointer /metadata/owner. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/package` | Exact frontmatter leaf at JSON Pointer /metadata/package. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/permissions` | Exact frontmatter leaf at JSON Pointer /metadata/permissions. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/permissions/file_read` | Exact frontmatter leaf at JSON Pointer /metadata/permissions/file_read. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/permissions/file_write` | Exact frontmatter leaf at JSON Pointer /metadata/permissions/file_write. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/permissions/shell` | Exact frontmatter leaf at JSON Pointer /metadata/permissions/shell. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/portable` | Exact frontmatter leaf at JSON Pointer /metadata/portable. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/previous_skill` | Exact frontmatter leaf at JSON Pointer /metadata/previous_skill. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/related-skills` | Exact frontmatter leaf at JSON Pointer /metadata/related-skills. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/requires` | Exact frontmatter leaf at JSON Pointer /metadata/requires. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/reviewed` | Exact frontmatter leaf at JSON Pointer /metadata/reviewed. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/risk_tier` | Exact frontmatter leaf at JSON Pointer /metadata/risk_tier. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/role` | Exact frontmatter leaf at JSON Pointer /metadata/role. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/scope` | Exact frontmatter leaf at JSON Pointer /metadata/scope. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/service` | Exact frontmatter leaf at JSON Pointer /metadata/service. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/short-description` | Exact frontmatter leaf at JSON Pointer /metadata/short-description. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/source_artifact` | Exact frontmatter leaf at JSON Pointer /metadata/source_artifact. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/stage` | Exact frontmatter leaf at JSON Pointer /metadata/stage. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/status` | Exact frontmatter leaf at JSON Pointer /metadata/status. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/tags` | Exact frontmatter leaf at JSON Pointer /metadata/tags. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/team` | Exact frontmatter leaf at JSON Pointer /metadata/team. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/three-version` | Exact frontmatter leaf at JSON Pointer /metadata/three-version. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/tool-version` | Exact frontmatter leaf at JSON Pointer /metadata/tool-version. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/triggers` | Exact frontmatter leaf at JSON Pointer /metadata/triggers. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/upstream` | Exact frontmatter leaf at JSON Pointer /metadata/upstream. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/upstream/branch` | Exact frontmatter leaf at JSON Pointer /metadata/upstream/branch. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/upstream/index_skill` | Exact frontmatter leaf at JSON Pointer /metadata/upstream/index_skill. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/upstream/index_skill_name` | Exact frontmatter leaf at JSON Pointer /metadata/upstream/index_skill_name. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/upstream/repo` | Exact frontmatter leaf at JSON Pointer /metadata/upstream/repo. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/upstream/sibling_skills` | Exact frontmatter leaf at JSON Pointer /metadata/upstream/sibling_skills. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/upstream/skills_dir` | Exact frontmatter leaf at JSON Pointer /metadata/upstream/skills_dir. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/upstream/skills_dir_alias` | Exact frontmatter leaf at JSON Pointer /metadata/upstream/skills_dir_alias. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/upstream_clone_path` | Exact frontmatter leaf at JSON Pointer /metadata/upstream_clone_path. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/upstream_override_env` | Exact frontmatter leaf at JSON Pointer /metadata/upstream_override_env. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/use-cases` | Exact frontmatter leaf at JSON Pointer /metadata/use-cases. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/vendor` | Exact frontmatter leaf at JSON Pointer /metadata/vendor. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/metadata/version` | Exact frontmatter leaf at JSON Pointer /metadata/version. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/name` | Exact frontmatter leaf at JSON Pointer /name. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/origin` | Exact frontmatter leaf at JSON Pointer /origin. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/owner` | Exact frontmatter leaf at JSON Pointer /owner. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/paths` | Exact frontmatter leaf at JSON Pointer /paths. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/permissions` | Exact frontmatter leaf at JSON Pointer /permissions. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/permissions/env` | Exact frontmatter leaf at JSON Pointer /permissions/env. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/permissions/file_read` | Exact frontmatter leaf at JSON Pointer /permissions/file_read. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/permissions/file_write` | Exact frontmatter leaf at JSON Pointer /permissions/file_write. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/permissions/network` | Exact frontmatter leaf at JSON Pointer /permissions/network. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/permissions/shell/allowed_scripts` | Exact frontmatter leaf at JSON Pointer /permissions/shell/allowed_scripts. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/reviewed` | Exact frontmatter leaf at JSON Pointer /reviewed. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/service` | Exact frontmatter leaf at JSON Pointer /service. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/severity` | Exact frontmatter leaf at JSON Pointer /severity. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/source` | Exact frontmatter leaf at JSON Pointer /source. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/tags` | Exact frontmatter leaf at JSON Pointer /tags. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/title` | Exact frontmatter leaf at JSON Pointer /title. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/tools` | Exact frontmatter leaf at JSON Pointer /tools. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/triggers` | Exact frontmatter leaf at JSON Pointer /triggers. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/user-invocable` | Exact frontmatter leaf at JSON Pointer /user-invocable. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/user_invocable` | Exact frontmatter leaf at JSON Pointer /user_invocable. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/version` | Exact frontmatter leaf at JSON Pointer /version. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/when-to-use` | Exact frontmatter leaf at JSON Pointer /when-to-use. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |
| `declared:/when_to_use` | Exact frontmatter leaf at JSON Pointer /when_to_use. Absent values are blank; full frontmatter disambiguates absent and declared empty values. |

### files.csv

| Column | Meaning |
|---|---|
| `skillId` | Foreign key to skills.csv.id. |
| `path` | File path relative to its skill directory; use with find.py --skill NAME --read PATH. |
| `storage` | file or missing in the current retained library. |
| `available` | Whether this file location is currently present. |
| `bytes` | Current bytes if available, otherwise the historical archive size. |
| `sizeSource` | current-file-bytes or historical-archive-inventory. |
| `extension` | Lowercase filename suffix; blank for extensionless paths. |
| `role` | Heuristic role based on filename/path/extension. |
| `mimeType` | Guessed MIME type from extension, not content validation. |
| `sha256` | Current file content digest; null/blank for missing files. |
| `contentKind` | text, binary-or-non-utf8, or unavailable. |
| `encoding` | utf-8 when text was decoded; null/blank otherwise. |
| `lines` | Current decoded text line count; null/blank when unavailable/non-text. |
| `words` | Whitespace token count; not model tokens. |
| `characters` | Unicode text character count; null/blank for unavailable/non-text. |
| `executableBit` | Filesystem executable bit, not permission approval or proof it can run; null/blank if unavailable. |

### sections.csv

| Column | Meaning |
|---|---|
| `skillId` | Foreign key to skills.csv.id. |
| `order` | 1-based sequence within this skill and this table. |
| `level` | ATX heading depth, 1 to 6. |
| `title` | Heading text as extracted, or human-readable category title. |
| `startLine` | 1-based inclusive source start line. |
| `endLine` | 1-based inclusive source end line. Sections include nested subsection content. |
| `parentOrder` | Nearest parent heading order; null/blank for top-level headings. |

### references.csv

| Column | Meaning |
|---|---|
| `skillId` | Foreign key to skills.csv.id. |
| `order` | 1-based sequence within this skill and this table. |
| `line` | 1-based source line for this link/mention. |
| `column` | 1-based source column of the extracted match. |
| `kind` | markdown-link, image, link-definition, or url-mention. |
| `label` | Extracted link label; empty for bare URL mentions. |
| `target` | Literal extracted destination; never fetched or executed. |
| `insideCodeBlock` | True for URL mentions found inside a fenced example. |
| `resolvedPath` | Resolved library-relative local path, or null for non-local/unresolved destinations. |
| `availability` | available-file, available-directory, missing-indexed, not-found, external-unchecked, fragment-unchecked, dynamic-unchecked, outside-library, or unparsed. |

### code-blocks.csv

| Column | Meaning |
|---|---|
| `skillId` | Foreign key to skills.csv.id. |
| `order` | 1-based sequence within this skill and this table. |
| `language` | First code-fence info token; blank if unspecified. |
| `info` | Complete code-fence info string. |
| `startLine` | 1-based inclusive source start line. |
| `endLine` | 1-based inclusive source end line. Sections include nested subsection content. |
| `closed` | Whether a closing fence was observed. |
| `contentBytes` | Code block body byte count, excluding fence delimiters. |
| `contentSha256` | SHA-256 of the exact UTF-8 code-block payload; no code executed. |

### categories.csv

| Column | Meaning |
|---|---|
| `id` | Exact category folder identifier. |
| `title` | Heading text as extracted, or human-readable category title. |
| `count` | Number of skills in this category. |
| `availableFileCount` | File locations currently available in the retained library. |
| `missingFileCount` | Known missing file locations in this category. |
| `incompleteSkills` | Skills with at least one known missing reference. |
| `recordedWarningSkills` | Skills with a retained partial historical warning. |
| `availableBytes` | Current available bytes in this category. |
| `missingHistoricalBytes` | Previously recorded sizes of this category’s missing references. |
| `directoryPage` | Category Markdown directory path relative to the library root. |
| `skillIds` | JSON array of member skill identifiers. |

