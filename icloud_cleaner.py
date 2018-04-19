import imaplib
from configobj import ConfigObj

def connect(config):
    mail = imaplib.IMAP4_SSL(config["imap_server"], config["imap_port"])
    mail.login(config["username"], config["password"])

config = ConfigObj("config.ini")
imap_conn = connect(config)