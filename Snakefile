# Snakefile
# End-to-end pipeline from raw Netflix CSV and OMDb API to final results and figures.

rule all:
    input:
        # cleaned data
        "data/processed/netflix_clean.csv",
        "data/processed/netflix_imdb_ids.csv",
        "data/processed/omdb_clean.csv",
        "data/processed/netflix_omdb_merged.csv",

        # data quality + integration
        "results/netflix_missingness.csv",
        "results/omdb_missingness.csv",
        "results/integration_summary.csv",

        # analysis tables
        "results/summary_stats.csv",
        "results/correlation_matrix.csv",
        "results/award_rating_summary.csv",
        "results/rating_by_decade.csv",

        # figures
        "figures/runtime_vs_rating.png",
        "figures/votes_vs_rating.png",
        "figures/metascore_vs_rating.png",
        "figures/rating_histogram.png",
        "figures/rating_by_decade.png"


# 01: clean Netflix (Kaggle CSV -> cleaned + id list + missingness)
rule clean_netflix:
    input:
        "data/raw/Netflix_TV_Shows_and_Movies.csv"
    output:
        "data/processed/netflix_clean.csv",
        "data/processed/netflix_imdb_ids.csv",
        "results/netflix_missingness.csv"
    shell:
        "python scripts/01_clean_netflix.py"


# 02: fetch OMDb data via API
# only if outputs don't already exist
rule fetch_omdb:
    input:
        "data/processed/netflix_imdb_ids.csv"
    output:
        "data/raw/omdb_raw.jsonl",
        "data/processed/omdb_from_netflix.csv"
    run:
        import os
        # Only run if outputs don't exist
        if not all(os.path.exists(str(f)) for f in output):
            shell("python scripts/02_fetch_omdb.py")
        else:
            print("OMDb data already exists. Skipping API fetch.")


# 03: clean OMDb (works only on local CSV, no API calls here)
rule clean_omdb:
    input:
        "data/processed/omdb_from_netflix.csv"
    output:
        "data/processed/omdb_clean.csv",
        "results/omdb_missingness.csv"
    shell:
        "python scripts/03_clean_omdb.py"


# 04: merge Netflix + OMDb
rule merge_netflix_omdb:
    input:
        "data/processed/netflix_clean.csv",
        "data/processed/omdb_clean.csv"
    output:
        "data/processed/netflix_omdb_merged.csv",
        "results/integration_summary.csv"
    shell:
        "python scripts/04_merge.py"


# 05: analyze + plot
rule analyze_and_plot:
    input:
        "data/processed/netflix_omdb_merged.csv"
    output:
        "results/summary_stats.csv",
        "results/correlation_matrix.csv",
        "results/award_rating_summary.csv",
        "results/rating_by_decade.csv",
        "figures/runtime_vs_rating.png",
        "figures/votes_vs_rating.png",
        "figures/metascore_vs_rating.png",
        "figures/rating_histogram.png",
        "figures/rating_by_decade.png"
    shell:
        "python scripts/05_analyze_and_plot.py"
