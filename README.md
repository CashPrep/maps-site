# Local Business Finder

A simple web app that searches Google Maps data using the Apify Google Maps Scraper Actor.

## Setup

1. Clone the repo
2. Create a `.env` file with your Apify token:
   ```
   APIFY_TOKEN=your_token_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run locally:
   ```bash
   python app.py
   ```
5. Open http://localhost:5000

## Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repo
3. Add `APIFY_TOKEN` as an environment variable
4. Deploy!
