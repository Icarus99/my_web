from . import web
from flask import render_template
from flask_login import login_required


@web.route('/')
def main_page():
    return render_template('page-maintenance.html')

@web.route('/home')
@login_required
def home():
    return render_template('home.html')

@web.route('/test')
@login_required
def test():
    return 'good morning'