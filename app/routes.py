import sqlite3
from datetime import datetime

import shows
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required, login_manager
from werkzeug.urls import url_parse

from app import app, db
from app.forms import NewShowForm, LoginForm, RegistrationForm
from app.models import Show, Producer, Actor, ActorToShow, User


#app password: pshl ypwr bpnp alpn
@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html", title='Home')


@app.route('/show_list')
def show_list():
    #list_shows = ["Money Heist", "The 100", "Prison Break", "Breaking Bad"]
    show_list = Show.query.all()
    return render_template("show_list.html", title="Tv Show", show_list=show_list)


@app.route('/show/<title>')
def show(title):
    show = Show.query.filter_by(title=title).first_or_404()
    return render_template("show.html", show=show, title=show.title, date=show.date, description=show.description)


@app.route('/new_show', methods=['GET', 'POST'])
@login_required
def new_show():
    form = NewShowForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():

        # conn = sqlite3.connect('app.db')
        # cursor = conn.cursor()
        # sql_query = "SELECT COUNT(*) AS id FROM Show"
        # cursor.execute(sql_query)
        # id_count = cursor.fetchone()[0]
        # conn.close()
        # id_count = id_count + 1
        add_show =Show( title=form.show_title.data,
                               date=form.date.data, description=form.description.data)
        db.session.add(add_show)
        db.session.commit()

        flash('New TV Show has been created'.format(form.show_title.data, form.date.data, form.actor.data, form.description.data))
        return render_template('show.html', form=form, title=form.show_title.data,
                               date=form.date.data, description=form.description.data)
    return render_template("new_show.html", form=form, title=form.show_title.data,
                           date=form.date.data, description=form.description.data)


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    s1 = Show(id=1, title="Money Heist", date="December 20, 2017", description="An unusual group of robbers attempt to carry out the most perfect robbery in Spanish history")
    db.session.add(s1)
    db.session.commit()

    s2 = Show(id=2, title="Prison Break", date="August 29, 2005", description="A structural engineer installs himself in a prison he helped design in order to save his falsely accused brother from a death sentence by breaking themselves out from the inside")
    db.session.add(s2)
    db.session.commit()

    s3 = Show(id=3, title="The 100", date="March 19, 2014", description="Set 97 years after a nuclear war destroyed civilization when a spaceship housing humanity's lone survivors sends 100 juvenile delinquents back to Earth hoping to repopulate the planet")
    db.session.add(s3)
    db.session.commit()

    s4 = Show(id=4, title="The Office", date="March 24, 2005",
              description="A mockumentary on a group of typical office workers, where the workday consists of ego clashes, inappropriate behavior, and tedium.")
    db.session.add(s4)
    db.session.commit()

    p2 = Producer(id=2, firstname="Alex", lastname="Pina")
    db.session.add(p2)
    db.session.commit()

    p3 = Producer(id=3, firstname="Zack", lastname="Estrin")
    db.session.add(p3)
    db.session.commit()

    p4 = Producer(id=4, firstname="Jason", lastname="Rothenberg")
    db.session.add(p4)
    db.session.commit()

    a2 = Actor(id=2, firstname="Alvaro", lastname="Morte", age=48)
    db.session.add(a2)
    db.session.commit()

    a3 = Actor(id=3, firstname="Wentworth", lastname="Miller", age=51)
    db.session.add(a3)
    db.session.commit()

    a4 = Actor(id=4, firstname="Eliza", lastname="Taylor", age=33)
    db.session.add(a4)
    db.session.commit()

    a2s1 = ActorToShow(actor_id=a2.id, show_id=s1.id)
    db.session.add(a2s1)
    db.session.commit()

    return render_template("main.html")


# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

