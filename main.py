import json
from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from data import db_session
from data.users import User
from data.tests import Tests


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
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


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = request.form.get('remember')
        db_sess = db_session.create_session()
        try:
            user = db_sess.query(User).filter(User.email == email).first()
            if user and user.check_password(password):
                login_user(user, remember=bool(remember_me))
                flash('Вы успешно вошли в аккаунт')
                return redirect('/')
            raise AttributeError
        except AttributeError:
            flash('Неправильный логин или пароль')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    global strong_symbols
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_again = request.form.get('password_again')
        remember_me = request.form.get('remember')
        username = request.form.get('username')
        
        if password != password_again:
            flash('Пароли не совпадают')
        else:
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == email).first():
                flash('Пользователь уже зарегистрирован в системе')
            elif (len(password) >= 6 and [*filter(lambda x: x in strong_symbols, password)]) or (len(password) >= 8):
                user = User(name=username,
                            email=request.form.get('email'),
                            hashed_password=generate_password_hash(password))
                db_sess.add(user)
                db_sess.commit()
                flash("Пользователь добавлен")
                logout_user()
                login_user(user, remember=bool(remember_me))
                return redirect('/')
            else:
                flash("Пароль слабый")
    return render_template('register.html')


@app.route('/')
@app.route('/index')
def main_page():
    return render_template('main.html')


@app.route('/create_test', methods=['GET', 'POST'])
@login_required
def create_test_page():
    try:
        test_name = request.form.get('test_name')
        description = request.form.get('description')
        test_type = request.form.get('type')
        
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        test_ = Tests(name=test_name, creator=user,
                      description=description, test_type=test_type)
        db_sess.add(test_)
        db_sess.commit()
        flash('Заготовка для теста успешно создана!')
        
    except Exception as e:
        print(e)
        flash('Извините, что-то пошло не так')
    return render_template('create_test.html')


@app.route('/go_test', methods=['GET', 'POST'])
def go_test_page():
    test_name = "Первая анкета (>_<)"
    question_list = [{"name": "Сколько Вам лет?", "variants": ["0-10", "10-20", "20-30", "30-40", "50-60", "60+"]},
                     {"name": "Как Ваше настроение?", "variants": ["Очень хорошо", "Хорошо",
                                                                   "Нормально", "Плохо", "Очень плохо"]},
                     {"name": "Как Вам выступление?", "variants": ["Очень хорошо", "Хорошо",
                                                                   "Нормально", "Плохо", "Очень плохо"]}]
    return render_template('go_test.html', test_name=test_name, question_list=question_list)


if __name__ == '__main__':
    main()
