from flask import Flask


app = Flask(__name__)


@app.route('/<name>')
def hello(name):
    return f'hello {name}'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
