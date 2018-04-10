from flask import Flask

app = Flask(__name__)


@app.route('/api/lalala')
def hello():
    return 'Hello World! I have been seen times.ddd'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
