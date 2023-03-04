from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.job_adding_form import JobForm, make_datetime_from_str
from forms.login_form import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_page():
    db_sess = db_session.create_session()
    return render_template('index.html', jobs_list=db_sess.query(Jobs).all(), title='Миссия колонизация Марса')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def login():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.email = form.login.data
        ...
    return render_template('register_form.html', title='Регистрация', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = make_datetime_from_str(form.start_date.data)
        job.end_date = make_datetime_from_str(form.end_date.data)
        job.is_finished = form.is_finished.data

        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template('job_init.html', title='Добавленмие работы', form=form)


if __name__ == '__main__':
    main()
