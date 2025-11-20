import pandas as pd
from pathlib import Path
import re
import numpy as np

# Paths
RAW_PATH = Path("data/raw/Netflix_TV_Shows_and_Movies.csv")
OUT_CLEAN = Path("data/processed/netflix_clean.csv")
OUT_IDS   = Path("data/processed/netflix_imdb_ids.csv")

def main():
    print("Loading raw Netflix file...")
    df = pd.read_csv(RAW_PATH)
    print("Raw shape:", df.shape)

    # OPTIONAL: filter only movies 
    if "type" in df.columns:
        df = df[df["type"].str.lower() == "movie"].copy()
        print("After filtering to movies:", df.shape)

    # Keep only rows with valid imdb_id
    df_clean = df[
        (df["imdb_id"].notna()) &
        (df["imdb_id"].astype(str).str.len() >= 7)
    ].copy()

    # Normalize imdb_id as string
    df_clean["imdb_id"] = df_clean["imdb_id"].astype(str).str.strip()
    print("After imdb_id cleaning:", df_clean.shape)

    # Save cleaned dataset
    OUT_CLEAN.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(OUT_CLEAN, index=False)
    print(f"Saved cleaned Netflix dataset to: {OUT_CLEAN}")

    # Save unique ID list
    ids = (
        df_clean[["imdb_id"]]
        .dropna()
        .drop_duplicates()
        .sort_values("imdb_id")
    )
    ids.to_csv(OUT_IDS, index=False)
    print(f"Saved {len(ids)} IMDb IDs to: {OUT_IDS}")

if __name__ == "__main__":
    main()