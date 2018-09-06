# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='./flaskr.db',
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    if session['logged_in'] == True:
        db = get_db()
        cur = db.execute('select key, text, status, user_username from items')
        entries = cur.fetchall()
        return render_template('show_entries.html', entries=entries)
    else:
        return redirect(url_for('register'))


@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    if request.method == 'POST':
        if request.form['username'] != "":
            print("\n")
            db.execute('insert into user (username) values (?)', (request.form['username'],))
            cur = db.execute('select * from user')
            usernames = cur.fetchall()
            print(usernames)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        cur = db.execute('select * from user')
#, (request.form['username'],))
        usernames = cur.fetchall()
        print(usernames)
        if len(usernames) > 0:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        else:
            error = "User has not been registered"
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run()
