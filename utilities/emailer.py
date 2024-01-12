import threading

from django.core.mail import EmailMessage

from utilities.logger_util import Logger

LOG_EMAILS = True


class EmailThread(threading.Thread):
    def __init__(self, subj, msg, sender, recipients):
        self.subj = subj
        self.msg = msg
        self.sender = sender
        self.recipients = recipients
        threading.Thread.__init__(self)

    def run(self):
        email = EmailMessage(self.subj, self.msg, self.sender, self.recipients)
        email.send()
        if LOG_EMAILS:
            logger = Logger()
            logger.log("Sent Email", "System, using the email" + self.sender + ", sent email to " + str(self.recipients) + " with subject: " + self.subj + " and content: " + self.msg)


def send_email_asynch(subj, msg, sender, recipients):
    EmailThread(subj, msg, sender, recipients).start()
