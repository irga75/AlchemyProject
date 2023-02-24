from flask import Flask, render_template
from data import db_session
from data.jobs import Jobs

db_session.global_init("db/blogs.db")

db_sess = db_session.create_session()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def jobs_table():
    return render_template('index.html', jobs_list=db_sess.query(Jobs).all())


def main():
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()
