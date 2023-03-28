from flask import Flask, render_template

app = Flask(__name__)


@app.route('/wellcome')
def wellcome_page():
    return render_template('wellcome.html')


@app.route('/')
@app.route('/index')
def main_page():
    return render_template('main.html')


@app.route('/create_test')
def create_test_page():
    return render_template('create_test.html')


if __name__ == '__main__':
    try:
        app.run(port=8080, host='127.0.0.1')
    except Exception as e:
        print(e)
