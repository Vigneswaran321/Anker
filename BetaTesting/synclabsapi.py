from flask import Flask, render_template, send_file, send_from_directory
import requests
from bs4 import BeautifulSoup
import openai
import time

app = Flask(__name__)

# Your API key for OpenAI
API_KEY = '6e8df25c-fdee-4db0-8ff7-1adbe8d532fa'

def request_video_processing(audio_url, video_url):
    url = 'https://api.synclabs.so/video'
    headers = {
        'accept': 'application/json',
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "audioUrl": audio_url,
        "videoUrl": video_url,
        "synergize": True,
        "maxCredits": 800,
        "webhookUrl": None,
        "model": "sync-1.5-beta"
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def download_video(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

@app.route('/')
def index():
    # Example of generating news content
    # news_headlines = generate_news_content()
    # Select the first headline
    # first_headline = news_headlines[0]
    # Generate audio for the first headline
    # audio_response = generate_news_audio(first_headline)
    # audio_response.write_to_file('output.mp3')
    # Example of request_video_processing
    audio_url = "https://anker-xi.vercel.app/video/output.mp3"
    video_url = "https://anker-xi.vercel.app/video/input.mp4"
    response = request_video_processing(audio_url, video_url)
    video_id = response['id']
    time.sleep(300)  # Wait for 5 minutes
    while True:
        status_response = requests.get(f'https://api.synclabs.so/video/{video_id}', headers={'x-api-key': API_KEY})
        status = status_response.json()['status']
        if status == 'COMPLETED':
            download_url = status_response.json()['url']
            download_video(download_url, 'result_video.mp4')
            break
        time.sleep(60)  # Check status every minute
    return "Video processing completed and downloaded."

@app.route('/video')
def video():
    # Path to your video file
    video_path = 'result_video.mp4'
    return send_file(video_path, as_attachment=True)

@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
