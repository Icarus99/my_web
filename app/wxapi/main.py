from . import wxapi
from flask import render_template, request
from flask_login import login_required
from app.spider.wxlogin import WXLogin
from app.forms.auth import wxRegisterForm
from app.models.wxInfo import wxInfo
from app.models.user import User
from app.models.base import db
from app.models.partnerRequests import partnerRequests
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

    r = "logged in"

    if status is None:
        r = "need signup"

    crypto = Crypto()
    return {"status": r, "encrypted_id": crypto.encrypt(wx_login.get_openid())}

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
        key = form.data['key']
        crypto = Crypto()
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

        return "logged in"
    else:
        return "bad request"

@wxapi.route('/wxfetchprofile', methods=['GET','POST'])
def wx_fetch_profile():
    data = request.json
    crypto = Crypto()
    openid = crypto.decrypt(data["encrypted_id"])
    print("openid: "+openid)
    user = User()
    user = user.query.filter_by(wx_open_id=openid).first()

    if(user.partner_id == None):
        #检查partnerRequests表单
        partnerRequest = partnerRequests()
        requests = partnerRequest.query.filter_by(partner=user.id).all()
        re_requests={}
        index = 0
        for i in requests:
            re_requests[index]={"id": i.id, "adder": i.adder, "created_time": i.created_time.strftime("%Y-%m-%d %H:%M:%S")}
            index += 1
        return re_requests
    else:
        partner = User()
        partner = partner.query.filter_by(id=user.partner_id).first()
        return {"avatarUrl": partner.avatar, "nickname": partner.nickname}


@wxapi.route('/wxgetpartner', methods=['GET','POST'])
def wx_get_partner():
    data = request.json
    user = User()
    user = user.query.filter_by(nickname=data['nickname']).first()
    if(user):
        return {'nickname': user.nickname, 'avatarUrl': user.avatar}
    else:
        return "not found"

@wxapi.route('/wxaddpartner', methods=['GET', 'POST'])
def wx_add_partner():
    data = request.json
    user = User()
    crypto = Crypto()
    openid = crypto.decrypt(data["encrypted_id"])
    user = user.query.filter_by(wx_open_id=openid).first()
    partner = user.query.filter_by(nickname=data['nickname']).first()

    #如果搜索的对象已有对象，返回
    if(partner.partner_id != None):
        return "already added"

    partnerRequest = partnerRequests()
    partnerRequest.adder = user.id
    partnerRequest.partner = partner.id
    partnerRequest.created_time = datetime.datetime.now()
    db.session.add(partnerRequest)
    db.session.commit()

    return 'good'

@wxapi.route('/wxprocesspartner', methods=['GET', 'POST'])
def wx_process_partner():
    data = request.json

    partnerRequest = partnerRequests()
    requests = partnerRequest.query.filter_by(id=data["id"]).first()

    if data["status"] == "approved":
        user1 = User()
        user2 = User()
        user1 = user1.query.filter_by(id=requests.adder).first()
        user2 = user2.query.filter_by(id=requests.partner).first()
        user1.partner_id = user2.id
        user2.partner_id = user1.id

    db.session.delete(requests)
    db.session.commit()
    return 'good'