import sqlite3
from datetime import datetime

import shows
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required, login_manager
from werkzeug.urls import url_parse

from app import app, db
from app.forms import NewShowForm, LoginForm, RegistrationForm, NewActorForm, NewProducerForm
from app.models import Show, Producer, Actor, ActorToShow, User, ProducerToShow


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
    print(show, show.title, show.a2s[0], show.a2s[0].Actor.firstname)
    return render_template("show.html", show=show)


@app.route('/new_show', methods=['GET', 'POST'])
@login_required
def new_show():
    form = NewShowForm()

    form.actors.choices = [(a.id, a.firstname) for a in Actor.query.all()]
    form.producers.choices = [(p.id, p.firstname) for p in Producer.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        show = Show(title=form.show_title.data,
                               date=form.date.data, description=form.description.data)
        db.session.add(show)
        for actor_id in form.actors.data:
            actor = Actor.query.get(actor_id)
            if actor:
                show.a2s.append(ActorToShow(actor_id=actor_id))
            else:
                flash("Invalid actor selected")

        for producer_id in form.producers.data:
            producer = Producer.query.get(producer_id)
            if producer:
                show.p2s.append(ProducerToShow(producer_id=producer_id))
            else:
                flash("Invalid producer selected")
        db.session.commit()
        flash('Show added successfully!')
        return redirect(url_for('new_show'))

    return render_template('new_show.html', form=form)

@app.route('/new_actor', methods=['GET', 'POST'])
@login_required
def new_actor():
    form = NewActorForm()

    form.shows.choices = [(s.id, s.title) for s in Show.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        actor = Actor(firstname=form.first_name.data, lastname=form.last_name.data,
                        age=form.age.data)
        db.session.add(actor)
        for show_id in form.shows.data:
            show = Show.query.get(show_id)
            if show:
                actor.a2s.append(ActorToShow(actor_id=actor.id, show_id=show.id))
            else:
                flash("Invalid actor selected")
        db.session.add(actor)
        db.session.commit()

        flash('Actor added successfully!')
        return redirect(url_for('new_actor'))
    return render_template('new_actor.html', form=form)

@app.route('/new_producer', methods=['GET', 'POST'])
@login_required
def new_producer():
    form = NewProducerForm()

    form.shows.choices = [(s.id, s.title) for s in Show.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        producer = Producer(firstname=form.first_name.data, lastname=form.last_name.data,
                      age=form.age.data)
        db.session.add(producer)
        for show_id in form.shows.data:
            show = Show.query.get(show_id)
            if show:
                producer.p2s.append(ProducerToShow(producer_id=producer.id, show_id=show.id))
            else:
                flash("Invalid actor selected")
        db.session.add(producer)
        db.session.commit()

        flash('Producer added successfully!')
        return redirect(url_for('new_producer'))
    return render_template('new_producer.html', form=form)



@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    s1 = Show(id=1, title="Money Heist", date=datetime(2017,12,20), description="An unusual group of robbers attempt to carry out the most perfect robbery in Spanish history")
    db.session.add(s1)
    db.session.commit()

    s2 = Show(id=2, title="Prison Break", date=datetime(2005,8,29), description="A structural engineer installs himself in a prison he helped design in order to save his falsely accused brother from a death sentence by breaking themselves out from the inside")
    db.session.add(s2)
    db.session.commit()

    s3 = Show(id=3, title="The 100", date=datetime(2014,3,19), description="Set 97 years after a nuclear war destroyed civilization when a spaceship housing humanity's lone survivors sends 100 juvenile delinquents back to Earth hoping to repopulate the planet")
    db.session.add(s3)
    db.session.commit()

    s4 = Show(id=4, title="The Office", date=datetime(2005,3,24),
              description="A mockumentary on a group of typical office workers, where the workday consists of ego clashes, inappropriate behavior, and tedium.")
    db.session.add(s4)
    db.session.commit()

    p1 = Producer(id=1, firstname="Alex", lastname="Pina", age=datetime(1967,6,23))
    db.session.add(p1)
    db.session.commit()

    p2 = Producer(id=2, firstname="Zack", lastname="Estrin", age=datetime(1971,9,16))
    db.session.add(p2)
    db.session.commit()

    p3 = Producer(id=3, firstname="Jason", lastname="Rothenberg", age=datetime(1967,5,10))
    db.session.add(p3)
    db.session.commit()

    a1 = Actor(id=1, firstname="Alvaro", lastname="Morte", age=datetime(1975,2,23))
    db.session.add(a1)
    db.session.commit()

    a2 = Actor(id=2, firstname="Wentworth", lastname="Miller", age=datetime(1972,6,2))
    db.session.add(a2)
    db.session.commit()

    a3 = Actor(id=3, firstname="Eliza", lastname="Taylor", age=datetime(1989,10,24))
    db.session.add(a3)
    db.session.commit()

    a1s1 = ActorToShow(actor_id=a1.id, show_id=s1.id)
    db.session.add(a1s1)
    db.session.commit()

    a2s2 = ActorToShow(actor_id=a2.id, show_id=s2.id)
    db.session.add(a2s2)
    db.session.commit()

    a3s3 = ActorToShow(actor_id=a3.id, show_id=s3.id)
    db.session.add(a3s3)
    db.session.commit()

    p1s1 = ProducerToShow(producer_id=p1.id, show_id=s1.id)
    db.session.add(p1s1)
    db.session.commit()

    p2s2 = ProducerToShow(producer_id=p2.id, show_id=s2.id)
    db.session.add(p2s2)
    db.session.commit()

    p3s3 = ProducerToShow(producer_id=p3.id, show_id=s3.id)
    db.session.add(p3s3)
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

@app.route('/404')
def notFound():
    return render_template("404.html")

@app.route('/500')
def unexpectedError():
    return render_template("500.html")


