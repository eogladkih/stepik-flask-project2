import os
import json
import random

from flask import Flask, render_template, request as flask_req
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sd;lfjsalfh;sajf;ldsa;cdsa;flsmc.,xzlksahkflh'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


with open('teachers.json', 'r') as t:
    teachers = json.load(t)

with open('goals.json', 'r') as t:
    goals_dict = json.load(t)

day_dict = {"mon": "Понедельник",
            "tue": "Вторник",
            "wed": "Среда",
            "thu": "Четверг",
            "fri": "Пятница",
            "sat": "Суббота",
            "sun": "Воскресенье"}


def t_free(teacher_id):

    free_time = {}
    for en_day, ru_day in day_dict.items():
        free_td = []
        for item in teachers:
            if item['id'] == teacher_id:
                for k, v in item['free'][en_day].items():
                    if v:
                        free_td.append(k)
                free_time[en_day] = free_td
    return free_time


def get_teacher(id):
    for item in teachers:
        if item['id'] == id:
            return item
    else:
        return False


def get_by_goal(goal):
    getbygoal_list = []
    for item in teachers:
        if goal in item['goals']:
            getbygoal_list.append(item)
    return getbygoal_list


def get_rnd_teachers():
    random6 = random.choices(teachers, k=6)
    return random6


# SQLAlchemy Classes
class DictDay(db.Model):
    __tablename__ = 'dict_days'
    id = db.Column(db.Integer, primary_key=True)
    day_ru = db.Column(db.String, unique=True, nullable=False)
    day_en = db.Column(db.String, unique=True, nullable=False)


class DictGoal(db.Model):
    __tablename__ = 'dict_goals'
    id = db.Column(db.Integer, primary_key=True)
    goal_ru = db.Column(db.String, unique=True, nullable=False)
    goal_en = db.Column(db.String, unique=True, nullable=False)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    json_id = db.Column(db.Integer)
    name = db.Column(db.String, unique=True, nullable=False)
    about = db.Column(db.String)
    free = db.Column(db.JSON)
    goals = db.Column(db.String)
    picture = db.Column(db.String)
    price = db.Column(db.Integer)
    rating = db.Column(db.Float)
    students = db.relationship('Booking', backref='teacher')


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String)
    student_phone = db.Column(db.String, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    day = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    client_purpose = db.Column(db.String, nullable=False)
    client_time = db.Column(db.String, nullable=False)
    client_name = db.Column(db.String)
    client_phone = db.Column(db.String, nullable=False)


# FlaskForm Classes
class OrderForm(FlaskForm):
    clientName = StringField('Вас зовут', validators=[InputRequired()])
    clientPhone = StringField('Ваш телефон', validators=[InputRequired()])
    clientSubmit = SubmitField('Записаться на пробный урок')


class RequestForm(FlaskForm):
    clientPurpose = RadioField('clientPurpose', choices=[("travel", "Для путешествий"), ("study", "Для школы"),
                                                         ("work", "Для работы"), ("relocate", "Для переезда")])
    clientTime = RadioField('clientTime', choices=[("1-2", "1-2 часа в неделю"), ("3-5", "3-5 часа в неделю"),
                                                   ("5-7", "5-7 часа в неделю"), ("7-10", "7-10 часа в неделю")])
    clientName = StringField('Вас зовут')
    clientPhone = StringField('Ваш телефон')
    clientSubmit = SubmitField('Найдите мне преподавателя')


@app.route('/')
def index():
    data = get_rnd_teachers()
    return render_template("index.html", data=data)


@app.route('/all')
def all():
    teachers_count = len(teachers)
    return render_template('all.html', data=teachers, num=teachers_count)


@app.route('/goals/<goal>/')
def goals(goal):
    data = get_by_goal(goal)
    return render_template('goal.html', data=data, goal=goal, goals_dict=goals_dict)


@app.route('/profiles/<int:id_teacher>/')
def profiles(id_teacher):
    item = get_teacher(id_teacher)
    if item:
        free_time = t_free(id_teacher)
        return render_template('profile.html', data=item, free_time=free_time, day_dict=day_dict, goals_dict=goals_dict)
    return render_template('page_not_found.html'), 404


@app.route('/request/')
def request():
    form = RequestForm()
    return render_template('request.html', form=form)


@app.route('/request_done/', methods=['GET', 'POST'])
def request_done():
    if flask_req.method == 'POST':
        return render_template('request_done.html')


@app.route('/booking/<int:id_teacher>/<string:dw>/<time>/')
def booking_form(id_teacher, dw, time):
    data = get_teacher(id_teacher)
    form = OrderForm()
    return render_template('booking.html', data=data, dw=dw, time=time, day_dict=day_dict, id=id_teacher, form=form)


@app.route('/booking_done/', methods=["GET", "POST"])
def booking_done():
    if flask_req.method == 'POST':
        return render_template('booking_done.html')


if __name__ == "__main__":
    app.run(debug=True)
