"""
03_clean_omdb.py

Purpose:
    - Take the OMDb CSV produced by 02_fetch_omdb.py and perform
      basic cleaning + type conversions on key fields.
    - Produce a cleaned OMDb dataset suitable for integration with Netflix.
    - Generate a simple data quality profile (missingness) for documentation.

Inputs:
    - data/processed/omdb_from_netflix.csv

Outputs:
    - data/processed/omdb_clean.csv
    - results/omdb_missingness.csv
"""

from pathlib import Path
import pandas as pd

# ---------- Paths ----------
OMDB_IN      = Path("data/processed/omdb_from_netflix.csv")
OMDB_CLEAN   = Path("data/processed/omdb_clean.csv")
RESULTS_DIR  = Path("results")
MISSING_CSV  = RESULTS_DIR / "omdb_missingness.csv"


def parse_runtime_to_minutes(s):
    """Parse strings like '123 min' into integer minutes."""
    if pd.isna(s):
        return None
    s = str(s)
    parts = s.split()
    for p in parts:
        try:
            return int(p)
        except ValueError:
            continue
    return None


def parse_votes(s):
    """Parse vote counts like '1,234,567' into integers."""
    if pd.isna(s):
        return None
    s = str(s).replace(",", "")
    try:
        return int(s)
    except ValueError:
        return None


def main():
    print("=== 03: CLEAN OMDb DATA ===")
    print(f"Loading OMDb data from: {OMDB_IN}")

    if not OMDB_IN.exists():
        raise FileNotFoundError(
            f"Expected OMDb input at {OMDB_IN}, but it does not exist. "
            "Run 02_fetch_omdb.py first to generate omdb_from_netflix.csv."
        )

    df = pd.read_csv(OMDB_IN)
    print("Raw OMDb shape:", df.shape)

    # Basic normalization
    # Ensure imdb_id exists and is standardized
    if "imdb_id" not in df.columns:
        raise KeyError("Expected an 'imdb_id' column in OMDb dataset, but it was not found.")

    df["imdb_id"] = df["imdb_id"].astype(str).str.strip()

    # Drop exact duplicate imdb_id rows, keeping first
    before_dups = len(df)
    df = df.drop_duplicates(subset=["imdb_id"])
    after_dups = len(df)
    print(f"Dropped {before_dups - after_dups} duplicate rows based on imdb_id.")

    # Type conversions / cleaned numeric fields 

    # Runtime to minutes
    if "Runtime" in df.columns:
        df["runtime_minutes"] = df["Runtime"].apply(parse_runtime_to_minutes)

    # imdbRating to numeric (float)
    if "imdbRating" in df.columns:
        df["imdbRating_clean"] = pd.to_numeric(df["imdbRating"], errors="coerce")

    # imdbVotes to integer
    if "imdbVotes" in df.columns:
        df["imdbVotes_clean"] = df["imdbVotes"].apply(parse_votes)

    # Metascore to numeric (0-100 typical)
    if "Metascore" in df.columns:
        df["Metascore_clean"] = pd.to_numeric(df["Metascore"], errors="coerce")

    # Year to numeric (some rows might have ranges or non-numeric)
    if "Year" in df.columns:
        df["Year_clean"] = pd.to_numeric(df["Year"], errors="coerce")

    # Data quality profile
    print("Computing missingness profile for OMDb data...")
    missing_counts = df.isna().sum().to_frame(name="n_missing")
    missing_counts["p_missing"] = missing_counts["n_missing"] / len(df)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    missing_counts.to_csv(MISSING_CSV)
    print(f"Saved OMDb missingness profile to: {MISSING_CSV}")

    # Save cleaned OMDb dataset 
    OMDB_CLEAN.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OMDB_CLEAN, index=False)
    print(f"Saved cleaned OMDb dataset to: {OMDB_CLEAN}")

    print("=== DONE: 03_clean_omdb ===")


if __name__ == "__main__":
    main()
