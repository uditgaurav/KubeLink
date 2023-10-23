from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)
CORS(app)

GITHUB_REPO = 'uditgaurav/KubeLink'
TOKEN = os.environ.get('GITHUB_TOKEN')
API_URL = f'https://api.github.com/repos/{GITHUB_REPO}/dispatches'

@app.route('/triggerClusterCreation', methods=['POST'])
def trigger_cluster_creation():
    # Define the event type for the GitHub Action
    event_type = 'create-cluster'

    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.everest-preview+json',
        'Content-Type': 'application/json'
    }

    data = {
        'event_type': event_type
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 204:
        return jsonify(status='in-progress')
    else:
        return jsonify(status='error', message=response.text), 500

if __name__ == '__main__':
    app.run(debug=True)
