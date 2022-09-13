from flask import Blueprint

wxapi = Blueprint('wxapi',__name__)

from app.wxapi import main