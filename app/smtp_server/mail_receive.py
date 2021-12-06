from app.models import UserMail, MailBox
from app import db
from sqlalchemy.exc import SQLAlchemyError


def save(data, rcpttos, mailfrom):
    text = data.decode()
    try:
        text.split('swaks/\n\n')[1]
        for i in range(0, len(text.split("\n"))):
            if text.split("\n")[i].startswith("Subject"):
                title = text.split("\n")[i].split(": ")[1]
    except:
        title = text.split('/\n')[1].split('\n\n')[0]

    for email in rcpttos:
        mail_id = UserMail.query.filter_by(email=email).first().id
        content = text.split('\n\n')[1]

        message = MailBox(mail_id=mail_id, email_from=mailfrom,
                          title=title, content=content)
        try:
            db.session.add(message)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
