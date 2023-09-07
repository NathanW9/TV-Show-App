from flask import render_template, flash, redirect, url_for
from app import app


@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html", title='Home')

@app.route('/show_list')
def show_list():
    list_shows = ["Money Heist", "The 100", "Prison Break", "Breaking Bad"]
    return render_template("show_list.html", title="Tv Show", show_list=list_shows)

@app.route('/money_heist')
def show_page():
    return render_template("money_heist.html", title="Money Heist")


@app.route('/new_show')
def new_show():
    return render_template("new_show.html", title="New Show")