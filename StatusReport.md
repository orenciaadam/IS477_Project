# Status Report

## Overview of Planned Work
Reflecting on Milestone 2, our project plan outlined an approach to investigate factors that influence IMDb ratings of Netflix movies by integrating two data sources: the Netflix IMDb dataset from Kaggle and the OMDb API. Planned tasks included reproducible data acquisition, structured storage, data cleaning, merging using a shared primary key (IMDb ID), and preliminary data analysis. In this milestone, we focused on strengthening reproducibility in our workflow and aligning each step with the complete data lifecycle.

## Data Acquisition & Storage

### Netflix Dataset
- Downloaded and placed under `data/raw/`
- Includes attributes such as:
  - `title`
  - `type`
  - `release_year`
  - `age_certification`
  - `runtime`
  - `imdb_id`
  - `imdb_score`
  - `imdb_votes`

### OMDb API Dataset
- Retrieved using `scripts/fetch_omdb.py`
- Uses IMDb IDs for consistent linkage
- Raw responses stored in `omdb_raw.jsonl` for provenance
- Selected attributes exported to `omdb_from_netflix.csv`
- API keys securely handled through ignored local config files

## Data Cleaning & Primary Key Preparation
Initial preprocessing of the Netflix dataset used `scripts/clean_netflix.py`:

- Filters rows with valid IMDb IDs  
- Standardizes IMDb ID formatting  
- Outputs:
  - `netflix_clean.csv`
  - `netflix_imdb_ids.csv`

These cleaned IDs were passed into the OMDb retrieval workflow for reproducibility.

## Data Integration
We performed an inner join on `imdb_id`, validating:

- Primary key compatibility  
- Alignment of OMDb attributes with Netflix titles  
- Value added by OMDb-enriched metadata  

The merged dataset now contains combined fields from both sources.

## Data Cleaning & Quality Assessment (In Progress)

### Standardization & Variable Preparation
- Converted OMDb runtimes to numeric minutes and unified with Netflix runtimes
- Parsed complex numerical fields (`imdbVotes`, `BoxOffice`) into float-compatible formats
- Identified sparse fields (`Awards`, `Metascore`)
- Resolved redundant fields (e.g., `title` vs `Title`) using `title_unified` and `release_year_clean`

These efforts address inconsistencies and missing-data issues identified in Milestone 2.

## Challenges Encountered
OMDb API free-tier rate limits affected data acquisition:

- Limited initial pulls to 25 → 200 titles  
- Implemented safe-failure logic and rate-limit handling  
- Ensured partial datasets remained reproducible  

The smaller sample still provides adequate coverage for exploratory work.

## Existing Artifacts in Repository
- `scripts/clean_netflix.py`  
- `scripts/fetch_omdb.py`  
- `data/raw/`  
- `data/processed/`  
- Jupyter notebooks for exploration and validation  

## Timeline (Oct – Dec 2025)

| Date Range | Task | Deliverable |
|-----------|-------|-------------|
| Oct 7–14 | Submit Project Plan | `ProjectPlan.md` |
| Oct 15–27 | Data acquisition & storage | OMDb fetch + Netflix cleaning |
| Oct 28–Nov 5 | Data integration | Join on `imdb_id` |
| Nov 6–11 | Interim Status Report | `StatusReport.md` |
| Nov 12–25 | Continued API acquisition | Expand OMDb sample |
| Nov 25–28 | Analysis & visualization | Exploratory analysis |
| Nov 28–Dec 5 | Workflow automation | Reproducible pipeline |
| Dec 6–10 | Final submission | Final report + visuals |

Primary adjustments involved scaling the OMDb acquisition and adding explicit documentation for ethical data handling.

## Ethical Data Handling & Licensing Compliance

### OMDb API
- Licensed under CC BY-NC 4.0  
- Attribution included  
- Non-commercial use only  
- Raw data preserved for transparency  

### Netflix IMDb Scores Dataset (Kaggle)
- Academic use only  
- Proper attribution provided  
- No redistribution  

### Responsible Data Practices
- API keys protected via `.gitignore`  
- Raw vs processed data separated  
- Version control ensures transparency  
- All transformations documented  

## Data Lifecycle Alignment
**Planning → Acquisition → Cleaning → Integration → Analysis → Documentation**

Our workflow follows the complete data lifecycle to ensure transparency and reproducibility.

## License References
- https://creativecommons.org/licenses/by-nc/4.0/  
- https://www.kaggle.com/datasets/thedevastator/netflix-imdb-scores  

## Team Member Contribution Summary

### Daniel Newman
- Led Netflix preprocessing (`Clean.ipynb`)
- Conducted exploratory analysis (`Open_NTSM.ipynb`)
- Extracted & standardized IMDb IDs (`Primary_key.ipynb`)
- Performed data quality checks
- Drafted `StatusReport.md`
- Prepared structured outputs for OMDb workflow

### Adam Orencia
- Built OMDb ingestion workflow (`fetch_omdb.py`)
- Implemented rate-limit handling & safe requests
- Structured reproducible directory layout
- Managed secure API key configuration
- Assisted in integration & pipeline troubleshooting
