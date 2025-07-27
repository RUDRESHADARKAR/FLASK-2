from flask import Flask, request, redirect, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Instagram Reels Downloader API is working!"

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    og_video = soup.find('meta', property='og:video')
    if og_video:
        video_url = og_video['content']
        return render_template_string(
            f"<video controls src='{video_url}' width='320'></video><br><a href='{video_url}' download>Download</a>")
    return "Could not fetch video. Make sure it's public."

if __name__ == '__main__':
    app.run()
