from flask import Flask, render_template
import json

app = Flask(__name__)


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

# print(goals['relocate'])

def t_free(teacher_id):

    free_time = {}
    for en_day, ru_day in day_dict.items():
        free_td = []
        for item in teachers:
            if item['id'] == teacher_id:
                for k, v in item['free'][en_day].items():
                    if v:
                        free_td .append(k)
                #free_time[ru_day] = free_td
                free_time[en_day] = free_td
    return free_time


def getteacher(id):
    for item in teachers:
        if item['id'] == id:
            return item
    else:
        return False





# print(t_free(1))

# def get_goals(teacher_id):
#     for item in teachers:
#         if item['id'] == teacher_id:
#             goal_list = []
#             for i in item['goals']:
#                 goal_list.append(goals[i])
#             return goal_list
#
#
# print(get_goals(0))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/all')
def all():
    return render_template('all.html')


@app.route('/goals/<goal>/')
def goals(goal):
    return render_template('goal.html')


@app.route('/profiles/<int:id_teacher>/')
def profiles(id_teacher):
    if getteacher(id_teacher):
        item = getteacher(id_teacher)
        free_time = t_free(id_teacher)
        return render_template('profile.html', data=item, free_time=free_time, day_dict=day_dict, goals_dict=goals_dict)
    return render_template('page_not_found.html'), 404


@app.route('/request/')
def request():
    return render_template('request.html')


@app.route('/request_done/')
def request_done():
    return render_template('request_done.html')


@app.route('/booking/<int:id_teacher>/<string:dw>/<time>/')
def booking_form(id_teacher, dw, time):
    data = getteacher(id_teacher)
    return render_template('booking.html', data=data, dw=dw, time=time, day_dict=day_dict, id=id_teacher )


@app.route('/booking_done/')
def booking_done():
    return render_template('booking_done.html')


if __name__ == "__main__":
    app.run(debug=True)