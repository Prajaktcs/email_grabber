import imaplib
import email

from elasticsearch import Elasticsearch

import constants
from models import EmailMsg


def get_email_and_save(es_client: Elasticsearch, username: str, password: str) -> None:
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        M.login(username, password)
        M.select(mailbox='spark')
        _, data = M.search(None, 'ALL')
        print(data[0])
        for num in data[0].split():
            typ, data = M.fetch(num, '(RFC822)')
            # print('Message %s\n%s\n' % (num, data[0][1]))
            msg = email.message_from_bytes(data[0][1])
            if 'unsubscribe' != msg['Subject']:
                email_msg = EmailMsg()
                email_msg.from_user = msg['From']
                email_msg.to_user = msg['To']
                email_msg.cc_user = msg['CC']
                email_msg.received_date = msg['Date']
                for m in msg.walk():
                    if m.get_content_type() == 'text/plain':
                        email_msg.body = str(m)
                        break
                email_msg.save(using=es_client)
            M.store(num, '+X-GM-LABELS', '\\Trash')
        print('deleting messages')
        M.close()
        M.logout()
    except imaplib.IMAP4.error as e:
        print("LOGIN FAILED!!! " + str(e))


if __name__ == '__main__':
    es_client = Elasticsearch()
    get_email_and_save(es_client, constants.username, constants.password)
