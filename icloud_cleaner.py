import re
import email
import imaplib
import email.header

from configobj import ConfigObj

def connect(config):
    email_connection = imaplib.IMAP4_SSL(config["imap_server"], config["imap_port"])
    email_connection.login(config["username"], config["password"])
    email_connection.select("inbox")

    return email_connection

def search_emails(email_connection, sender):
    typ, data = email_connection.search(None, '(FROM "' + sender + '")')
    
    # Split the email identifiers in an array
    mail_ids = data[0]
    return mail_ids.split()

# Add the deleted flag to an email
def set_deleted(email_connection, email_id):
    email_connection.store(email_id, '+FLAGS', '\\Deleted')

def fetch_uid(email_connection, email_id):
    status, uid_string = email_connection.fetch(email_id, 'UID')
    return re.search(r'\((.*?)\)', uid_string[0]).group(1).replace("UID ", "")

config = ConfigObj("config.ini")
email_connection = connect(config)

emails = search_emails(email_connection, "example@gmail.com")
print("Fetched " + str(len(emails)) + " emails for " + "address")

for e in emails:
    uid = fetch_uid(email_connection, e)
    # set_deleted(email_connection, e)

# Confirm the deletion of the messages
# email_connection.expunge()