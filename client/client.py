
from flask import Flask, send_from_directory, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('assets', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

