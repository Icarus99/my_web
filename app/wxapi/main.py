from . import wxapi
from flask import render_template, request
from flask_login import login_required
from app.spider.wxlogin import WXLogin
from app.forms.auth import wxRegisterForm
from app.models.wxInfo import wxInfo
from app.models.user import User
from app.models.base import db
from app.libs.crypto import Crypto
import datetime


@wxapi.route('/wxlogin', methods=['GET','POST'])
def wx_login_check():
    data = request.json
    #初始化WXLogin
    wx_login = WXLogin(code=data['code'],signature=data['signature'])

    #通过appid和secret和code取openid
    wx_login.request_openid()
    #查找数据库中是否存在该openid的用户
    status = wx_login.retrive_user()

    if status is None:
        crypto = Crypto(data['code'])
        return crypto.encrypt(wx_login.get_openid())
    else:
        return "logged in"

@wxapi.route('/wxregister', methods=['GET','POST'])
def wx_register():
    form = wxRegisterForm(request.form)
    result = {"email": '', "nickname": '', "password": ''}
    info_extra = {}

    if not form.validate():
        if form.email.errors:
            result['email'] = form.email.errors[0]
        if form.nickname.errors:
            result['nickname'] = form.nickname.errors[0]
        if form.password.errors:
            result['password'] = form.password.errors[0]
        return result
    elif request.method == 'POST':
        code = form.data['code']
        key = form.data['key']
        crypto = Crypto(code)
        openid = crypto.decrypt(key)

        #创建用户表
        user = User()
        user.set_attrs(form.data)
        user.set_attrs({'wx_open_id': openid})
        db.session.add(user)
        db.session.commit()

        #创建登陆态表
        wxinfo = wxInfo()
        now = datetime.datetime.now()
        extra = {'openid': openid, 'member_id': 123, 'created_time': now, 'updated_time': now}
        wxinfo.set_attrs(extra)
        db.session.add(wxinfo)
        db.session.commit()

        return {'nickname': form.data['nickname']}
    else:
        return "bad request"

