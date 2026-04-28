import os
from flask import Flask, request, jsonify, send_from_directory
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

APOFY_TOKEN = os.getenv("APIFY_TOKEN")
if not APOFY_TOKEN:
    raise RuntimeError("APIFY_TOKEN is not set")

ACTOR_ID = "compass/crawler-google-places"
client = ApifyClient(APOFY_TOKEN)
app = Flask(__name__, static_folder="static", static_url_path="/static")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json(force=True)
    query = data.get("query", "").strip()
    location = data.get("location", "").strip()

    if not query or not location:
        return jsonify({"error": "query and location are required"}), 400

    full_query = f"{query} in {location}"

    try:
        run = client.actor(ACTOR_ID).call(
            run_input={
                "searchStringsArray": [full_query],
                "maxCrawledPlacesPerSearch": 50,
            }
        )
        dataset_client = client.dataset(run["defaultDatasetId"])
        items = dataset_client.list_items().items

        simplified = []
        for item in items:
            simplified.append({
                "name": item.get("title") or item.get("name"),
                "address": item.get("address"),
                "rating": item.get("totalScore") or item.get("rating"),
                "reviews": item.get("reviewsCount"),
                "phone": item.get("phone"),
                "website": item.get("website"),
                "url": item.get("url"),
            })

        return jsonify({"results": simplified})

    except Exception as e:
        print("Apify error:", e)
        return jsonify({"error": "Failed to fetch data from Apify"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
