"""
05_analyze_and_plot.py

Purpose:
    - Take the merged Netflix + OMDb dataset.
    - Compute summary statistics and correlations for numeric fields.
    - Explore ratings by awards and by time.
    - Save:
        * tabular outputs into results/
        * figures into figures/

Inputs:
    - data/processed/netflix_omdb_merged.csv

Outputs (tables):
    - results/summary_stats.csv
    - results/correlation_matrix.csv
    - results/award_rating_summary.csv
    - results/rating_by_decade.csv

Outputs (figures):
    - figures/runtime_vs_rating.png
    - figures/votes_vs_rating.png
    - figures/metascore_vs_rating.png
    - figures/rating_histogram.png
    - figures/rating_by_decade.png
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_PATH   = Path("data/processed/netflix_omdb_merged.csv")
RESULTS_DIR = Path("results")
FIG_DIR     = Path("figures")


def main():
    print("=== 05: ANALYZE + PLOT ===")

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Expected merged dataset at {DATA_PATH}, but it does not exist. "
            "Run 04_merge_netflix_omdb.py first."
        )

    df = pd.read_csv(DATA_PATH)
    print("Merged shape:", df.shape)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Select numeric columns
    candidate_numeric = [
        "imdbRating_clean",   # OMDb numeric IMDb rating
        "runtime_minutes",    # parsed runtime
        "imdbVotes_clean",    # parsed vote count
        "Metascore_clean",    # numeric metascore
        "Year_clean",         # numeric year
        "imdb_score",         # original Netflix rating if present
        "imdb_votes",         # original Netflix votes if present
    ]

    numeric_cols = [c for c in candidate_numeric if c in df.columns]
    if not numeric_cols:
        raise ValueError("No expected numeric columns were found in the merged dataset.")

    # 2. Summary statistics (rows = variables)
    summary_stats = df[numeric_cols].describe().T
    summary_csv = RESULTS_DIR / "summary_stats.csv"
    summary_stats.to_csv(summary_csv)
    print(f"Saved summary statistics to: {summary_csv}")

    # 3. Correlation matrix
    corr_df = df[numeric_cols].corr()
    corr_csv = RESULTS_DIR / "correlation_matrix.csv"
    corr_df.to_csv(corr_csv)
    print(f"Saved correlation matrix to: {corr_csv}")


    # 4. Awards vs rating
    if "Awards" in df.columns and "imdbRating_clean" in df.columns:
        df["has_awards"] = df["Awards"].notna() & (df["Awards"].astype(str).str.lower() != "n/a")

        award_summary = (
            df.groupby("has_awards")["imdbRating_clean"]
              .agg(["count", "mean"])
              .rename(index={False: "no_awards", True: "has_awards"})
        )

        award_csv = RESULTS_DIR / "award_rating_summary.csv"
        award_summary.to_csv(award_csv)
        print(f"Saved awards vs rating summary to: {award_csv}")
    else:
        award_summary = None


    # 5. Rating by decade
    if "Year_clean" in df.columns and "imdbRating_clean" in df.columns:
        df_dec = df.copy()
        df_dec["decade"] = (df_dec["Year_clean"] // 10) * 10
        rating_by_decade = (
            df_dec.dropna(subset=["decade"])
                  .groupby("decade")["imdbRating_clean"]
                  .agg(["count", "mean"])
                  .reset_index()
                  .sort_values("decade")
        )

        decade_csv = RESULTS_DIR / "rating_by_decade.csv"
        rating_by_decade.to_csv(decade_csv, index=False)
        print(f"Saved rating-by-decade summary to: {decade_csv}")
    else:
        rating_by_decade = None

    # 6. Figures

    # Runtime vs rating
    if "runtime_minutes" in df.columns and "imdbRating_clean" in df.columns:
        plt.figure(figsize=(8, 6))
        plt.scatter(df["runtime_minutes"], df["imdbRating_clean"], alpha=0.4)
        plt.xlabel("Runtime (minutes)")
        plt.ylabel("IMDb Rating (OMDb)")
        plt.title("Runtime vs IMDb Rating")
        plt.tight_layout()
        out_path = FIG_DIR / "runtime_vs_rating.png"
        plt.savefig(out_path)
        plt.close()
        print(f"Saved figure: {out_path}")

    # Votes vs rating 
    if "imdbVotes_clean" in df.columns and "imdbRating_clean" in df.columns:
        plt.figure(figsize=(8, 6))
        plt.scatter(df["imdbVotes_clean"], df["imdbRating_clean"], alpha=0.4)
        plt.xlabel("IMDb Votes")
        plt.ylabel("IMDb Rating (OMDb)")
        plt.title("Votes vs IMDb Rating")
        plt.tight_layout()
        out_path = FIG_DIR / "votes_vs_rating.png"
        plt.savefig(out_path)
        plt.close()
        print(f"Saved figure: {out_path}")

    # Metascore vs rating
    if "Metascore_clean" in df.columns and "imdbRating_clean" in df.columns:
        plt.figure(figsize=(8, 6))
        plt.scatter(df["Metascore_clean"], df["imdbRating_clean"], alpha=0.4)
        plt.xlabel("Metascore")
        plt.ylabel("IMDb Rating (OMDb)")
        plt.title("Metascore vs IMDb Rating")
        plt.tight_layout()
        out_path = FIG_DIR / "metascore_vs_rating.png"
        plt.savefig(out_path)
        plt.close()
        print(f"Saved figure: {out_path}")

    # Histogram of IMDb ratings
    if "imdbRating_clean" in df.columns:
        plt.figure(figsize=(8, 6))
        df["imdbRating_clean"].dropna().hist(bins=20)
        plt.xlabel("IMDb Rating (OMDb)")
        plt.ylabel("Count of movies")
        plt.title("Distribution of IMDb Ratings")
        plt.tight_layout()
        out_path = FIG_DIR / "rating_histogram.png"
        plt.savefig(out_path)
        plt.close()
        print(f"Saved figure: {out_path}")

    # Rating by decade bar chart
    if rating_by_decade is not None and not rating_by_decade.empty:
        plt.figure(figsize=(8, 6))
        plt.bar(
            rating_by_decade["decade"].astype(int).astype(str),
            rating_by_decade["mean"]
        )
        plt.xlabel("Decade")
        plt.ylabel("Average IMDb Rating (OMDb)")
        plt.title("Average IMDb Rating by Decade")
        plt.tight_layout()
        out_path = FIG_DIR / "rating_by_decade.png"
        plt.savefig(out_path)
        plt.close()
        print(f"Saved figure: {out_path}")

    print("=== DONE: 05_analyze_and_plot ===")


if __name__ == "__main__":
    main()
