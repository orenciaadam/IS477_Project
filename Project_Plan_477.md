# Project Plan — IS 477 Course Project

## 1. Overview
- For our course project, we are exploring the **factors that influence IMDb ratings of Netflix movies**.  
- We will use the **“Netflix IMDb Scores” CSV** as our primary dataset and enrich it with data from the **Open Movie Database (OMDb) API** to gain insights into what leads to a high rating.  
- The API provides additional variables such as `Genre`, `Runtime`, `Language`, `Country`, `Awards`, and `BoxOffice`, which are not available in the static Netflix dataset.  
- Our main goal is to determine which of these characteristics—such as genre or runtime—contribute to higher IMDb ratings.  
- We will use **Python** for cleaning, preprocessing, and integration using a shared primary key (`imdb_id`).  
- Since the sources differ in format (CSV vs JSON), we will build a **clean, reproducible end-to-end workflow** that merges both into one enriched dataset.  
- The final outcome will be a richer, reproducible dataset and analysis that helps explain what influences IMDb ratings on Netflix.  

---

## 2. Research Question(s)
**Primary Question:**  
> What factors influence IMDb audience ratings of Netflix movies?

**Supporting Questions:**
- Does movie runtime correlate with IMDb ratings?  
- Which genres tend to perform better with audiences?  
- Do certain countries or languages produce higher-rated Netflix movies?  
- How do release years and age certifications impact ratings?  

These questions will be explored using **statistical summaries, correlations, and data visualizations** after the datasets are integrated.

---

## 3. Datasets

### **Dataset 1 — Netflix Movies and TV Shows (Kaggle CSV)**
- Static dataset in **CSV** format.  
- Contains information such as `title`, `type`, `release_year`, `runtime`, `age_certification`, `imdb_id`, `imdb_score`, and `imdb_votes`.  
- Serves as the **base dataset** representing Netflix’s catalog of movies and shows.  
- Provides audience ratings (`imdb_score`) but lacks detailed metadata such as genre, language, and country.  
- ~5,283 unique records with 10 columns.

### **Dataset 2 — OMDb API**
- Dynamic dataset retrieved programmatically using **Python’s `requests` library**.  
- Provides **movie metadata** from IMDb, including `Genre`, `Director`, `Runtime`, `Country`, `Language`, `Awards`, and `BoxOffice`.  
- The API enriches the Netflix dataset with additional descriptive and contextual attributes.  
- Integration key: `imdb_id` (shared across both datasets).  
- Data is collected reproducibly, stored as `omdb_results.csv`, and documented for provenance.  
- Includes both numeric and text-based attributes that allow for exploratory analysis (e.g., correlations and descriptive patterns).

---

## 4. Team Roles & Responsibilities
| Team Member | Responsibilities |
|--------------|------------------|
| **Adam** | API data acquisition and cleaning. Write scripts to call the OMDb API, test reproducibility, and store results in a usable pandas DataFrame. |
| **Daniel** | Netflix CSV preparation. Clean columns, handle missing IMDb IDs, standardize titles, and conduct minimal exploratory analysis. |
| **Both** | Responsible for data integration, analysis, visualization, and documentation. Work collaboratively on GitHub for version control, pushing and reviewing code as needed. |

---

## 5. Timeline (Oct – Dec 2025)

| Date Range | Task | Deliverable |
|-------------|------|-------------|
| **Oct 7 – Oct 14** | Submit Project Plan | `ProjectPlan.md` with overview, datasets, and timeline |
| **Oct 15 – Oct 27** | Data acquisition and storage | Fetch OMDb API data reproducibly and clean Netflix CSV |
| **Oct 28 – Nov 5** | Data integration | Merge datasets by `imdb_id`, resolve missing or duplicate values |
| **Nov 6 – Nov 11** | Submit Interim Status Report | `StatusReport.md` summarizing progress and next steps |
| **Nov 12 – Nov 25** | Analysis and visualization | Examine correlations between ratings, runtime, and genre |
| **Nov 26 – Dec 5** | Workflow automation | Build an end-to-end reproducible notebook or script |
| **Dec 6 – Dec 10** | Final submission | Final report (`README.md`), visualizations, and GitHub release |

---

## 6. Constraints
- Our data faces constraints related to **integration quality, availability, and technical limits**.  
- The free OMDb API enforces a **limit of 1,000 calls per day** and returns **10 results per page**, requiring batch requests and local caching for reproducibility.  
- Several OMDb fields (e.g., `BoxOffice`, `Awards`, `Metascore`) may contain missing or inconsistent values, reducing depth for some analyses.  
- Some Netflix entries lack valid IMDb IDs, limiting the join size between datasets.  
- Manual validation may be required to review or correct API mismatches.  
- Despite these constraints, we will **document all limitations** clearly and design our workflow to remain reproducible and transparent.  

---

## 7. Gaps / Areas for Input
- The next step is to **evaluate which OMDb fields are most complete and reliable** for inclusion in the analysis.  
- We plan to test different integration methods to ensure a strong match rate and minimize duplicates between datasets.  
- An open decision remains on whether to emphasize **correlation analysis** (runtime vs rating) or **categorical comparisons** (genres and countries).  
- We will seek input from the instructor or peers on effective visualization formats and reproducibility documentation.  
- As a potential extension, we may explore **text or sentiment analysis** using the Netflix `description` field if time permits.  

---

## Summary
By integrating Netflix’s catalog with detailed OMDb movie data, this project explores how different movie characteristics shape audience perception in a reproducible and transparent workflow for analyzing patterns in IMDb ratings.


