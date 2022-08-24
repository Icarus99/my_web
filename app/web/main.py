from . import web
from flask import render_template



@web.route('/')
def main_page():
    return render_template('home.html')