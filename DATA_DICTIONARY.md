# Data Dictionary

## Dataset Overview
This dictionary describes the merged dataset combining Netflix metadata from Kaggle with enriched movie information from the OMDb API.

---

## Netflix Dataset Fields (Source: Kaggle)

| Variable | Type | Description |
|----------|------|-------------|
| index | integer | Row index from original Netflix dataset |
| id | string | Netflix internal identifier |
| title | string | Movie title (Netflix version) |
| type | string | Content type (always MOVIE in this dataset) |
| description | string | Netflix's plot summary/synopsis |
| release_year | integer | Year the movie was released |
| age_certification | string | Age rating/certification (e.g., R, PG, G) |
| runtime | integer | Runtime in minutes (Netflix data) |
| imdb_id | string | IMDb unique identifier (primary key) |
| imdb_score | float | IMDb rating from Netflix dataset (0-10 scale) |
| imdb_votes | float | Number of IMDb votes from Netflix dataset |

---

## OMDb API Fields (Source: OMDb API)

### Basic Information
| Variable | Type | Description |
|----------|------|-------------|
| Title | string | Movie title from OMDb |
| Year | string | Release year from OMDb |
| Rated | string | MPAA rating (e.g., R, PG-13, G) |
| Released | string | Release date (formatted string) |
| Runtime | string | Runtime with units (e.g., "114 min") |
| Type | string | Media type (e.g., "movie") |

### Creative Information
| Variable | Type | Description |
|----------|------|-------------|
| Genre | string | Comma-separated list of genres |
| Director | string | Director name(s) |
| Writer | string | Writer name(s) |
| Actors | string | Main actors (comma-separated) |
| Plot | string | Movie plot summary from OMDb |
| Language | string | Languages spoken in film |
| Country | string | Country/countries of production |

### Awards and Ratings
| Variable | Type | Description |
|----------|------|-------------|
| Awards | string | Awards won or nominated for |
| Ratings | string | JSON-formatted list of ratings from various sources |
| Metascore | float | Metascore rating (0-100 scale) |
| imdbRating | string | IMDb rating from OMDb (string format) |
| imdbVotes | string | Vote count with comma formatting |
| imdbID | string | IMDb identifier (duplicate of imdb_id) |

### Additional Metadata
| Variable | Type | Description |
|----------|------|-------------|
| Poster | string | URL to movie poster image |
| DVD | string | DVD release date |
| BoxOffice | string | Box office earnings (currency formatted) |
| Production | string | Production company |
| Website | string | Official movie website |

---

## Cleaned/Derived Fields (Created during data processing)

| Variable | Type | Description | Source Script |
|----------|------|-------------|---------------|
| runtime_minutes | integer | Parsed runtime in minutes (numeric) | 03_clean_omdb.py |
| imdbRating_clean | float | Numeric IMDb rating (0-10 scale) | 03_clean_omdb.py |
| imdbVotes_clean | integer | Parsed vote count (commas removed) | 03_clean_omdb.py |
| Metascore_clean | integer | Numeric Metascore (0-100 scale) | 03_clean_omdb.py |
| Year_clean | integer | Numeric release year | 03_clean_omdb.py |

---

## Data Quality Notes

- **Missing Values:** Awards, Metascore, BoxOffice, Production, Website fields frequently contain null or "N/A" values
- **Primary Key:** `imdb_id` serves as the unique identifier for joining Netflix and OMDb datasets
- **Duplicates:** Some fields appear in both datasets (title, runtime, year, rating) with slight variations
- **Cleaned Fields:** The `*_clean` suffix indicates fields that have been parsed from string to numeric format for analysis

---

## Integration Details

- **Join Type:** Inner join on `imdb_id`
- **Netflix Records:** 3,407 movies with valid IMDb IDs
- **OMDb Records:** 500 movies fetched via API
- **Final Merged Dataset:** 500 movies (limited by OMDb API fetch)

For detailed integration statistics, see `results/integration_summary.csv`
