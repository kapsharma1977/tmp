from flask import render_template , render_template_string, Blueprint, session
#from . import mongo

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template("index.html")
    # String-based templates
    # return render_template_string("""
    #     {% extends "flask_user_layout.html" %}
    #     {% block content %}
    #         <h2>Home page</h2>
    #         <p><a href={{ url_for('user.register') }}>Register</a></p>
    #         <p><a href={{ url_for('user.login') }}>Sign in</a></p>
    #         <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
    #         <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
    #         <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
    #     {% endblock %}
    #     """)
    # if 'email' is session:
    #     # Check role faculty or student
    #     return render_template("index.html")
    # else:
    #     return render_template("index.html")


@main.route('/profile')
def profile():
    return 'Profile'

