from flask import Flask

app = Flask(__name__)


@app.route('/monitoring/health')
def check_health():
    return 'OK'


if __name__ == '__main__':
    app.run()
