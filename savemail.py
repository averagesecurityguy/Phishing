#!/usr/bin/env python

import smtpd
import asyncore

MAILFILE = 'mailfile.txt'
SERVER = '127.0.0.1'
PORT = 25

def save_message(fr, to, msg):
    with open(MAILFILE, 'a') as mf:
        mf.write('FROM: {0}\nTO: {1}\nMSG:\n{2}\n\n'.format(fr, to, msg))


class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        print '[*] Saving message for {0}.'.format(rcpttos)
        
        try:
            save_message(mailfrom, rcpttos, data)
        except:
            pass

server = CustomSMTPServer((SERVER, PORT), None)
print '[+] Server listening on port {0}'.format(PORT)
asyncore.loop()