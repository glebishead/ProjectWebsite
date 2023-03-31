import json
from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
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


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return redirect('/')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    error = False
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_again = request.form.get('password_again')
        if not (password == password_again):
            error = 'Passwords is not the same'
        else:
            pass
        #     # message
        # # записать в бд
        # password = password_again = generate_password_hash(password)
        # if not check_password_hash(хэшированный из бд, вводимый):
        #     # ошибка
    return render_template('register.html', error=error)


@app.route('/')
@app.route('/index')
def main_page():
    return render_template('main.html')


@app.route('/create_test')
def create_test_page():
    return render_template('create_test.html')


if __name__ == '__main__':
    main()
