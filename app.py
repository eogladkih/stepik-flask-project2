from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'здесь будет главная'


@app.route('/all')
def all():
    return 'здесь будут преподаватели'


@app.route('/goals/<goal>/')
def goals(goal):
    return 'здесь будет цель <goal>'


@app.route('/profiles/<id_teacher>/')
def profiles(id_teacher):
    return 'здесь будет преподаватель <id учителя>'


@app.route('/request/')
def request():
    return 'здесь будет заявка на подбор,'


@app.route('/request_done/')
def request_done():
    return 'заявка на подбор отправлена'


@app.route('/booking/<id_teacher>/<dw>/<time>/')
def booking_form():
    return 'здесь будет форма бронирования <id учителя>'


@app.route('/booking_done/')
def booking_done():
    return 'заявка отправлена'


if __name__ == "__main__":
    app.run(debug=True)