import re
import sys
import email
import imaplib
import os.path
import email.header
import argparse
from configobj import ConfigObj

def connect(config):
    email_connection = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'])
    email_connection.login(config['username'], config['password'])
    email_connection.select('inbox')

    print('Successfully connected to ' + config['username'] + '@icloud.com inbox')

    return email_connection

def search_emails(email_connection, sender):
    typ, data = email_connection.search(None, '(FROM "' + sender + '")')
    
    # Split the email identifiers in an array
    mail_ids = data[0]
    return mail_ids.split()

# Add the deleted flag to an email
def set_deleted(email_connection, email_uid):
    email_connection.uid("STORE", int(email_uid), "+FLAGS", "(\\Deleted)")

def fetch_uid(email_connection, email_id):
    status, uid_string = email_connection.fetch(email_id, 'UID')
    uid_res = re.search(r'\((.*?)\)', uid_string[0])

    if (uid_res != None):
        return uid_res.group(1).replace('UID', '')
    else:
        return None

def parse_args():
    parser = argparse.ArgumentParser(description='Delete all incoming emails from a sender email address')
    parser.add_argument('--email', help='The sender whose messages should be deleted')
    parser.add_argument('--file', help='A file which contains the target emails. Each email should be on a separate line.')

    return parser.parse_args()

def validate_input_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def verify_cli_args(args):
    if args.email == None and args.file == None:
        print('You need to specify a target email or a file. Use --help for details')
        sys.exit()

def import_emails_from_file(filename):
    if os.path.isfile(filename):
        return open(filename).read().split('\n')
    else:
        print('The file ' + filename + ' doesn\'t exist')

args = parse_args()
verify_cli_args(args)
target_emails = []

if args.email == None:
    target_emails = import_emails_from_file(args.file)
else:
    target_emails = [args.email]

config = ConfigObj('config.ini')

print('Connecting to ' + config['username'] + '@icloud.com...')
email_connection = connect(config)

total_emails_count = 0
for target_idx, target_email in enumerate(target_emails):
    if not validate_input_email(target_email):
        print('The email \'' + target_email + '\' is not valid')
        continue

    emails = search_emails(email_connection, target_email)
    emails_count = str(len(emails))
    total_emails_for_target = int(emails_count)
    total_deleted_emails = 0

    while int(emails_count) > 0:
        print('Found ' + emails_count + ' email(s) for ' + target_email)

        for idx, e in enumerate(emails):
            # The fetching of the email UID is required
            # since the email ID may change between operations
            # as specified by the IMAP standard
            uid = fetch_uid(email_connection, e)
            if (uid != None):
                print('Deleted email ' + str(total_deleted_emails + idx + 1) + '/' + str(total_emails_for_target))
                set_deleted(email_connection, uid)
            else:
                print('Email ' + str(total_deleted_emails + idx + 1) + '/' + str(total_emails_for_target) + ' was not valid')

        # Confirm the deletion of the messages
        email_connection.expunge()

        print('Deleted ' + emails_count + ' email(s) for ' + target_email)
        print('Checking for remaining emails...')

        # Verify if there are any emails left on the server for 
        # the target address. This is required to circumvent the
        # chunking of the search results by iCloud
        emails = search_emails(email_connection, target_email)
        emails_count = str(len(emails))
        total_deleted_emails = total_emails_for_target
        total_emails_for_target += int(emails_count)

    print('The cleanup for ' + target_email + ' was successful. Deleted ' + str(total_emails_for_target) + ' email(s)')
    total_emails_count += total_emails_for_target

print('The cleanup was successful. Deleted ' + str(total_emails_count) + ' email(s)')

# Close the mailbox and logout
email_connection.close()
email_connection.logout()