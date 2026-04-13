#!/usr/bin/env python3
from flask import Flask, send_from_directory
import os

app = Flask(__name__)
DATA_DIR = os.path.expanduser("~/gcs/data")

@app.route('/phb_global_state.npy')
def serve_state():
    return send_from_directory(DATA_DIR, 'phb_global_state.npy')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
