#!/usr/bin/env python3
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

STATE_FILE = Path(__file__).parent / 'state.json'

DEFAULT_STATE = {"tasks": [], "notes": [], "events": [], "blocks": [], "lastModified": None}

def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_state(data):
    data['lastModified'] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    return data

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(load_state())

@app.route('/api/state', methods=['POST'])
def update_state():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    return jsonify(save_state(data))

@app.route('/api/ping')
def ping():
    return jsonify({"status": "ok"})

@app.route('/')
def index():
    return send_file('index.html')

if __name__ == '__main__':
    if not STATE_FILE.exists():
        save_state(DEFAULT_STATE.copy())
    app.run(host='0.0.0.0', port=8080)
