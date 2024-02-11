from flask import Flask, render_template, send_file, send_from_directory
import requests
from bs4 import BeautifulSoup
import openai
import time

app = Flask(__name__)

def request_video_processing():
    url = "https://api.d-id.com/clips"

    payload = {
        "script": {
            "type": "audio",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
            },
            "ssml": "false",
            "audio_url": "https://anker-xi.vercel.app/video/output.mp3"
        },
        "config": { "result_format": "mp4" },
        "presenter_config": { "crop": { "type": "rectangle" } },
        "presenter_id": "amy-FLZ1USJl7m"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic Y21WaGNHVnlaMkZ0YVc1bk1UTTFRR2R0WVdsc0xtTnZiUTpENjVEa3FTOEdtOUNjX1JSZTJCY2c="
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    id = response_data.get('id')
    print(f"Video_id: {id}")
    return id

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
    video_id = request_video_processing()

    url = f"https://api.d-id.com/clips/{video_id}"
    headers = {
        "accept": "application/json",
        "authorization": "Basic Y21WaGNHVnlaMkZ0YVc1bk1UTTFRR2R0WVdsc0xtTnZiUTpENjVEa3FTOEdtOUNjX1JSZTJCY2c="
    }
    while True:
        response = requests.get(url, headers=headers)
        response_data = response.json()

        result_url = response_data.get('result_url')
        download_video(result_url, 'result_video.mp4')
        break
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
