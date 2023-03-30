import json
from flask import Flask, render_template, request
from data import db_session


app = Flask(__name__)
with open('data/keys.json', 'r', encoding='utf-8') as file:
    data = json.loads(file.read())
    app.config['SECRET_KEY'] = data['secret_key']


def main():
    try:
        db_session.global_init("db/blogs.db")
        app.run(port=8080, host='127.0.0.1', debug=True)
    except Exception as e:
        print(e)


@app.route('/register', methods=['GET', 'POST'])
def wellcome_page():
    if request.method == 'POST':
        data = request.data
        print(data)
        
        # перенаправить на другую страницу
    return render_template('register.html')


@app.route('/')
@app.route('/index')
def main_page():
    return render_template('main.html')


@app.route('/create_test')
def create_test_page():
    return render_template('create_test.html')


if __name__ == '__main__':
    main()
