#!/usr/bin/env python

#
# Send phishing emails by doing the following:
#  * Read a JSON file that defines a first name, email address,
#    template, and a unique identifier.
#  * Create an email message with the data read from the file.
#  * Send the email to the specified address.
# 
import json
import smtplib
import email.mime.text


MX = ''  # Hostname for target MX server.
PHISH_MX = ''  # Hostname for phishing server. 
PHISHFILE = 'targets.json'
CAMP1_ADDR = ''  # Source email address for campaign 1.
CAMP2_ADDR = ''  # Source email address for campaign 2.
CAMP1_SUBJ = ''  # Subject for campaign 1 email.
CAMP2_SUBJ = ''  # Subject for campaign 2 email.
CAMP1_URL = 'http://<phish_server>/owa/auth/logon.html?id={0}' 
CAMP2_URL = 'http://<phish_server>/awareness.html?id={0}'

CAMP1_TEMP = '''
<p>Hi {0},</p> 
<p>As part of our ongoing effort to protect client data and improve security,
we have recently upgraded the encryption of our email system. To ensure
your email is properly encrypted, please <a href="{1}">login</a>.</p> 
<p>Thank you for your patience as we work to improve security.</p> 
<p>Regards,</p>
<p>IT Department</p>

'''

CAMP2_TEMP = '''
<p>Hi {0},</p> 
<p>Due to a technical issue in the processing system, there was an error
processing your check. To ensure timely payment, please <a href="{1}">login</a>
 and remedy this error.</p>
<p>Thank you for your patience as we work to correct this issue.</p>
<p>Regards,</p>
<p>HR Department</p> 
'''


def send_message(mailfrom, rcptto, data):
    try:
        server = smtplib.SMTP(MX, 25, PHISH_MX)
        server.sendmail(mailfrom, rcptto, data)

    except smtplib.SMTPDataError as e:
        print '[-] {0}'.format(str(e[1]))

    except smtplib.SMTPServerDisconnected as e:
        print '[-] {0}'.format(str(e))

    except smtplib.SMTPConnectError as e:
        print '[-] {0}'.format(str(e[1]))


def read_phish_file(filename):
    with open(filename) as pf:
        return json.loads(pf.read())


def build_message(template, subj, url, first, vid):
    link = url.format(vid)
    html = template.format(first, link)
    msg = email.mime.text.MIMEText(html, 'html')
    msg['Subject'] = subj

    return msg


if __name__ == '__main__':
    phish = read_phish_file(PHISHFILE)
    for p in phish['targets']:
        if p['campaign'] == 'CAMP1':
            msg = build_message(CAMP1_TEMP, CAMP1_SUBJ, CAMP1_URL, p['first'], p['id'])
            msg['From'] = CAMP1_ADDR
            msg['To'] = p['email']
            print "Sending campaign 1 email to {0} with id {1}".format(p['email'], p['id'])
            send_message(CAMP1_ADDR, p['email'], msg.as_string())

        elif p['campaign'] == 'CAMP2':
            msg = build_message(CAMP2_TEMP, CAMP2_SUBJ, CAMP2_URL, p['first'], p['id'])
            msg['From'] = CAMP2_ADDR
            msg['To'] = p['email']
            print "Sending PR email to {0} with id {1}".format(p['email'], p['id'])
            send_message(CAMP2_ADDR, p['email'], msg.as_string())

        else:
            pass
