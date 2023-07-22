from flask import Flask

from cron import setup_cron

app = Flask(__name__)

setup_cron(app)


@app.route('/monitoring/health')
def check_health() -> str:
    return 'OK'


if __name__ == '__main__':
    app.run()
