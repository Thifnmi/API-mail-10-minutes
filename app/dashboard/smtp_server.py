import smtpd


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data,
                        mail_options=None, rcpt_options=None):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to:', rcpttos)
        print('Message length:', data.decode())

        from app import db
        from .database import MailBox, UserMail
        from sqlalchemy.exc import SQLAlchemyError

        for email in rcpttos:
            mail_id = UserMail.query.filter_by(email=email).first().id
            text = data.decode()
            content = None
            for i in range(0, len(text.split("\n"))):
                if text.split("\n")[i].startswith("Subject"):
                    title = text.split("\n")[i].split(": ")[1]
                if text.split("\n")[i].startswith("Content"):
                    content = text.split("\n")[i].split(": ")[1]
            if content is not None:
                text = content

            message = MailBox(mail_id=mail_id, email_from=mailfrom,
                              title=title, content=text)
            try:
                db.session.add(message)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
