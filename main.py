from flask import Flask, render_template

app = Flask(__name__)


@app.route('/wellcome')
def wellcome_page():
    return render_template('wellcome.html', name='Jerry')


def main_page():
    return render_template('main.html', name='Jerry')


if __name__ == '__main__':
    try:
        app.run(port=8080, host='127.0.0.1')
    except Exception as e:
        print(e)
