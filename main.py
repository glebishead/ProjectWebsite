import json
from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.users import User


app = Flask(__name__)
with open('data/keys.json', 'r', encoding='utf-8') as file:
    data = json.loads(file.read())
    app.config['SECRET_KEY'] = data['secret_key']
    strong_symbols = data['strong_symbols']


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
        db_sess = db_session.create_session()
        try:
            user = db_sess.query(User).filter(User.email == email).first()
            if user.check_password(password):
                flash('Вы успешно вошли в аккаунт')
                return redirect('/')
            else:
                flash('Неправильный логин или пароль')
        except AttributeError:
            flash("Пользователя не существует в системе")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    global strong_symbols
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_again = request.form.get('password_again')
        if password != password_again:
            flash('Пароли не совпадают')
        else:
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == email).first():
                flash('Пользователь уже зарегистрирован в системе')
            elif (len(password) >= 6 and [*filter(lambda x: x in strong_symbols, password)]) or (len(password) >= 8):
                user = User(name=f'user{db_sess.query(User).count() + 1}',
                            email=request.form.get('email'),
                            hashed_password=generate_password_hash(password))
                db_sess.add(user)
                db_sess.commit()
                flash("Пользователь добавлен")
                return redirect('/')
            else:
                flash("Пароль слабый")
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



#
#
#
#
#
#
#







