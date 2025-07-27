from flask import Flask, request, jsonify
import requests
import re
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "Instagram Reels Downloader API is working!"

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        shared_data = re.search(r"window\.__additionalDataLoaded\('extra',(.*?)\);</script>", res.text)
        
        if not shared_data:
            return jsonify({"error": "Could not parse video data"}), 400

        json_data = json.loads(shared_data.group(1))
        video_url = json_data['graphql']['shortcode_media']['video_url']
        
        return jsonify({"video_url": video_url})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
