# iCloud email cleaning tool

A simple tool to batch delete all incoming emails from a sender. Especially useful if you subscribe to a bunch of newsletters and don't bother to delete the emails day by day

### Requirements

- python 2.7
- email_validator package (you can install it with `pip install email_validator`)
- an iCloud account with two-factor authentication enabled

### Usage

To use the tool you have to create a configuration file named `config.ini`. You can use the provided `config.example.ini` file as a template in which you have to replace `your_icloud_username` with your iCloud email without the `@icloud.com` part. If for some reasons the tool throws an `AUTHENTICATIONFAILED` error try to replace this variable with the full email address as stated [here](https://support.apple.com/en-us/HT202304). You also have to replace `your_app_specific_passsord` with an app specific password generated in your [Apple ID setting page](https://www.google.com) under the app specific password subsection.

After you finished setting up the configuration file in order to use the tool you just have to run `python icloud_cleaner.py target_email_address` in the script directory