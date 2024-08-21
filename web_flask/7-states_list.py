#!/usr/bin/python3
"""
A Flask web application that displays a list of states.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    """Close the current SQLAlchemy session."""
    storage.close()

@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display a HTML page with a list of states sorted by name."""
    states = storage.all(State)
    sorted_states = sorted(states.values(), key=lambda state: state.name)
    return render_template('states_list.html', states=sorted_states)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

