# Import Form and RecaptchaField (optional)
from flask_wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, RadioField # BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired

# Import Form validators
from wtforms.validators import Required, Email, EqualTo

from app import images


class AddUserForm(Form):
    name = TextField(
        "名前",
        [
            Required(message="名前は必須だよ〜ん")
        ]
    )
    sex = RadioField(
        'man',
        [
            Required(message="性別は必須だよ〜ん")
        ],
        choices=[('man', '男'), ('woman', '女')],

    )
    email = TextField(
        'メールアドレス',
        [
            Email(),
            Required(message='メアドは必須だよ〜ん')
        ]
    )
    password = PasswordField(
        'パスワード', [
            Required(message='パスワードは必須だよ〜ん')
        ]
    )
    user_image = FileField('', validators=[FileRequired(), FileAllowed(images, '画像を選択して！')])
