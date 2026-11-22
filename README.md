# CodeAlpha Web Scraping – Deployed Web Application

A Flask web app that scrapes book details from **Books to Scrape** and displays the results in a browser. Users can choose 1–5 catalogue pages and download the collected records as CSV.

## Features
- Public webpage with a Start Scraping button
- Live scraping using Requests and BeautifulSoup
- Book title, price, rating, availability and product URL
- Results table and CSV download
- Responsive layout for desktop and mobile
- Render deployment configuration (`render.yaml`)

## Deploy free on Render
1. Create/sign in to GitHub and Render.
2. Create a new GitHub repository, for example `CodeAlpha-Web-Scraping`.
3. Upload all files and folders from this project to the repository root (not the ZIP file itself).
4. In Render, choose **New + → Web Service** and connect the GitHub repository.
5. Select the **Free** instance plan. The included `render.yaml` supplies the build/start settings. If entering them manually:
   - Runtime: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
6. Click **Deploy Web Service**. When deployment succeeds, open the public `https://...onrender.com` URL.

No one using the deployed site needs Python or VS Code installed. They only need a browser and internet connection.

## Run locally only if you want to test
```bash
python -m venv venv
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
# source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000`. Local testing is optional; the deployed version runs on Render.

## Important free-hosting notes
- Render free web services can spin down after 15 minutes without traffic; the first visit after that can take around a minute to wake up.
- The free service filesystem is temporary. This app keeps the latest scrape in memory for the running instance; results may reset after a restart, redeploy or spin-down. Download the CSV if you need to keep a copy.
- The scraper is limited to five pages per request and pauses briefly between pages. It is intended for educational use against the practice website, not high-volume scraping.

## Suggested internship screenshots
1. Public deployed app URL in browser.
2. Scraping success message and results table.
3. CSV opened in Excel.
4. GitHub repository file list.
5. Render deployment status showing Live.
