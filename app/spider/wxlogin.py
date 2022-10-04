from app.libs.httper import HTTP
from flask import current_app
from app.models.user import User
from app.models.base import db
from app.models.wxInfo import wxInfo


class WXLogin:
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'

    def __init__(self, code='', signature='', openid=''):
        self.code = code
        self.appid = current_app.config['APPID']
        self.secret = current_app.config['APPSECRET']
        self.openid = openid
        self.session_key = ''
        self.signature = signature

    def get_openid(self):
        return self.openid

    def request_openid(self):
        if(self.code == ''):
            print('bad request')
        else:
            url = self.url.format(self.appid, self.secret, self.code)
            result = HTTP.get(url)
            # print(result)
            self.fill_requested_data(result)

    def fill_requested_data(self, data):
        if data['session_key']:
            self.session_key = data['session_key']
        else:
            print('no session key')
        if data['openid']:
            self.openid = data['openid']
            print(data['openid'])
        else:
            print('no openid')

    def retrive_user(self):
        if self.openid != '':
            wxinfo = wxInfo.query.filter_by(openid = self.openid).first()
            # user = User.query.filter_by(wx_open_id = self.openid).first()
            #测试，增加we_openid
            # stmt = db.update(User).where(User.email == "test1@qq.com").values(wx_open_id = '').execution_options(synchronize_session="fetch")
            # result = db.session.execute(stmt)
            # db.session.commit()

        return wxinfo

    def check_partner(self):
        user = User.query.filter_by(openid= self.openid).first()
        if(user):
            print(user['partner_id'])
        else:
            print("not found")