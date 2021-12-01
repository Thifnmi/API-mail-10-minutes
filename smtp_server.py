import smtpd
import asyncore
from app.dashboard.controller import save


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data,
                        mail_options=None, rcpt_options=None):
        print(data)
        save(data=data, rcpttos=rcpttos, mailfrom=mailfrom)


if __name__ == '__main__':
    server = CustomSMTPServer(('0.0.0.0', 1025), None)
    asyncore.loop()
