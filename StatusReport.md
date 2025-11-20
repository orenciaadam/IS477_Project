Status Report
Overview of Planned Work

Reflecting on Milestone 2, our project plan outlined an approach to investigate factors that influence IMDb ratings of Netflix movies by integrating two data sources: the Netflix IMDb dataset from Kaggle and the OMDb API. Planned tasks included reproducible data acquisition, structured storage, data cleaning, merging using a shared primary key (IMDb ID), and preliminary data analysis. In this milestone, we focused on strengthening reproducibility in our workflow and aligning each step with the complete data lifecycle.

Data Acquisition & Storage

As planned, we successfully obtained and stored both datasets in a structured, reproducible manner.

Netflix Dataset

Downloaded and placed under data/raw/.

Includes base attributes such as title, type, release_year, age_certification, runtime, imdb_id, imdb_score, and imdb_votes.

OMDb API Dataset

Retrieved using a custom ingestion workflow in scripts/fetch_omdb.py.

Uses IMDb IDs as lookup keys to ensure consistent linkage between datasets.

Raw responses stored in omdb_raw.jsonl to preserve provenance.

Processed attributes (e.g., Genre, Runtime, Country, Awards, BoxOffice) exported to omdb_from_netflix.csv.

API authentication is securely handled through local configuration files excluded via .gitignore.

Data Cleaning & Primary Key Preparation

Initial preprocessing of the Netflix dataset was performed using scripts/clean_netflix.py.
This script:

Filters rows with valid IMDb IDs.

Standardizes IMDb ID formatting.

Produces two outputs:

netflix_clean.csv — cleaned dataset

netflix_imdb_ids.csv — deduplicated primary-key list

These cleaned IDs were then passed directly into the OMDb retrieval process to strengthen consistency and reproducibility.

Data Integration

We completed a test integration of both datasets using an inner join on imdb_id, validating:

The compatibility of the primary key,

Proper alignment of OMDb attributes with Netflix titles,

The ability of enriched fields to expand analytical opportunities.

The merged dataset now includes both Netflix fields and OMDb-enriched attributes.

Data Cleaning & Quality Assessment (In Progress)

Completed steps include:

Standardization & Variable Preparation

Converted string-based OMDb runtimes into numeric values and reconciled them with Netflix runtimes into a unified runtime_min field.

Transformed complex numeric fields (imdbVotes, BoxOffice) into float-compatible formats.

Identified null-heavy fields (e.g., Awards, Metascore) to inform later analytic decisions.

Resolved redundant fields across sources (e.g., title vs. Title, release_year vs. Year) by creating standardized variables such as title_unified and release_year_clean.

These steps directly address formatting inconsistencies and missing-data patterns identified during Milestone 2.

Challenges Encountered

OMDb’s free-tier API limits were the largest deviation from our original plan. Daily request caps halted early acquisition attempts, requiring us to:

Limit enrichment to smaller samples (initially 25, then 200),

Implement rate-limit detection and safe-failure logic,

Build the workflow such that partial data remains valid and reproducible.

Despite reduced coverage, the sample provides adequate data for exploratory analysis and workflow validation.

Existing Artifacts in Repository

Current technical artifacts include:

scripts/clean_netflix.py — Netflix preprocessing

scripts/fetch_omdb.py — OMDb ingestion

data/raw/ — raw datasets + provenance

data/processed/ — cleaned and integrated datasets

Jupyter notebooks for exploratory cleaning & validation

These artifacts demonstrate measured progress toward our full lifecycle pipeline.

Timeline (Oct – Dec 2025)
Date Range	Task	Deliverable
Oct 7 – Oct 14	Submit Project Plan	ProjectPlan.md
Oct 15 – Oct 27	Data acquisition and storage	OMDb fetch + Netflix cleaning
Oct 28 – Nov 5	Data integration	Join on imdb_id, resolve duplicates
Nov 6 – Nov 11	Interim Status Report	StatusReport.md
Nov 12 – Nov 25	Continued API acquisition	Expand OMDb sample
Nov 25 – Nov 28	Analysis & visualization	Exploratory analysis
Nov 28 – Dec 5	Workflow automation	End-to-end reproducible pipeline
Dec 6 – Dec 10	Final submission	Final report + visualizations

Our primary adjustment involves scaling API acquisition. Because full retrieval was slower than expected, we began with a 200-title sample to build and validate the full pipeline before scaling to all 5,000 rows.

We also identified an oversight in our original plan: ethical data considerations. Although our datasets are public and non-personal, we revised documentation to explicitly address licensing and responsible data use.

Ethical Data Handling & Licensing Compliance
OMDb API

Licensed under CC BY-NC 4.0 (non-commercial required).

Attribution provided along with license references.

Raw responses are stored to preserve transparency.

Netflix IMDb Scores Dataset (Kaggle)

Used solely for academic and non-commercial purposes.

No redistribution or commercialization.

Attribution provided to the dataset creator.

Responsible Data Practices Implemented

API keys stored locally and protected via .gitignore.

Separation of raw vs. processed data ensures provenance.

GitHub is used for transparent version control.

All transformations are documented.

Data Lifecycle Alignment

Planning → Acquisition → Cleaning → Integration → Analysis → Documentation

Our project intentionally follows the complete data lifecycle to ensure reproducibility, transparency, and responsible data management.

License References

OMDb License: https://creativecommons.org/licenses/by-nc/4.0/

Kaggle Dataset: https://www.kaggle.com/datasets/thedevastator/netflix-imdb-scores

Team Member Contribution Summary
Daniel Newman

Led preprocessing of Netflix dataset (Clean.ipynb).

Conducted structural and exploratory analysis (Open_NTSM.ipynb).

Identified and standardized IMDb IDs (Primary_key.ipynb).

Performed data quality checks (missing values, formatting).

Drafted project documentation including StatusReport.md.

Prepared structured output for OMDb integration.

Adam Orencia

Developed the OMDb ingestion workflow (fetch_omdb.py).

Implemented rate-limit handling and safe API request logic.

Structured the reproducible directory system.

Managed secure API key configuration.

Assisted with dataset integration and troubleshooting.