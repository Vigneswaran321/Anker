from flask import Flask, render_template, send_file, send_from_directory
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

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

@app.route('/')
def index():
    # Generate news content
    #news_headlines = generate_news_content()
    # Select the first headline
    #first_headline = news_headlines[0]
    # Generate audio for the first headline
    #audio_response = generate_news_audio(first_headline)
    #audio_response.write_to_file('output.mp3')
    # Serve the video player
    return render_template('index.html')

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
