import time
import json
import requests
import pandas as pd
from pathlib import Path

# ----- Load API key (reuses your existing pattern) -----
KEY_CANDIDATES = ["api_key", "api_key.txt", "omdb_apikey.txt"]
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

# ----- Paths -----
IDS_PATH = Path("data/processed/netflix_imdb_ids.csv")
RAW_JSON = Path("data/raw/omdb_raw.jsonl")
OUT_CSV  = Path("data/processed/omdb_from_netflix.csv")

# Which fields to keep from OMDb
KEEP = [
    "Title","Year","Rated","Released","Runtime","Genre","Director","Writer","Actors",
    "Plot","Language","Country","Awards","Poster","Ratings","Metascore","imdbRating",
    "imdbVotes","imdbID","Type","DVD","BoxOffice","Production","Website"
]

def omdb_by_id(imdb_id: str) -> dict:
    """Fetch a single title from OMDb by IMDb ID."""
    url = "http://www.omdbapi.com/"
    params = {"apikey": OMDB_KEY, "i": imdb_id, "r": "json"}
    r = requests.get(url, params=params, timeout=15)
    data = r.json()
    data["imdb_id"] = imdb_id  # normalized join key
    return data

def main():
    # Load the list of IDs created by clean_netflix.py
    ids_df = pd.read_csv(IDS_PATH)
    imdb_ids = ids_df["imdb_id"].astype(str).tolist()[:25]
    print(f"Loaded {len(imdb_ids)} IMDb IDs from {IDS_PATH}")

    results = []
    RAW_JSON.parent.mkdir(parents=True, exist_ok=True)

    with RAW_JSON.open("w", encoding="utf-8") as f_raw:
        for i, imdb_id in enumerate(imdb_ids, start=1):
            try:
                data = omdb_by_id(imdb_id)

                # Detect OMDb daily limit and stop early
                if data.get("Error") == "Request limit reached!":
                    print(f"❌ Hit daily OMDb request limit at ID #{i} ({imdb_id}). Stopping early.")
                    break

                # Write raw JSON line for provenance
                f_raw.write(json.dumps(data) + "\n")

                if data.get("Response") == "True":
                    subset = {k: data.get(k) for k in KEEP}
                    subset["imdb_id"] = imdb_id
                    results.append(subset)
                else:
                    print(f"[{i}] {imdb_id}: OMDb error = {data.get('Error')}")
            except Exception as e:
                print(f"[{i}] {imdb_id}: Exception {e}")

            # Small pause to be nice to API / avoid throttling
            time.sleep(0.25)

            if i % 50 == 0:
                print(f"...fetched {i} titles so far")

    omdb_df = pd.DataFrame(results)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    omdb_df.to_csv(OUT_CSV, index=False)
    print(f"✅ Saved {len(omdb_df)} OMDb rows to: {OUT_CSV}")

if __name__ == "__main__":
    main()
