# OMDb API Key Setup
This project uses the OMDb API to fetch movie metadata. You need your own free API key.

## Getting an API Key

1. Go to: http://www.omdbapi.com/apikey.aspx
2. Select "FREE" tier (1,000 daily requests)
3. Enter your email
4. Check your email for the activation link
5. Click the link to activate your key

## Using Your API Key

Create a file named `api_key.txt` in the project root directory:
```
your-api-key-here
```

**Important:** Do NOT commit this file to Git. It's already in `.gitignore`.

## Note on Reproducibility

If you're reproducing our results:
- Download the raw data from Box (see README.md)
- The workflow will skip API calls if `data/raw/omdb_raw.jsonl` exists
- You only need an API key if you want to fetch fresh data