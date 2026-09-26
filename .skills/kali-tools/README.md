# Kali command and package skill collection

**3,339 individually addressable references: 2,766 command skills and 573 package-only skills.**

Coverage comes from all **780 tool pages** linked by the [official Kali all-tools directory](https://www.kali.org/tools/all-tools/), collected on 2026-09-16. Those pages describe **1,489 binary packages**. Every explicit command link and every inline “Includes … command” label in the directory was matched; one additional command heading found on the detailed pages is included as well.

## What was created

Each command has a unique `kali-<source>-<command>` skill name. Each binary package without a published command heading has a separate `...-package` skill. Names are identifiers, not executable spellings; consult the `command` field for the exact published label.

An individual skill provides:

- Official source URL and command/package anchor, source project, binary package, published version and architecture.
- Page update label, retrieval timestamp, source-page SHA-256, Kali categories and metapackage memberships when published.
- Dependencies, installed-size declaration, and the published installation declaration—none executed or verified as installed.
- A short attributed description where retained, plus factual package context.
- Extracted command synopsis and option signatures where recognizable, with an explicit extraction policy and source link for full semantics.
- A bounded task-selection, preflight, verification, evidence, failure-interpretation, stop and cleanup workflow.
- A generated `SKILL.md` view and, for command records, a separate `HELP.txt` interface-reference view.

**These are source-derived, generated references, not thousands of individually hand-audited or execution-tested runbooks.** Command interfaces and page version labels can describe different builds. Some pages publish little useful command documentation; gaps are labeled instead of filled with invented syntax.

High-risk tool families have descriptive/defensive references only. Their operational transcripts are not republished, and the guides do not supply payload deployment, credential theft, covert persistence, or detection-evasion recipes. Ordinary entries still require authorization and environment checks before active use.

## Why plain JSON bundles instead of loose folders?

The existing library was near both workspace snapshot limits: roughly 128 MB and 10,000 files. Adding thousands of loose folders would exceed the file limit. No existing skill files were deleted or replaced.

The new definitions are therefore stored in **ordinary, uncompressed JSON and JSONL**, with one addressable registry record per skill. Shared source/package metadata is stored once. The lookup helper renders one guide at a time. The previously deleted ZIP and template remain absent.

This is **not** a claim that 3,339 new physical `SKILL.md` files were installed. Folder-based skill loaders cannot auto-discover these bundled entries. Export only the selected guide(s) needed for such a loader, into an approved location with sufficient storage.

## Find and read

```bash
python3 /home/user/skills/_catalog/find.py --category kali-tools --limit 10
python3 /home/user/skills/_catalog/find.py nmap --category kali-tools --limit 10
python3 /home/user/skills/_catalog/find.py --skill kali-nmap-nmap --outline
python3 /home/user/skills/_catalog/find.py --skill kali-nmap-nmap --files
python3 /home/user/skills/_catalog/find.py --skill kali-nmap-nmap --read SKILL.md
python3 /home/user/skills/_catalog/find.py --skill kali-nmap-nmap --read HELP.txt
python3 /home/user/skills/_catalog/find.py --skill kali-nmap-nmap --detail
```

`--start-line` and `--end-line` support selective text reads. Output is capped by default. For an explicit text export, `--raw --max-chars 100000` emits the selected text without a JSON wrapper and fails if it would be silently truncated. Choose and approve the destination separately; no bulk export is performed automatically.

## Data files

| File | Purpose |
|---|---|
| [index.json](index.json) | Detailed registry: 780 source records, 1,489 package records, and 3,339 named skill records |
| [skills.csv](skills.csv) | One row per named skill; 26 columns covering source, package, command, dependencies, interfaces, provenance and storage |
| [command-content.jsonl](command-content.jsonl) | Byte-addressed command descriptions/interface facts; one record per command, not executable code |
| [coverage.json](coverage.json) | Coverage counts and unmatched-command results |
| [index.schema.json](index.schema.json) | JSON Schema for the columnar registry |
| [validation.json](validation.json) | Content, source, generated-view and lookup validation results |

The main [library JSON](../_catalog/index.json) links this collection under `collections`. Its shared CSV tables cover physical folder skills; the complete `skills` array is reconstructed by `index_codec.load()` rather than duplicated inside the manifest. Its `discoverableSkillCount` includes bundled collections. The main HTML catalog and search helper combine both.

## JSON structure and joins

`index.json` uses columnar records to avoid repeating field names thousands of times. For each of `sources`, `packages`, and `skills`, zip a row with `rowSchemas[table]` to obtain a dictionary.

```python
import json
from pathlib import Path
index = json.loads(Path('/home/user/skills/kali-tools/index.json').read_text())
skills = [dict(zip(index['rowSchemas']['skills'], row)) for row in index['skills']]
```

- `skills.source` joins `sources.id`.
- `skills.package` joins `packages.id`.
- `sources.url + '#' + skills.anchor` identifies the official published section.
- A command's `contentOffset` and `contentBytes` identify exactly one UTF-8 JSONL record in `command-content.jsonl`. Offsets and lengths are **bytes**, not character positions.
- `contentSha256` verifies that JSONL record, including its newline. The reader checks it before decoding.
- Package-only records have null content offsets and hashes; they do not pretend to have executable help.
- CSV list/dictionary values are compact JSON. Blank values indicate unavailable/not-applicable data. Formula-triggering strings receive an apostrophe prefix; JSON is authoritative for exact string values.

## Important field meanings

- `version`, `architecture`, `installedSize`, `installDeclaration`, `dependencies`: published metadata, not measurements of the local system.
- `categories`, `metapackages`: Kali's labels, not a new security audit or a permission policy.
- `mode`: `bounded-authorized-use`, `reference-only`, or `package-reference`.
- `documentedLongOptions`: extracted interface hints, not exhaustive syntax validation or claims that an option works in the installed build.
- `helpPolicy`: whether interface facts were extracted, documentation was insufficient, or operational material was deliberately not republished.
- `pageSha256`: digest of the fetched page at collection time; not an upstream software-package authenticity check.
- `contentSha256`: integrity of stored reference data, not a security verdict.
- `sourceUpdated` and `retrievedAt`: distinct source-page and collection timestamps. Neither proves a package is current or patched.

Descriptions are limited attributed excerpts plus generated factual context. Full explanatory prose and attack-example sections are not mirrored. Interface signatures are functional reference facts; follow the official source for complete, current documentation. Software licenses are not guessed from the package being listed in Kali.

## Maintenance and validation

- `_catalog/kali_collect.py` retrieves public documentation at a bounded rate; it never runs Kali tools.
- `_catalog/kali_build.py` rebuilds this collection from the temporary page cache.
- `_catalog/build_index.py` rebuilds the physical-skill indexes and combined catalog without recollecting the web.
- Recollection/building requires Beautiful Soup; the installed lookup helper uses the Python standard library only.
- Temporary downloaded HTML is removed after validation to preserve workspace capacity. Rebuilding the Kali collection from source therefore requires recollection.

No tools, services, scanners, drivers, or target-facing workflows were installed or executed while creating this collection.
