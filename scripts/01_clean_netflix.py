"""
01_clean_netflix.py

Purpose:
    - Take the raw Kaggle Netflix CSV.
    - Filter to movies only (through type column).
    - Standardize and validate imdb_id.
    - Save:
        * data/processed/netflix_clean.csv          -> cleaned Netflix records
        * data/processed/netflix_imdb_ids.csv       -> unique IMDb IDs for future reference
        * results/netflix_missingness.csv           -> data quality profile


"""

import pandas as pd
from pathlib import Path
import hashlib

def compute_sha256(filepath):
    """Compute SHA-256"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

# paths
RAW_PATH      = Path("data/raw/Netflix_TV_Shows_and_Movies.csv")
OUT_CLEAN     = Path("data/processed/netflix_clean.csv")
OUT_IDS       = Path("data/processed/netflix_imdb_ids.csv")
RESULTS_DIR   = Path("results")
MISSINGNESS_CSV = RESULTS_DIR / "netflix_missingness.csv"


def main():
    print("=== 01: CLEAN NETFLIX DATA ===")
    print(f"Loading raw Netflix file from: {RAW_PATH}")
    df = pd.read_csv(RAW_PATH)

    # Compute and save checksum for data integrity
    print("Computing SHA-256 checksum for raw Netflix data...")
    checksum = compute_sha256(RAW_PATH)
    print(f"Netflix CSV SHA-256: {checksum}")
    
    # Save checksum to results
    checksum_file = RESULTS_DIR / "checksums.txt"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with checksum_file.open("w") as f:
        f.write(f"Netflix_TV_Shows_and_Movies.csv: {checksum}\n")
    print(f"Saved checksum to: {checksum_file}")

    print("Raw shape:", df.shape)

    # Filter to movies
    if "type" in df.columns:
        df = df[df["type"].str.lower() == "movie"].copy()
        print("After filtering to movies only:", df.shape)
    else:
        print("Warning: 'type' column not found. Skipping movie filter.")

    # Valid imdb_id
    if "imdb_id" not in df.columns:
        raise KeyError("Expected an 'imdb_id' column in the Netflix dataset, but it was not found.")

    # Valid IDs (non-null and length >= 7)
    df_clean = df[
        (df["imdb_id"].notna()) &
        (df["imdb_id"].astype(str).str.len() >= 7)
    ].copy()

    # Normalize imdb_id as string
    df_clean["imdb_id"] = df_clean["imdb_id"].astype(str).str.strip()
    print("After imdb_id cleaning/filtering:", df_clean.shape)

    # Data quality profile
    # Missing values and percentages 
    print("Computing missingness profile for cleaned Netflix data...")
    missing_counts = df_clean.isna().sum().to_frame(name="n_missing")
    missing_counts["p_missing"] = missing_counts["n_missing"] / len(df_clean)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    missing_counts.to_csv(MISSINGNESS_CSV)
    print(f"Saved missingness profile to: {MISSINGNESS_CSV}")

    # Save Clean Dataset
    OUT_CLEAN.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(OUT_CLEAN, index=False)
    print(f"Saved cleaned Netflix dataset to: {OUT_CLEAN}")

    # Save unique IMDb ID list
    ids = (
        df_clean[["imdb_id"]]
        .dropna()
        .drop_duplicates()
        .sort_values("imdb_id")
    )
    ids.to_csv(OUT_IDS, index=False)
    print(f"Saved {len(ids)} unique IMDb IDs to: {OUT_IDS}")

    print("=== DONE: 01_clean_netflix ===")


if __name__ == "__main__":
    main()
