"""
    Flaskr
    ~~~~~~

    A simple todoapp adapted from code written by Armin Ronacher (github.com/silshack/flaskr)

    :copyright: (c) 2018 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import sys


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


@app.route('/show_entries')
def show_entries():
    if session['logged_in'] == True:
        db = get_db()
        cur = db.execute('select text, status, user_username from items')
        entries = cur.fetchall()
        for row in entries:
            print('Row found: %s, %s, %s' % (row[0], row[1], row[2]), file=sys.stderr)
        return render_template('show_entries.html', entries=entries)
    else:
        return redirect(url_for('register'), error="You did not log in. Register?")


@app.route('/add', methods=['POST'])
def add():
    db = get_db()
    if db.execute("select * from items where user_username = '%s'" % (request.form['username'])):
        db.execute('insert into items (text, user_username, status) values (?, ?, ?)',
                 [request.form['text'], request.form['username'], True if request.form['status'] == "on" else False])
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))
    else:
        return redirect(url_for('show_entries'), error="Save data was invalid.")


@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    if request.method == 'POST':
        if request.form['username'] != "":
            print("\n")
            db.execute('insert into user (username) values (?)', (request.form['username'],))
            db.commit()
    cur = db.execute('select * from user')
    usernames = cur.fetchall()
    for row in usernames:
        print('Username found: %s' % row[0], file=sys.stderr)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        cur = db.execute('select * from user')

        usernames = cur.fetchall()
        for rows in usernames:
            if rows[0] == request.form['username']:
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash('You were logged in')
            return redirect(url_for('show_entries'))
        
        error = "User has not been registered"
        return render_template('register.html', error=error)
    return render_template('login.html', error=error)

@app.route('/delete', methods=['DELETE'])
def delete_entry():
    error = None
    db = get_db()
    cur = db.execute("DELETE * from items where user_username = %s AND text = %s" % (request.form("h2_username"), request.form("h2_text")))
    db.commit
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
