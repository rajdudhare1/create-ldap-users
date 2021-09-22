#!/usr/bin/python3

from utils.email import Email
from utils.data import Excel, CSV
from utils.ldap import User, LDAPConnection
import argparse
from os import environ

def run_create_user(user,smtpServer,smtpPort,smtpUser,smtpPassword,smtpSender):
    if u.create_user():
        print('Account Created For User - %s' %(user.givenName))
        e = Email(user,smtpServer,smtpPort,smtpUser,smtpPassword,smtpSender)
        e.send_email()
    
if __name__ == '__main__':
    if 'LDAP_HOST' not in environ:
        print("Kindly run the admin.cfg first! - set -a; source admin.cfg; set +a")
    else:
        ldapServer = environ['LDAP_HOST']
        ldapUser = environ['LDAP_USER']
        ldapPassword = environ['LDAP_PASSWORD']
        ldapSearchBase = environ['LDAP_SEARCH_BASE']
        smtpServer = environ['SMTP_HOST']
        smtpPort = environ['SMTP_PORT']
        smtpUser = environ['SMTP_USER']
        smtpPassword = environ['SMTP_PASSWORD']
        smtpSender = environ['SMTP_SENDER_EMAIL']
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--csv', help='provide csv file location',required=False)
        parser.add_argument('--xl', help ='provide xlxs file location',required=False)
        parser.add_argument('--firstname', help='provide first name',required=False)
        parser.add_argument('--lastname', help='provide last name',required=False)
        parser.add_argument('--email', help='provide email address',required=False)
        parser.add_argument('--title',help='provide title for user',required=False)
        parser.add_argument('--org',help='provide organisation name',required=False)
        parser.add_argument('--sheet', help ='provide xlxs file location',required=False)

        args = parser.parse_args()
        if args.csv != None:
            csv= CSV(args.csv)
            title, fnames, lnames, emails, org = csv.read_file()
            c = LDAPConnection()
            c.create_connection(ldapServer,ldapUser,ldapPassword,ldapSearchBase)
            for i in range(len(fnames)):
                u = User(fnames[i], lnames[i], emails[i], search_base=ldapSearchBase,title=title[i],org=org[i],connection=c)
                u.create_connection(ldapServer,ldapUser,ldapPassword,ldapSearchBase)
                run_create_user(u,smtpServer,smtpPort,smtpUser,smtpPassword,smtpSender)
            c.delete_connection()

        elif args.xl != None:
            xl= Excel(args.xl,args.sheet)
            title, fnames, lnames, emails, org = xl.read_file()
            c = LDAPConnection()
            c.create_connection(ldapServer,ldapUser,ldapPassword,ldapSearchBase)
            for i in range(len(fnames)):
                u = User(fnames[i], lnames[i], emails[i], search_base=ldapSearchBase,title=title[i],org=org[i],connection=c)
                u.create_connection(ldapServer,ldapUser,ldapPassword,ldapSearchBase)
                run_create_user(u,smtpServer,smtpPort,smtpUser,smtpPassword,smtpSender)
            c.delete_connection()

        elif args.firstname != None:
            c = LDAPConnection()
            c.create_connection(ldapServer,ldapUser,ldapPassword,ldapSearchBase)
            u = User(args.firstname, args.lastname, args.email,search_base=ldapSearchBase,title=args.title,org=args.org,connection=c)
            run_create_user(u,smtpServer,smtpPort,smtpUser,smtpPassword,smtpSender)
            c.delete_connection()
