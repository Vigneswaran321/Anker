from flask import Flask, render_template, stream_with_context
import os
import random

app = Flask(__name__)

@app.route('/')
def index():
    result_url = response_data.get('result_url')
    if result_url:
        download_video(result_url, os.path.join('headlines', f'result_video_{i}.mp4'))
        i += 1
        break
    else:
        time.sleep(10)  # Wait for 5 seconds before checking again
    return render_template('index.html')


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
    print(video_path)
    return stream_with_context(play_video(video_path))


def play_video(video_path):
    with open(video_path, 'rb') as f:
        while True:
            # Read 1MB of data from the video file
            chunk = f.read(1024*1024)
            if not chunk:
                break
            yield chunk


if __name__ == '__main__':
    app.run(debug=True)
