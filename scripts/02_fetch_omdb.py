"""
fetch_omdb.py

Purpose:
    - Programmatically acquire OMDb movie metadata for IMDb IDs derived from the Netflix dataset.
    - This script requires an OMDb API key. Users must create their own key at:
          https://www.omdbapi.com/apikey.aspx
    - The script searches for a local file containing the API key (e.g., `api_key.txt`).

Reproducibility notes:
    - This script is designed to run automatically in our Snakemake workflow
      *only if* the raw OMDb file (`data/raw/omdb_raw.jsonl`) does not exist.
    - This prevents unnecessary API usage, respects OMDb rate limits, and allows others
      to fully reproduce our data acquisition by simply providing their own API key.

Outputs:
    - data/raw/omdb_raw.jsonl   (raw JSON for provenance)
    - data/processed/omdb_from_netflix.csv
"""

import time
import json
import requests
import pandas as pd
from pathlib import Path
import hashlib

# ---------------------------------------------------------
# Load API key

def compute_sha256(filepath):
    """Compute SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

KEY_CANDIDATES = ["api_key", "api_key.txt", "omdb_apikey.txt", "Daniel_API_key.txt"]
key_path = next((Path(p) for p in KEY_CANDIDATES if Path(p).exists()), None)

if key_path is None:
    raise FileNotFoundError(
        f"Couldn't find any of {KEY_CANDIDATES}. "
        "Create one, paste your OMDb key on a single line, and re-run."
    )

OMDB_KEY = key_path.read_text(encoding="utf-8").strip()
if not OMDB_KEY or "REPLACE" in OMDB_KEY:
    raise ValueError("Your key file is empty or still a placeholder. Paste your real OMDb key.")

print(f"Loaded OMDb key from {key_path}")

# ---------------------------------------------------------
# Paths


IDS_PATH = Path("data/processed/netflix_imdb_ids.csv")
RAW_JSON = Path("data/raw/omdb_raw.jsonl")
OUT_CSV  = Path("data/processed/omdb_from_netflix.csv")

# Fields to keep from OMDb
KEEP = [
    "Title","Year","Rated","Released","Runtime","Genre","Director","Writer","Actors",
    "Plot","Language","Country","Awards","Poster","Ratings","Metascore","imdbRating",
    "imdbVotes","imdbID","Type","DVD","BoxOffice","Production","Website"
]

# ---------------------------------------------------------
# Fetch a single OMDb entry


def omdb_by_id(imdb_id: str) -> dict:
    url = "http://www.omdbapi.com/"
    params = {"apikey": OMDB_KEY, "i": imdb_id, "r": "json"}
    r = requests.get(url, params=params, timeout=15)
    data = r.json()
    data["imdb_id"] = imdb_id
    return data

# ---------------------------------------------------------
# Main pipeline


def main():

    # Skip API if raw JSONL already exists
    if RAW_JSON.exists():
        print(f"OMDb raw data already exists at {RAW_JSON}")
        print("Rebuilding CSV from existing JSONL to avoid API calls...")
        
        # Rebuild CSV from JSONL
        results = []
        with RAW_JSON.open("r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                if data.get("Response") == "True":
                    subset = {k: data.get(k) for k in KEEP}
                    subset["imdb_id"] = data.get("imdb_id")
                    results.append(subset)
        
        omdb_df = pd.DataFrame(results)
        OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        omdb_df.to_csv(OUT_CSV, index=False)
        print(f"Rebuilt {len(omdb_df)} rows in {OUT_CSV}")
        return
    

    # Load cleaned list of IDs
    ids_df = pd.read_csv(IDS_PATH)
    print("Full imdb_id file shape:", ids_df.shape)

    MAX_TITLES = 500

    all_ids = ids_df["imdb_id"].astype(str).tolist()
    imdb_ids = all_ids[:MAX_TITLES]

    print(f"Loaded {len(imdb_ids)} IMDb IDs from {IDS_PATH} (cap={MAX_TITLES})")

    results = []
    RAW_JSON.parent.mkdir(parents=True, exist_ok=True)

    # Write raw JSONL for provenance
    with RAW_JSON.open("w", encoding="utf-8") as f_raw:
        for i, imdb_id in enumerate(imdb_ids, start=1):

            try:
                data = omdb_by_id(imdb_id)

                # Detect daily limit
                if data.get("Error") == "Request limit reached!":
                    print(f"Hit OMDb request limit at index #{i} ({imdb_id}). Stopping early.")
                    break

                # Save raw record
                f_raw.write(json.dumps(data) + "\n")

                # Extract if successful
                if data.get("Response") == "True":
                    subset = {k: data.get(k) for k in KEEP}
                    subset["imdb_id"] = imdb_id
                    results.append(subset)
                else:
                    print(f"[{i}] {imdb_id}: OMDb error = {data.get('Error')}")

            except Exception as e:
                print(f"[{i}] {imdb_id}: Exception occurred → {e}")

            # Sleep to avoid rate limiting
            time.sleep(0.25)

            if i % 50 == 0:
                print(f"...fetched {i} titles so far")

    # Save processed CSV
    omdb_df = pd.DataFrame(results)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    omdb_df.to_csv(OUT_CSV, index=False)

    print(f"Saved {len(omdb_df)} OMDb rows to: {OUT_CSV}")

    # Compute checksum for raw OMDb data
    print("Computing SHA-256 checksum for raw OMDb data...")
    checksum = compute_sha256(RAW_JSON)
    print(f"OMDb raw JSONL SHA-256: {checksum}")
    
    # add checksums file
    checksum_file = Path("results/checksums.txt")
    with checksum_file.open("a") as f:  
        f.write(f"omdb_raw.jsonl: {checksum}\n")
    print(f"Appended checksum to: {checksum_file}")


if __name__ == "__main__":
    main()
