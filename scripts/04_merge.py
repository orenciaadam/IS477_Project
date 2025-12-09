"""
04_merge_netflix_omdb.py

Purpose:
    - Integrate the cleaned Netflix and OMDb datasets into a single table.
    - Perform a join on imdb_id.
    - Save a simple summary for documentation.

Inputs:
    - data/processed/netflix_clean.csv
    - data/processed/omdb_clean.csv

Outputs:
    - data/processed/netflix_omdb_merged.csv
    - results/integration_summary.csv
"""

from pathlib import Path
import pandas as pd

# Paths
NETFLIX_CLEAN = Path("data/processed/netflix_clean.csv")
OMDB_CLEAN    = Path("data/processed/omdb_clean.csv")
OUT_MERGED    = Path("data/processed/netflix_omdb_merged.csv")

RESULTS_DIR   = Path("results")
INTEGRATION_SUMMARY = RESULTS_DIR / "integration_summary.csv"


def main():
    print("=== 04: MERGE NETFLIX + OMDb ===")

    if not NETFLIX_CLEAN.exists():
        raise FileNotFoundError(f"Missing input: {NETFLIX_CLEAN} not found.")

    if not OMDB_CLEAN.exists():
        raise FileNotFoundError(f"Missing input: {OMDB_CLEAN} not found.")

    print(f"Loading Netflix data from: {NETFLIX_CLEAN}")
    nf = pd.read_csv(NETFLIX_CLEAN)
    print("Netflix shape:", nf.shape)

    print(f"Loading OMDb data from: {OMDB_CLEAN}")
    omdb = pd.read_csv(OMDB_CLEAN)
    print("OMDb shape:", omdb.shape)

    # Standardize imdb_id in both tables
    if "imdb_id" not in nf.columns:
        raise KeyError("Netflix data is missing 'imdb_id' column.")
    if "imdb_id" not in omdb.columns:
        raise KeyError("OMDb data is missing 'imdb_id' column.")

    nf["imdb_id"] = nf["imdb_id"].astype(str).str.strip()
    omdb["imdb_id"] = omdb["imdb_id"].astype(str).str.strip()

    # drop duplicate imdb_id in Netflix just in case
    before_nf = len(nf)
    nf = nf.drop_duplicates(subset=["imdb_id"])
    after_nf = len(nf)
    if before_nf != after_nf:
        print(f"Dropped {before_nf - after_nf} duplicate Netflix rows based on imdb_id.")

    # Integration: inner join on imdb_id
    print("Merging on imdb_id (inner join)...")
    merged = nf.merge(omdb, on="imdb_id", how="inner")
    print("Merged shape:", merged.shape)

    # integration summary
    n_netflix = len(nf)
    n_omdb = len(omdb)
    n_merged = len(merged)

    # How many ids are unique to each side
    netflix_ids = set(nf["imdb_id"])
    omdb_ids = set(omdb["imdb_id"])

    only_netflix = len(netflix_ids - omdb_ids)
    only_omdb = len(omdb_ids - netflix_ids)
    intersection = len(netflix_ids & omdb_ids)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summary_rows = [
        {"metric": "n_netflix_clean", "value": n_netflix},
        {"metric": "n_omdb_clean", "value": n_omdb},
        {"metric": "n_merged_inner", "value": n_merged},
        {"metric": "n_ids_netflix_only", "value": only_netflix},
        {"metric": "n_ids_omdb_only", "value": only_omdb},
        {"metric": "n_ids_intersection", "value": intersection},
    ]
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(INTEGRATION_SUMMARY, index=False)
    print(f"Saved integration summary to: {INTEGRATION_SUMMARY}")

    # Save merged dataset
    OUT_MERGED.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUT_MERGED, index=False)
    print(f"Saved merged dataset to: {OUT_MERGED}")

    print("=== DONE: 04_merge_netflix_omdb ===")


if __name__ == "__main__":
    main()
