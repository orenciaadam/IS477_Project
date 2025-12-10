# Factors Influencing IMDb Ratings of Netflix Movies

## Contributors
- **Daniel Newman** 
- **Adam Orencia**

---

## Project Summary

For this project, we chose to look into what factors influence IMDb ratings for movies on Netflix by combining two separate data sources with two different formats to build a fully reproducible computational workflow. We started with the Netflix IMDb Scores dataset from Kaggle. From there, we took the data and found a primary key. We used it to merge the data sets. We collected the 3,407 movie records and enriched them with additional metadata from the OMDb API. This includes runtime, genres, creative contributors, awards, and critic scores. This was challenging, but utilizing the common IMDb ID, we were able to match the data sets. We also struggled as the OMDb limits daily pull requests; the workflow was designed to fetch only once, cache raw JSONL results, and rebuild downstream tables from cached data to guarantee reproducibility. This original plan did not account for the request times limitations, but after working with the OMDb data, we were able to resolve the issues and pull the requests.

Our Snakemake pipeline automates every major step by first acquiring data, computing SHA-256 checksums for provenance, then it moves on to cleaning and parsing the OMDb fields, validating join keys, merging both datasets, running missingness checks, and finally producing summary statistics and visualizations. All of the raw inputs, intermediate files, and final outputs are stored using version control, and they have also been saved both locally and to Box, allowing other users to reproduce the full workflow by simply providing their own OMDb API key.

After cleaning both sources, the merge yielded 500 valid movie records, matching each record to its counterpart on IMDb ID. Information from our integration showed that we successfully got:
- 3,407 Netflix movies with valid IMDb IDs
- 500 OMDb records fetched
- 500 inner-join matches
- 2,907 Netflix movies without corresponding OMDb entries (due to the API cap of 500)

---

## Data Profile

Our project uses two datasets that exemplify different points in the data lifecycle. The first was the Netflix IMDb Scores dataset from Kaggle. The second was the OMDb API. These sources are different as they were made, accessed, structured, and licensed, which affects how they can be used under ethical use. Our data profile describes each dataset's characteristics, the fields each contains, and how we obtained them. It also mentions the ethical and legal implications that guided our workflow.

### Dataset 1: Netflix IMDb Scores (Kaggle)

