from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import EqualTo, Length, NumberRange, DataRequired, Email, ValidationError

from app.models.user import User
from app.models.wxInfo import wxInfo


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64, message='Email length must longer than 8 and shorter than 64 characters'),
                                    Email(message='Not a valid email')])

    password = PasswordField(validators=[
        DataRequired(), Length(6, 32, message='Password must has at least 6 characters and no longer than 32 characters'),
        EqualTo('password2', message='Passwords must match')])

    password2 = PasswordField('repeat password')

    nickname = StringField(validators=[
        DataRequired(), Length(2, 10, message='nickname length must longer than 2 and shorter than 10 characters')])



    def validate_email(self, field):
        # db.session.
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64, message='Email length must longer than 8 and shorter than 64 characters'),
                                    Email(message='Not a valid email')])

    password = PasswordField(validators=[
        DataRequired(), Length(6, 32, message='Password must has at least 6 characters and no longer than 32 characters')])

class wxRegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64, message='Email length must longer than 8 and shorter than 64 characters'),
                                    Email(message='Not a valid email')])

    password = PasswordField(validators=[
        DataRequired(), Length(6, 32, message='Password must has at least 6 characters and no longer than 32 characters')])

    nickname = StringField(validators=[
        DataRequired(), Length(2, 10, message='nickname length must longer than 2 and shorter than 10 characters')])

    key = StringField()

    avatar = StringField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')







class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32, message='密码长度至少需要在6到32个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField(validators=[
        DataRequired(), Length(6, 32)])


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired()])
    new_password1 = PasswordField(validators=[
        DataRequired(), Length(6, 32, message='密码长度至少需要在6到32个字符之间'),
        EqualTo('new_password2', message='两次输入的密码不一致')])
    new_password2 = PasswordField(validators=[DataRequired()])