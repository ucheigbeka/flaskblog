import os
import secrets
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from flaskblog import mail


def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    if current_user.image_file != 'default.jpg':
        original_picture_path = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)
        os.remove(original_picture_path)
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    form_pic.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='noreply@demo.com')
    msg.body = f'''To reset your password visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email.
    '''
    mail.send(msg)
