from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World-feature AAAA!"

if __name__ == '__main__':
    # Get the port from the environment variable, default to 8083 if not set
    port = int(os.environ.get('FLASK_PORT', 8083))
    app.run(port=port)

