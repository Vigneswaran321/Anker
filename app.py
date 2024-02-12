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
    # news_headlines = generate_news_content()
    # # Select the first headline
    # first_headline = news_headlines[0]
    # # Generate audio for the first headline
    # audio_response = generate_news_audio(first_headline)
    # audio_response.write_to_file('static\output.mp3')
    # video_id = request_video_processing()
    # print(video_id)
    # url = f"https://api.d-id.com/clips/{video_id}"
    # headers = {
    #     "accept": "application/json",
    #     "authorization": "Basic Y21WaGNHVnlaMkZ0YVc1bk1UTTFRR2R0WVdsc0xtTnZiUTpENjVEa3FTOEdtOUNjX1JSZTJCY2c="
    # }
    # timeout = 60  # Set a timeout of 60 seconds
    # start_time = time.time()

    # while True:
    #     if time.time() - start_time > timeout:
    #         return "Video processing timed out."
        
    #     response = requests.get(url, headers=headers)
    #     response.raise_for_status()
    #     response_data = response.json()
        
    #     result_url = response_data.get('result_url')
    #     if result_url:
    #         download_video(result_url, os.path.join('headlines', f'result_video_{i}.mp4'))
    #         i += 1
    #         break
    #     else:
    #         time.sleep(10)  # Wait for 5 seconds before checking again
    return render_template('index.html')


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
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJvZHVjdF9pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vc3RyaXBlX2N1c3RvbWVyX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJvZHVjdF9uYW1lIjoidHJpYWwiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9zdWJzY3JpcHRpb25faWQiOiIiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9iaWxsaW5nX2ludGVydmFsIjoibW9udGgiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9wbGFuX2dyb3VwIjoiZGVpZC10cmlhbCIsImh0dHBzOi8vZC1pZC5jb20vc3RyaXBlX3ByaWNlX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJpY2VfY3JlZGl0cyI6IiIsImh0dHBzOi8vZC1pZC5jb20vY2hhdF9zdHJpcGVfc3Vic2NyaXB0aW9uX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jaGF0X3N0cmlwZV9wcmljZV9jcmVkaXRzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jaGF0X3N0cmlwZV9wcmljZV9pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vcHJvdmlkZXIiOiJnb29nbGUtb2F1dGgyIiwiaHR0cHM6Ly9kLWlkLmNvbS9pc19uZXciOmZhbHNlLCJodHRwczovL2QtaWQuY29tL2FwaV9rZXlfbW9kaWZpZWRfYXQiOiIyMDI0LTAyLTExVDA4OjU0OjM0LjAyOVoiLCJodHRwczovL2QtaWQuY29tL29yZ19pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vYXBwc192aXNpdGVkIjpbIlN0dWRpbyIsIkNoYXQiXSwiaHR0cHM6Ly9kLWlkLmNvbS9jeF9sb2dpY19pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vY3JlYXRpb25fdGltZXN0YW1wIjoiMjAyNC0wMi0xMVQwNzowNToxOS40MTRaIiwiaHR0cHM6Ly9kLWlkLmNvbS9hcGlfZ2F0ZXdheV9rZXlfaWQiOiJldTRieGljcHJmIiwiaHR0cHM6Ly9kLWlkLmNvbS91c2FnZV9pZGVudGlmaWVyX2tleSI6Iko2VmVnSmhiUFlNaXdFSEFLMThRNyIsImh0dHBzOi8vZC1pZC5jb20vaGFzaF9rZXkiOiJMZG1kc1JGY25nVXM2bmlkbjFyS3IiLCJodHRwczovL2QtaWQuY29tL3ByaW1hcnkiOnRydWUsImh0dHBzOi8vZC1pZC5jb20vZW1haWwiOiJyZWFwZXJnYW1pbmcxMzVAZ21haWwuY29tIiwiaHR0cHM6Ly9kLWlkLmNvbS9wYXltZW50X3Byb3ZpZGVyIjoic3RyaXBlIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLmQtaWQuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA0MjMxNjE0MTQ5OTkxMTU5NjMxIiwiYXVkIjpbImh0dHBzOi8vZC1pZC51cy5hdXRoMC5jb20vYXBpL3YyLyIsImh0dHBzOi8vZC1pZC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzA3NzMzNDg2LCJleHAiOjE3MDc4MTk4ODYsImF6cCI6Ikd6ck5JMU9yZTlGTTNFZURSZjNtM3ozVFN3MEpsUllxIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCByZWFkOmN1cnJlbnRfdXNlciB1cGRhdGU6Y3VycmVudF91c2VyX21ldGFkYXRhIG9mZmxpbmVfYWNjZXNzIn0.Ii0yGgl7HSS0AUTEMBkFH91f1uzxc1UcnluHaY7MBbq8mvYAfgsDkFzs1k7_doZHXfUru1X1f_Dv3odgMLS07jgB1ngDAO8cmuH9qUOi3A1kg05NJZqnw3A0-PcQ61W4yJz-RCEay9e_-Mz-MJiwMorxPA64DL-pGPyJKwkmNfaFKawOKXCBogpVXgfbdNcqM0lp2hiTCPElk1HOYHHmfzQi6_-08jdddCC0JT6lYXnDPWT5MWuxzzrkEjEi6XR3-d4jhMpBzsiwdaw6_eBcPs3ed-mYx_4Nq69p9Ud3oYyTH0X_5ltqebSz2RAlYLdyB3Rkdgy8NK8s6VxP0WEpcg"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    response_data = response.json()
    id = response_data.get('id')
    print(f"Video_id: {id}")
    return id


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
    api_key = os.environ.get('OPENAI_API_KEY')
    client = openai.Client(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a AI News Anchor acting similar like a human in a way that cannot be easily detected by the way of speaking and generate the content in english like a news anchor based upon the headlines received."},
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
video_files = [f for f in os.listdir(
    folder_path) if os.path.isfile(os.path.join(folder_path, f))]
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
    return play_video(video_path)


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
