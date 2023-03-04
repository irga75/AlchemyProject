import datetime

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, IntegerField, StringField, DateTimeField
from wtforms.validators import DataRequired, ValidationError


def make_datetime_from_str(one_string):
    if one_string:
        one_list = ['year', 'month', 'day', 'hour', 'minute']
        two_list = [int(x) for x in one_string.split()[0].split('.')] + [int(x) for x in one_string.split()[1].split(':')]
        one_dict = {}
        for i, value in enumerate(two_list):
            one_dict[one_list[i]] = value
        return datetime.datetime(**one_dict)


def my_date_check(form, field):
        try:
            make_datetime_from_str(field.data)
        except Exception:
            raise ValidationError('Not a valid datetime value.')


class JobForm(FlaskForm):
    team_leader = IntegerField('Id тимлида', validators=[DataRequired()])
    job = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Размер работы (в часах)', validators=[DataRequired()])
    collaborators = StringField('Участники')
    start_date = StringField('Время начала работы в формате Year.month.day hour:minute', validators=[my_date_check])
    end_date = StringField('Время окончания работы в формате Year.month.day hour:minute', validators=[my_date_check])
    is_finished = BooleanField('Закончена ли работа')
    submit = SubmitField('Отправить')
