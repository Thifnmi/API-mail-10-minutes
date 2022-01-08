import smtpd
import asyncore
from app.smtp_server.mail_receive import save
from threading import Thread


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data,
                        mail_options=None, rcpt_options=None):
        save(data=data, rcpttos=rcpttos, mailfrom=mailfrom)


# if __name__ == '__main__':
#     smtp = CustomSMTPServer(('0.0.0.0', 1025), None)
#     print(smtp)
#     kwargs = {'timeout': 1, 'use_poll': True}
#     t = Thread(target=asyncore.loop, kwargs=kwargs)
#     t.start()


CustomSMTPServer(('0.0.0.0', 1025), None)
kwargs = {'timeout': 1, 'use_poll': True}
t = Thread(target=asyncore.loop, kwargs=kwargs)
t.start()
