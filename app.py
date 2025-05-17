# app.py
from flask import Flask, request, jsonify, send_from_directory
from requests_html import HTMLSession
from urllib.parse import quote_plus
import os

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/search')
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Chýba dotaz"}), 400

    session = HTMLSession()
    url = f"https://www.google.com/search?q={quote_plus(query)}&hl=cs"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = session.get(url, headers=headers)
    r.html.render(timeout=20)

    results = []
    for result in r.html.find("div.g"):
        title_el = result.find("h3", first=True)
        link_el = result.find("a", first=True)
        if title_el and link_el:
            results.append({
                "title": title_el.text,
                "url": link_el.attrs.get("href")
            })

    # Uložíme do JSON souboru
    with open("vysledky.json", "w", encoding="utf-8") as f:
        import json
        json.dump(results, f, ensure_ascii=False, indent=2)

    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
