from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/all')
def all():
    return render_template('all.html')


@app.route('/goals/<goal>/')
def goals(goal):
    return render_template('goal.html')


@app.route('/profiles/<id_teacher>/')
def profiles(id_teacher):
    return render_template('profile.html')


@app.route('/request/')
def request():
    return render_template('request.html')


@app.route('/request_done/')
def request_done():
    return render_template('request_done.html')


@app.route('/booking/<id_teacher>/<dw>/<time>/')
def booking_form():
    return render_template('booking.html')


@app.route('/booking_done/')
def booking_done():
    return render_template('booking_done.html')


if __name__ == "__main__":
    app.run(debug=True)