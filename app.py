from flask import Flask, render_template, request, jsonify, send_file
import requests, csv, io, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)
BASE_URL = "https://books.toscrape.com/"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
HEADERS = {"User-Agent": "EducationalWebScraper/1.0"}
latest_rows = []

def scrape_books(max_pages=3):
    rows, url, page = [], BASE_URL, 0
    while url and page < max_pages:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for card in soup.select("article.product_pod"):
            title = card.select_one("h3 a")
            price = card.select_one(".price_color")
            stock = card.select_one(".availability")
            rating = card.select_one("p.star-rating")
            rating_word = next((c for c in rating.get("class", []) if c in RATINGS), "") if rating else ""
            if title:
                rows.append({
                    "title": title.get("title", title.get_text(strip=True)),
                    "price": price.get_text(strip=True) if price else "",
                    "rating": RATINGS.get(rating_word, ""),
                    "availability": " ".join(stock.stripped_strings) if stock else "",
                    "product_url": urljoin(url, title.get("href", "")),
                })
        nxt = soup.select_one("li.next a")
        url = urljoin(url, nxt.get("href")) if nxt else None
        page += 1
        if url:
            time.sleep(0.6)
    return rows

@app.get("/")
def home():
    return render_template("index.html", books=latest_rows)

@app.post("/scrape")
def scrape():
    global latest_rows
    pages = request.form.get("pages", "3")
    try:
        pages = max(1, min(int(pages), 5))
        latest_rows = scrape_books(pages)
        return render_template("index.html", books=latest_rows,
                               message=f"Successfully collected {len(latest_rows)} books from {pages} page(s).")
    except (requests.RequestException, ValueError) as exc:
        return render_template("index.html", books=latest_rows,
                               error=f"Scraping failed: {exc}. Please try again later."), 502

@app.get("/download")
def download():
    if not latest_rows:
        return ("No scraped data yet. Click Start Scraping first.", 400)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(latest_rows[0].keys()))
    writer.writeheader()
    writer.writerows(latest_rows)
    mem = io.BytesIO(output.getvalue().encode("utf-8-sig"))
    mem.seek(0)
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="scraped_books.csv")

@app.get("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
