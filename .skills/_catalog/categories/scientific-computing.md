# Scientific Computing & Domain Simulation

**20 folder skills** · Category: `scientific-computing`

[Quick index](../../QUICK-INDEX.md) · [Searchable catalog](../../catalog.html) · [Detailed CSV](../skills.csv) · [JSON manifest](../index.json)

Full descriptions and entry-point links are retained here. Detailed metadata, file inventories and outlines are stored once in the shared CSV tables; use the lookup helper to retrieve a selected record as JSON. No tool or permission is enabled by this directory.

`python3 /home/user/skills/_catalog/find.py --category scientific-computing --limit 10`

| Skill / entry point | Description | Available files | Missing | Recorded warning |
|---|---|---:|---:|---|
| <a id="skill-f9a5f587f0c5"></a>[dicom-metadata-extract](../../scientific-computing/dicom-metadata-extract/SKILL.md) | Used for extracting selected metadata from one DICOM file and flagging standard-tag PHI presence. Not for anonymization or clinical use. | 12 | 0 | — |
| <a id="skill-0ae4d7b33b42"></a>[dicom-series-preflight](../../scientific-computing/dicom-series-preflight/SKILL.md) | Used for header-only preflight of one DICOM series folder before conversion or inference. Not for de-identification or clinical clearance. | 10 | 0 | — |
| <a id="skill-9abfe3e2afaf"></a>[dicom-series-to-volume](../../scientific-computing/dicom-series-to-volume/SKILL.md) | Used for converting one CT DICOM series folder to a HU NIfTI volume with affine evidence. Not for multi-frame DICOM or clinical use. | 10 | 0 | — |
| <a id="skill-664cb081d73d"></a>[earth2studio-create-datasource](../../scientific-computing/earth2studio-create-datasource/SKILL.md) | Create and validate Earth2Studio data source wrappers (DataSource, ForecastSource, DataFrameSource, ForecastFrameSource) from remote stores. Do NOT use for fetching data with existing sources, model inference, or installation tasks. | 1 | 18 | — |
| <a id="skill-3a1b1a9834e9"></a>[earth2studio-create-diagnostic](../../scientific-computing/earth2studio-create-diagnostic/SKILL.md) | Create Earth2Studio diagnostic model wrappers for single-step data transformations, including simple derived diagnostics, packaged AutoModel diagnostics, and generative or diffusion diagnostics. Do NOT use for prognostic time-stepping models, data sources, or installation. | 1 | 19 | — |
| <a id="skill-0e77668be610"></a>[earth2studio-create-prognostic](../../scientific-computing/earth2studio-create-prognostic/SKILL.md) | Create Earth2Studio prognostic (time-stepping forecast) model wrappers. Do NOT use for diagnostic models, data sources, or installation. | 1 | 17 | — |
| <a id="skill-e809d6498807"></a>[earth2studio-data-fetch](../../scientific-computing/earth2studio-data-fetch/SKILL.md) | Fetch weather/climate data via Earth2Studio data sources for specific variables and times. Do NOT use for inference pipelines, model discovery, or installation. | 8 | 0 | — |
| <a id="skill-19d24ca84aab"></a>[earth2studio-deterministic-forecast](../../scientific-computing/earth2studio-deterministic-forecast/SKILL.md) | Build deterministic forecast scripts with Earth2Studio (model, data source, IO, inference). Do NOT use for ensemble, diagnostics, data-only fetch, or install. | 12 | 0 | — |
| <a id="skill-811a9e16cc1c"></a>[earth2studio-discover](../../scientific-computing/earth2studio-discover/SKILL.md) | Find Earth2Studio models, data sources, and examples for a weather/climate use case. Do NOT use for writing inference code, downloading data, or installation. | 5 | 0 | — |
| <a id="skill-87976ae5b98c"></a>[earth2studio-install](../../scientific-computing/earth2studio-install/SKILL.md) | Guide installing Earth2Studio via uv or pip, selecting model extras, and configuring the environment. Do NOT use for writing inference code, choosing models, or PhysicsNeMo questions. | 5 | 0 | — |
| <a id="skill-7e52575d5f8c"></a>[medtech-model-evidence-export](../../scientific-computing/medtech-model-evidence-export/SKILL.md) | Exports sanitized metadata, parameters, reproducibility details, quality metrics, and optional review artifacts from Medical AI inference runs or evidence packs to MLflow. Use after inference, including NV-Generate runs; not for live training tracking, model registration, or clinical use. | 15 | 0 | — |
| <a id="skill-af0ceb97571e"></a>[nv-generate-ct-rflow](../../scientific-computing/nv-generate-ct-rflow/SKILL.md) | Used for generating synthetic CT volumes and masks with NV-Generate-CTMR rflow-ct. Not for production training data without review. | 1 | 32 | — |
| <a id="skill-80864b46be40"></a>[nv-generate-mr](../../scientific-computing/nv-generate-mr/SKILL.md) | Used for generating synthetic body MRI volumes with NV-Generate-CTMR rflow-mr. Not for paired masks or production training data. | 14 | 0 | — |
| <a id="skill-66d33a0e9b6c"></a>[nv-generate-mr-brain](../../scientific-computing/nv-generate-mr-brain/SKILL.md) | Used for generating synthetic T1, T2, FLAIR, SWI, or MRA brain MRI volumes with NV-Generate-CTMR MR-Brain v1. Not for production training data. | 15 | 0 | — |
| <a id="skill-87f0775687ff"></a>[nv-generate-mr-brain-finetune](../../scientific-computing/nv-generate-mr-brain-finetune/SKILL.md) | Used for finetuning NV-Generate-CTMR MR-Brain v1 for T1, T2, FLAIR, SWI, or MRA data from a NIfTI datalist. Not for clinical or production data approval. | 12 | 0 | — |
| <a id="skill-5b5774324850"></a>[nv-generate-vae-finetune](../../scientific-computing/nv-generate-vae-finetune/SKILL.md) | Used for finetuning the NV-Generate-CTMR MAISI VAE from CT/MRI NIfTI datalists. Not for clinical or production data approval. | 13 | 0 | — |
| <a id="skill-0d9d6d0f7185"></a>[nv-reason-cxr](../../scientific-computing/nv-reason-cxr/SKILL.md) | Used for command-shape or live NV-Reason-CXR chest X-ray reasoning smoke tests. Not for diagnosis or clinical reporting. | 10 | 0 | — |
| <a id="skill-6e7da40f8dd5"></a>[nv-segment-ct](../../scientific-computing/nv-segment-ct/SKILL.md) | Used for running NV-Segment-CT VISTA3D on CT NIfTI volumes and recording label-map evidence. | 11 | 0 | — |
| <a id="skill-49927516842d"></a>[nv-segment-ct-finetune](../../scientific-computing/nv-segment-ct-finetune/SKILL.md) | Runs standard or fixed-channel softmax finetuning of NV-Segment-CT VISTA3D on CT NIfTI image/label datasets, with optional MONAI-native MLflow tracking and checkpoint evidence. Uses softmax for predefined, mutually exclusive classes; keeps the standard workflow when point prompts or runtime-variable classes are needed. Not for clinical validation. | 11 | 0 | — |
| <a id="skill-df8d5321431b"></a>[nv-segment-ctmr](../../scientific-computing/nv-segment-ctmr/SKILL.md) | Used for running NV-Segment-CTMR on CT or MRI NIfTI volumes and recording label-map evidence. Not for clinical interpretation. | 10 | 0 | — |

A blank warning is not a safety certification. Use `--skill NAME --detail`, `--files`, `--outline`, or `--links` for complete details without loading the entire library.

