import requests
from flask import Flask, request, Response

app = Flask(__name__)

# Define the SyncLabs API key
sync_labs_api_key = "YOUR_SYNC_LABS_API_KEY"

# Endpoint for lip sync process
@app.route('/lip-sync', methods=['POST'])
def lip_sync():
    # Ensure the method is POST
    if request.method != 'POST':
        return Response(
            '{"error": {"statusCode": 405, "message": "Method Not Allowed"}}',
            status=405,
            mimetype='application/json'
        )

    # Parse the JSON body of the request
    data = request.json
    video_url = data.get('videoUrl')
    audio_url = data.get('audioUrl')

    # Check if the values exist
    if not video_url or not audio_url:
        return Response(
            '{"error": {"statusCode": 400, "message": "Missing videoUrl or audioUrl in the request body."}}',
            status=400,
            mimetype='application/json'
        )

    # Validate URLs
    if not is_valid_url(video_url) or not is_valid_url(audio_url):
        return Response(
            '{"error": {"statusCode": 400, "message": "Invalid URL provided"}}',
            status=400,
            mimetype='application/json'
        )

    # Send the request to SyncLabs API
    sync_labs_api_url = "https://api.synclabs.so"
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': sync_labs_api_key
    }
    payload = {
        'audioUrl': audio_url,
        'videoUrl': video_url,
        'synergize': True,
        'webhookUrl': f"{request.url_root}api/lip-sync/webhook",
        'model': 'sync-1'
    }
    response = requests.post(sync_labs_api_url, json=payload, headers=headers)

    if not response.ok:
        error_message = f"Failed to lip sync video to audio: {response.status_code} {response.text}"
        return Response(
            f'{{"error": {{"statusCode": {response.status_code}, "message": "{error_message}"}}}}',
            status=response.status_code,
            mimetype='application/json'
        )

    data = response.json()
    video_response = requests.get(data['videoUrl'])

    # Save the video as result.mp4
    with open('result.mp4', 'wb') as video_file:
        video_file.write(video_response.content)

    return Response(
        '{"message": "Video downloaded successfully"}',
        status=200,
        mimetype='application/json'
    )

def is_valid_url(url):
    # You can implement your URL validation logic here
    return True  # Placeholder implementation

if __name__ == '__main__':
    app.run(debug=True)
