from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Instagram Reels Downloader API is working!"

@app.route('/download', methods=['POST'])
def download():
    # Accept both JSON and form-data input
    url = request.json.get('url') if request.is_json else request.form.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    og_video = soup.find('meta', property='og:video')

    if og_video:
        video_url = og_video['content']
        return jsonify({"video_url": video_url})
    else:
        return jsonify({"error": "Could not fetch video. Make sure it's public."}), 400

if __name__ == '__main__':
    app.run()
