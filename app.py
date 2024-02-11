from flask import Flask, render_template, send_file, send_from_directory, stream_with_context
import requests
from bs4 import BeautifulSoup
import openai
import time
import os
import random

app = Flask(__name__)

@app.route('/')
def index():
        # Example of generating news content
    news_headlines = generate_news_content()
    # Select the first headline
    first_headline = news_headlines[0]
    # Generate audio for the first headline
    audio_response = generate_news_audio(first_headline)
    audio_response.write_to_file('static\output.mp3')
    audio_url = "https://anker-xi.vercel.app/video/output.mp3"
    video_url = "https://anker-xi.vercel.app/video/input.mp4"
    response = request_video_processing(audio_url, video_url)
    video_id = response['id']
    while True:
        status_response = requests.get(f'https://api.synclabs.so/video/{video_id}', headers={'x-api-key': API_KEY})
        status = status_response.json()['status']
        if status == 'COMPLETED':
            download_url = status_response.json()['url']
            download_video(download_url, os.path.join('headlines', f'result_video_{i}.mp4'))
            i += 1
            break
        time.sleep(60)  # Check status every minuterequest_video_processing()
    return render_template('index.html')

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


def generate_news_content():
    # send a GET request to the page
    url = 'https://www.prnewswire.com/news-releases/news-releases-list/'
    response = requests.get(url)
    # create a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    # find the element with class 'card-title' and the text
    ele = soup.find_all('h3')
    ele.pop() 
    news_headlines = [j.text for j in ele]
    return news_headlines

def generate_news_audio(headline):
    api_key = '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'
    client = openai.Client(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a AI News Anchor acting similar like a human in a way that cannot be easily detected by the way of speaking and generate the content like a news anchor based upon the headlines received."},
            {"role": "user", "content": headline}
        ]
    )
    audio_content = completion.choices[0].message.content
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=audio_content
    )
    return response

def download_video(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Path to the folder containing video files
folder_path = 'headlines'
# List all files in the folder
video_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
# Shuffle the list to play files in random order
random.shuffle(video_files)
# Convert list to queue for FIFO behavior
video_queue = video_files.copy()

@app.route('/video')
def video():
    global video_queue
    
    if not video_queue:
        # If the queue is empty, refill it with the original list of video files
        video_queue = video_files.copy()
    
    # Get the next video file from the queue
    next_video = video_queue.pop(0)
    # Path to the next video file
    video_path = os.path.join(folder_path, next_video)
    return stream_with_context(play_video(video_path))

def play_video(video_path):
    with open(video_path, 'rb') as f:
        while True:
            # Read 1MB of data from the video file
            chunk = f.read(1024*1024)
            if not chunk:
                break
            yield chunk
            
@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
