from flask_mail import Message
from application import mail


def Send_Mail(subject , recipients,body):
        msg = Message(subject ,recipients , body)
        mail.send(msg)