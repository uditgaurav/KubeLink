from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://34.123.163.92:5000"}})

GITHUB_REPO = 'uditgaurav/KubeLink'
TOKEN = os.environ.get('GITHUB_TOKEN')
DISPATCH_API_URL = f'https://api.github.com/repos/{GITHUB_REPO}/dispatches'
RUNS_API_URL = f'https://api.github.com/repos/{GITHUB_REPO}/actions/runs'

@app.route('/triggerClusterCreation', methods=['POST'])
def trigger_cluster_creation():
    event_type = 'create-cluster'
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.everest-preview+json',
        'Content-Type': 'application/json'
    }
    data = {
        'event_type': event_type
    }
    response = requests.post(DISPATCH_API_URL, headers=headers, json=data)
    if response.status_code == 204:
        return jsonify(status='in-progress')
    else:
        return jsonify(status='error', message=response.text), 500

@app.route('/getClusterCreationStatus', methods=['GET'])
def get_cluster_status():
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(RUNS_API_URL, headers=headers)
    if response.status_code == 200:
        runs = response.json().get('workflow_runs', [])
        if runs:
            latest_run = runs[0]
            return jsonify(status=latest_run['status'], conclusion=latest_run['conclusion'])
        else:
            return jsonify(message="No workflow runs found"), 404
    else:
        return jsonify(status='error', message=response.text), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
