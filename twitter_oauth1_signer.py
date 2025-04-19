from flask import Flask, request, jsonify
from requests_oauthlib import OAuth1
import requests
import os

app = Flask(__name__)

# Load credentials from environment variables
CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")

@app.route("/")
def home():
    return "Twitter OAuth1 Signer Running"

@app.route("/upload-media", methods=["POST"])
def upload_media():
    if "media" not in request.files:
        return jsonify({"error": "Missing media file"}), 400

    media = request.files["media"].read()
    oauth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

    response = requests.post(
        "https://upload.twitter.com/1.1/media/upload.json",
        files={"media": media},
        auth=oauth
    )
    return jsonify(response.json()), response.status_code

@app.route("/tweet", methods=["POST"])
def tweet():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in body"}), 400

    payload = {
        "status": data["text"]
    }
    if "media_id" in data:
        payload["media_ids"] = data["media_id"]

    oauth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

    response = requests.post(
        "https://api.twitter.com/1.1/statuses/update.json",
        data=payload,
        auth=oauth
    )
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
