import imaplib
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


config = ConfigObj("config.ini")
email_connection = connect(config)
search_emails(email_connection, "example@gmail.com")