import smtpd
import asyncore
import threading


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to:', rcpttos)
        print('Message length:', len(data))
        return


class SMTPServer():
    def __init__(self):
        self.port = 1025

    def start(self):
        self.smtp = CustomSMTPServer(('0.0.0.0', self.port), None)
        kwargs = {'timeout': 1, 'use_poll': True}
        self.thread = threading.Thread(target=asyncore.loop, kwargs=kwargs)
        self.thread.start()

    def stop(self):
        self.smtp.close()
        self.thread.is_alive = False

        # self.thread.join()

    def get(self):
        return self.smtp.emails
