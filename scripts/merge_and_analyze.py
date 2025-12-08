import pandas as pd
from pathlib import Path

NETFLIX_CLEAN = Path("data/processed/netflix_clean.csv")
OMDB_CSV      = Path("data/processed/omdb_from_netflix.csv")
OUT_MERGED    = Path("data/processed/netflix_omdb_merged.csv")


def parse_runtime_to_minutes(s):
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
    if pd.isna(s):
        return None
    s = str(s).replace(",", "")
    try:
        return int(s)
    except ValueError:
        return None


def main():
    print("Loading cleaned Netflix data...")
    nf = pd.read_csv(NETFLIX_CLEAN)
    print("Netflix shape:", nf.shape)

    print("Loading OMDb data...")
    omdb = pd.read_csv(OMDB_CSV)
    print("OMDb shape:", omdb.shape)

    # Ensure key is consistent
    nf["imdb_id"] = nf["imdb_id"].astype(str).str.strip()
    omdb["imdb_id"] = omdb["imdb_id"].astype(str).str.strip()

    print("Merging on imdb_id...")
    merged = nf.merge(omdb, on="imdb_id", how="inner")
    print("Merged shape:", merged.shape)

    # Simple cleaning
    if "Runtime" in merged.columns:
        merged["runtime_omdb_min"] = merged["Runtime"].apply(parse_runtime_to_minutes)

    if "imdbVotes" in merged.columns:
        merged["imdbVotes_clean"] = merged["imdbVotes"].apply(parse_votes)

    if "imdbRating" in merged.columns:
        merged["imdbRating_clean"] = pd.to_numeric(merged["imdbRating"], errors="coerce")

    OUT_MERGED.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUT_MERGED, index=False)
    print(f"Saved merged dataset to: {OUT_MERGED}")


if __name__ == "__main__":
    main()