The first dataset comes from a publicly available Netflix IMDb Scores file from Kaggle. This has an original data source from Data.world. This set includes 3,407 movie titles from Netflix, each with its own unique `imdb_id`. This serves as our primary key across our two sources. The Netflix set captures key information about movies, such as their title, movie type (limited to MOVIE in our project's subset), a text description, the release year under `release_year`, and the age range it was given as `age_certification`. The data included further information related to performance attributes such as `runtime`, `imdb_score`, and `imdb_votes`. This data is collected using the current count and vote, and ratings at the time of collection.

The data had some large positives that contributed to why we selected it. The columns are well defined, and the dataset uses `imdb_id` that aided in record linkage during the project. We used `imdb_id` as a reliable primary key for integration and as a unique identifier. Because they are a unique identifier, we felt they were a stable point for merging with the OMDb data. The Netflix dataset is distributed under an "Other" license on Kaggle, which allows academic reuse with credit to the original creator (see our `DATA_LICENSE.md` file). This licensing context shaped how we store, cite, and redistribute the data we used. We downloaded the dataset manually and placed it into the project's `data/raw/` directory. Since redistribution for academic purposes is permitted, we were able to include this dataset in our Box folder for reproducibility.

### Dataset 2: OMDb API

The second dataset is sourced from the OMDb API; this data provides a much broader range of movie information. Compared to the static Netflix dataset, the OMDb data is dynamic and collected, matching IMDb IDs as inputs from our script. Our columns include key fields like Genre, Director, Writer, Actors, Plot, Language, Country, to name a few. These features allow for more analysis by connecting a movie's creative features to the viewer's perception. This served to provide more contextual information on how the movies were perceived by the audience.

We collected OMDb data programmatically through our scripts. Our script `scripts/02_fetch_omdb.py` queries the API and writes the results into a JSONL file (`data/raw/omdb_raw.jsonl`). This script is made to follow the reproducibility guidelines of the project in our data flow pipeline. If the JSONL file already exists, the script does not make any new API calls; it reconstructs the cleaned and processed tables from the stored raw data. This avoids API rate-limit issues and ensures that future runs of our workflow operate under identical inputs.

OMDb is licensed under CC BY-NC 4.0, which allows non-commercial use and sharing as long as attribution is provided (see our `DATA_LICENSE.md` file). Since this project is strictly academic, our use of OMDb data falls within those boundaries, providing us with access to use the data. To support reproducibility and transparency, we save all API responses in a single JSONL file (`data/raw/omdb_raw.jsonl`). Keeping the file in the repository provides the benefit that the full provenance of the dataset is upheld. It allows anyone to inspect the raw API outputs, then rerun the cleaning scripts, and then confirm that the processed tables match the workflow's transformation steps. Users may still supply their own API key if they prefer to regenerate the data locally, but storing the JSONL file directly in the repo makes the project fully reproducible without depending on API rate limits or external services.

### Data Preparation and Integration

To prepare the OMDb dataset for integration, our cleaning script produced several fields. These include numeric runtimes (`runtime_minutes`), numeric IMDb rating (`imdbRating_clean`), integer vote counts (`imdbVotes_clean`), numeric Metascore (`Metascore_clean`), and standardized release year (`Year_clean`). These transformations combine OMDb's variance in format to allow the Netflix dataset to be more complete.

Next, look at the integration of the two datasets. We performed this using an inner join on `imdb_id`, resulting in a merged dataset of 500 movies. This was the upper limit of feasible API requests under the free tier during development. The remaining 2,907 Netflix titles were not enriched due to API constraints rather than data issues. Integration outcomes and record counts are documented in [`results/integration_summary.csv`](results/integration_summary.csv).

Overall, these two datasets, one static and manually collected, the other dynamic and API-driven, reflect different perspectives of real-world data work. The Netflix metadata offers a clean, structured foundation, while OMDb provides rich but inconsistent and partially restricted information. Together, they form a combined dataset that supports further in-depth analysis of patterns in audience perception of the movies, creative attributes, and historical trends while following all legal and ethical requirements.

---

## Data Quality Assessment

We conducted a full data quality assessment to truly understand the strengths and key limitations of the Netflix and OMDb datasets. We did this before integration and analysis to make sure we were collecting quality data around the analytics. This assessment focused on missing data. We also made sure to check for duplicate information. We also looked at type and format standardization and integration. The goal was to identify possible future issues that could affect our later analysis.

### Missingness Analysis

When we looked into the quality of our data for missing values, we found a major difference between the two inputs. The Netflix data showed a relatively complete dataset, excluding the column of age certifications, where 61% were missing.

On the other hand, the OMDb dataset we saw large amounts of missing information and data fields. The large areas of missing data were the production at 99%, DVD date at 98%, BoxOffice at 54%, and Metascore at 57%. Even with this missing information, it was essential for modeling fields. The main data we leveraged were the IMDb rating, votes, runtime, and year, which were all relatively complete records that helped enrich the Netflix data.

**Missingness Profiles:**
- [`results/netflix_missingness.csv`](results/netflix_missingness.csv)
- [`results/omdb_missingness.csv`](results/omdb_missingness.csv)

### Duplicate Detection

In terms of duplicate detection, `imdb_id` served as a reliable primary key and unique identifier, as each movie is given one individual `imdb_id`. This was true across both datasets, where the Netflix dataset contained no duplicate `imdb_id`. In the OMDb dataset, occasionally repeated records occurred when requests were retried or partially failed. This is not an issue with the data itself, but in the method of calling we used. These were handled during the cleaning and dropped by removing extra entries for any given ID.

### Type and Format Standardization

The two datasets also had small differences in data type and format. This was mainly in the OMDb data. There were issues with the numeric fields, such as runtime, vote counts, and rating scores, that were formatted as strings, requiring parsing to fix. Our cleaning scripts converted "123,456" into integer vote counts, "114 min" into numeric runtime, and string-encoded ratings into floats. This standardization was essential for correlation analysis, which was key in determining the answer to our research question. We also used this cleaned and formatted information in our visualizations.

### Integration Quality

Our integration was mostly successful, but out of 3,407 Netflix records, only 500 had OMDb data available due to the free-tier API request limit. The inner join resulted in exactly 500 matched records and no unmatched OMDb entries. This was done intentionally to make sure that all requests related to our Netflix data could match on `imdb_id`. Because the merged dataset includes only titles fetched via the API, it may overrepresent certain patterns. This can come from a variety of reasons, but specifically for newer, more popular, or simply earlier-listed films, depending on ID ordering.

### Potential Sources of Bias

Finally, some potential sources of bias include the reduced set of the Netflix data, as we only kept the first 500 that had matches. This factor must be considered when interpreting findings, especially in analyses involving trends over time or award information. We are also using a small sample to generalize over the population. More about this will be discussed in our future work.

---


# Findings

Once the data was finally cleaned, we then went on to merge, hash, validate, and push everything through our Snakemake pipeline. After this was done, we were able to look at the data itself. From this analysis of the 500 merged observations, we were able to see a bunch of consistent trends in the data. We looked at how ratings changed across genres, decades, and other key areas of interest.

To start, the summary statistics for our main variables confirmed what we later saw in the visualizations.

**Summary Statistics**  
[`results/summary_stats.csv`](results/summary_stats.csv)

---

The first thing that stood out was just how evenly distributed IMDb ratings look when you plot them. The histogram of `imdbRating_clean` shows a tight distribution centered around 6 and 7, which matches the general opinion and understanding that most movies are "fine," a few are really bad, and only a handful break into the premium 8 and 9 range. The summary statistics back this up. The average OMDb rating in our sample was 6.58, with a minimum of 2.8 and a maximum of 8.8.

**Figure: Distribution of IMDb Ratings**  
![IMDb Rating Histogram](figures/rating_histogram.png)

---

The correlations showed some strong and telling relationships. The biggest one was seen between Metascore and IMDb rating (r ≈ 0.71). When you look at the scatterplot, it supports this. As critic scores increase, so do audience scores. This makes sense as good movies are often subjectively positive across all different types of audiences. The second strongest correlation was between Netflix's stored rating (`imdb_score`) and OMDb's IMDb rating (r ≈ 0.97). This tells us that the time at which the Netflix scores were captured has not altered much, and the value they store is something pretty close to what IMDb has currently, even though that data is dynamically fetched.

**Correlation Matrix**  
[`results/correlation_matrix.csv`](results/correlation_matrix.csv)

**Figure: Metascore vs IMDb Rating**  
![Metascore vs IMDb Rating](figures/metascore_vs_rating.png)

---

Vote count had a smaller positive correlation with a rating of (r ≈ 0.29). The scatterplot visualization shows a very wide range of votes, where some movies get over a million votes, but others can barely break into four digits. Movies tend to get more attention and receive a higher rating, but that is not always the case. There are also plenty of average-rated movies with large vote counts, possibly due to their popularity or how long they have been out. We can see that the runtime also showed a weak correlation of only (r ≈ 0.16). This means that watching a three-hour movie did not guarantee a better rating. Through our work, there are plenty of examples of some of the highest-rated movies being significantly shorter while still maintaining higher ratings.

**Figure: Runtime vs IMDb Rating**  
![Runtime vs IMDb Rating](figures/runtime_vs_rating.png)

**Figure: Votes vs IMDb Rating**  
![Votes vs IMDb Rating](figures/votes_vs_rating.png)

---

Our awards analysis was very interesting and a little surprising. Movies that received awards had an average score of 6.70, coming in slightly higher than the 6.25 rating for films without awards. It is not a large difference, but it is substantial enough to show that awards do matter on average. It begs the question of how global recognition changes after awards. We see a trend that shows awards lead to more positive ratings in the long run due to the large audience that comes with it.

**Awards Rating Summary**  
[`results/award_rating_summary.csv`](results/award_rating_summary.csv)

---

The decade trends were probably the most interesting to look at. Even with the smaller sample size, which does impact our analysis, the average IMDb ratings were highest in the 1960s (7.20) and have been sloping downward ever since. This could also come with the increase in interest in the system, and over time, the rating system will become more difficult with more and more movies being added. With movies in the 2020s averaging only 5.98 so far. It could be that audiences are harsher or studios are more money-driven and focused on algorithms, or maybe that people are no longer going to theaters as much. Streaming has changed the game for better or worse. Regardless of the reason, it is clear that older movies in our data have tended to be rated higher than the newer ones.

**Figure: Average Rating by Decade**  
![Rating by Decade](figures/rating_by_decade.png)

**Decade Summary Table**  
[`results/rating_by_decade.csv`](results/rating_by_decade.csv)

---

Overall, the strongest influences of higher IMDb ratings were Metascore, awards, and being released in an earlier decade. Runtime and popularity help a little bit, but they were not super strong predictors on their own.

## Future Work

In our project, we established a reproducible end-to-end workflow from data collection to analysis. Time limits meant we had some unavoidable limits related to the API. Because the free OMDb use is set to 1,000 requests each day, the final merged data was limited to 500 movies to stay within this limit when making our scripts. One useful thing to do later would be gathering more data by using a bigger API limit or a paid plan. This would help our study and let us look at more movies and acquire more representative data. It would also allow us to reduce the bias that comes from only taking the first 500 IMDb IDs. For example, a larger dataset might help smooth out trends as time passes, give better genre balance, and make the plots less noisy.

Future plans revolve around using more than just OMDb data. OMDb works well for getting basic info like ratings, runtimes, and genres, but it does limit how deep you can study some things and has obvious missing data (Metascore, Box Office, Production). Other movie sites like Rotten Tomatoes could fill the gap. Rotten Tomatoes, for example, has a way of measuring how critics disagree with the content. This would help us understand if they generally don't agree on how good Netflix movies are. Using more sources would also give us more practice with the main ideas of the class, such as combining data and matching schemas. We think it would be interesting but challenging to grow our system to balance data disagreements across APIs and other sources.

If we grew the data, we could get more useful ideas from predictive models. Currently, our work only has descriptive analyses such as correlations, distributions, and decade trends. With a larger, fuller dataset, we could build regression or tree-based models to predict IMDb scores from movie features. We could learn which variables best indicate a higher score and see which things really matter: Do more famous actors improve ratings? Does length really matter? Are documentaries just always better? Models would also make us more careful about data quality. For example, filling in missing data, encoding genres, and dealing with skewed variables like vote count.

We also didn't get to study how to handle missing data systematically. Now, our system focuses more on understanding and cleaning than actually fixing what's missing. Because some OMDb fields are very incomplete, even simple imputation could let us do more studies. If we filled in Metascore, for example, we could add more movies to correlations or models instead of removing them.

Another idea involves viewing ratings over time. IMDb scores are dynamic as they change based on viewership. Some movies flop initially but then grow to be classics in the future. A helpful metric would be understanding the change in the rating over time to see how a movie has aged. We didn't gather data that changes across time, but if we queried OMDb or TMDB consistently, we could curate a dataset that tracks how ratings change. It would also let us find out if movies get better-rated once they reach Netflix.

It would also be quite interesting to compare the Netflix selection to that of other platforms. Do Netflix users judge more harshly? Are Prime Video movies better rated? Is everything on Disney+ pretty much a 7 or 8 since everything is a superhero movie? This would need processes to grab data from many platforms, but it strongly connects to real-world streaming platform questions.

In general, the largest opportunity is not even about the study; it is about growing the system we have already made. The hardest part was creating the infrastructure. Now that the system is set, adding more data sources, doing deeper studies, or training models is very doable. The work could grow in several ways based on what questions we need to answer next.

---

## Reproducing the Work

To reproduce this project, follow these steps carefully:

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Verify Directory Structure

Ensure your directory structure matches:
```
IS477/
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
├── results/
├── figures/
├── Snakefile
├── run_all.sh
├── requirements.txt
└── README.md
```

### 3. Install Dependencies

Install required Python packages:
```bash
pip install -r requirements.txt
```

**Note:** We encountered dependency issues with PuLP and Snakemake, so `requirements.txt` specifies tested versions. For exact reproducibility, use:
```bash
pip install -r requirements_frozen.txt
```

### 4. Obtain OMDb API Key

Since OMDb data cannot be redistributed, you need your own API key:

1. Visit: https://www.omdbapi.com/apikey.aspx
2. Select the **FREE** tier (1,000 daily requests)
3. Enter your email and activate the key
4. Create a file named `api_key.txt` in the project root directory
5. Paste your API key as a single line in this file

**Important:** The key file is protected by `.gitignore` and will not be committed to version control.

See [`API_KEY_INSTRUCTIONS.md`](API_KEY_INSTRUCTIONS.md) for detailed instructions.

### 5. Download Data from Box

To avoid API rate limits, download our processed data from Box:

**Box Link:** [INSERT YOUR BOX LINK HERE]

Download the following folders and place them in your project directory:
- `data/raw/` → Contains `Netflix_TV_Shows_and_Movies.csv` and `omdb_raw.jsonl`
- `data/processed/` → Contains all cleaned CSV files
- `results/` → Contains analysis outputs
- `figures/` → Contains visualization PNG files

When `omdb_raw.jsonl` is present, the workflow automatically skips API calls and rebuilds processed data from the cached file.

### 6. Run the Complete Workflow

Execute the entire pipeline:
```bash
bash run_all.sh
```

**OR** run Snakemake directly:
```bash
python -m snakemake -c 1
```

This executes all steps in sequence:
1. Clean Netflix dataset (`01_clean_netflix.py`)
2. Fetch/rebuild OMDb data (`02_fetch_omdb.py`)
3. Clean OMDb data (`03_clean_omdb.py`)
4. Merge datasets (`04_merge.py`)
5. Generate analysis and visualizations (`05_analyze_and_plot.py`)

### 7. Verify Data Integrity

SHA-256 checksums are computed for raw data files and stored in `results/checksums.txt`. Compare your checksums to verify data integrity:
```bash
cat results/checksums.txt
```

Expected checksums:
```
Netflix_TV_Shows_and_Movies.csv: [YOUR_CHECKSUM]
omdb_raw.jsonl: [YOUR_CHECKSUM]
```

### 8. View Results

After successful execution, all outputs are available:
- **Tables:** `results/*.csv`
- **Visualizations:** `figures/*.png`
- **Data documentation:** `DATA_DICTIONARY.md`

---

## References

Back 2 Viz Basics. (2022). *Netflix TV Shows and Movies* [Dataset]. Data.world. Retrieved from Kaggle: https://www.kaggle.com/datasets/thedevastator/netflix-imdb-scores

Creative Commons. (n.d.). *CC BY-NC 4.0 License*. https://creativecommons.org/licenses/by-nc/4.0/

MIT License. (2025). *Project Code License for IS 477 Group Project*.

OMDb API. (n.d.). *Open Movie Database* [API]. http://www.omdbapi.com

Python Software Foundation. (n.d.). *Python* (Version 3.x) [Programming language]. https://www.python.org

TheDevastator. (2022). *Netflix IMDb Scores* [Kaggle Dataset]. Kaggle. https://www.kaggle.com/datasets/thedevastator/netflix-imdb-scores

**Python Libraries:**
- McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56-61.
- Harris, C. R., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357-362.
- Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90-95.
- Mölder, F., et al. (2021). Sustainable data analysis with Snakemake. *F1000Research*, 10, 33.

---