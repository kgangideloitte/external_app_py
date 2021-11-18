import os
from flask import Flask, render_template, request, redirect
import requests
import logging
import json

URL = os.environ.get("SERVER", "http://localhost:8082")
DEBUG = os.environ.get("DEBUG", True)
PORT = os.environ.get("PORT", 5000)

app = Flask(__name__)

@app.route("/")
def home():
  logging.info('home page requested')
  try:
    data = requests.get(URL + '/events').content
    # Parse JSON into a python object with attributes corresponding to dict keys.
    model = json.loads(data)
  except Exception:
    # backend is down, so provide alternative data
    model = {}
  return render_template("home.html", model=model)

@app.route("/event", methods=['POST'])
def create_happening():
  logging.info('event submitted')
  headers = {
      'Content-Type': 'application/json'
  }
  data = request.form.to_dict(flat=True)
  requests.post(URL + '/event', headers=headers, data=json.dumps(data))
  return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
