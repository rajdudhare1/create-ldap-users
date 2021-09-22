import ldap3
from ldap3 import HASHED_SALTED_SHA, MODIFY_REPLACE, ALL
from ldap3.utils.hashed import hashed
import string
import random


class User():
    def __init__(self, fname, lname, email,title='Mrs',org = 'ORG',mobile_number=123456, connection=None):
        self.fname = fname.lower()
        self.lname = lname.lower()
        self.fname = fname.capitalize()
        self.lname = lname.capitalize()
        self.email = email
        self.mobile_number = mobile_number
        self.orgName = org
        self.title = title
        self.uid = self.lname.lower()+ self.fname.lower()[0]
        self.userdn = 'uid='+self.uid+','+self.search_base
        self.givenName = self.fname +' '+self.lname
        self.gid = None
        self.conn = connection.conn
        self.attributes = None
        self.password = None
        self.search_filter = connection.search_filter
        self.search_attrs= connection.search_attrs
        self.search_base = connection.search_base
        
    def __check_if_user_already_exists(self):
        temporary_conn = self.conn
        temporary_conn.search(self.search_base, search_filter='(uid='+self.uid+')', attributes=self.search_attrs)
        if len(temporary_conn.entries) != 0 and temporary_conn.entries[0]['cn'] == self.givenName:
            return True
        elif len(temporary_conn.entries) != 0:
            if temporary_conn.entries[0]['cn'] != self.givenName and temporary_conn.entries[0]['uid'] == self.uid:
                self.uid = self.lname.lower()+ self.fname.lower()[0] + self.fname.lower()[1]
                self.userdn = 'uid='+self.uid+','+self.search_base
                return False
        else:
            return False

    def __getNextAvailableGid(self):
        if self.conn is not None:
            gids = []
            self.conn.search(self.search_base, self.search_filter, attributes=self.search_attrs)
            users = self.conn.entries
            for user in users:
                gids.append(int(str(user.gidNumber)))
            gids.sort()
            self.gid = gids[-1] + 1
        else:
            print("Please create connection first!")

    def __password_generator(self,length=8):
        LETTERS = string.ascii_letters
        NUMBERS = string.digits

        printable = f'{LETTERS}{NUMBERS}'
        printable = list(printable)
        random.shuffle(printable)

        random_password = random.choices(printable, k=length)
        self.password = ''.join(random_password)
        
    def modify_user_password(self):
        if self.password is not None:
            hashed_password = hashed(HASHED_SALTED_SHA, self.password)
            changes = {
                'userPassword': [(MODIFY_REPLACE, [hashed_password])]
            }
            success = self.conn.modify(self.userdn, changes=changes)
            if not success:
                print('Unable to change password for %s' % self.uid)
                print(self.conn.result)
                raise ValueError('Unable to change password')

    def __generate_user_config(self):
        self.attributes={'objectClass':  ['inetOrgPerson','posixAccount', 'shadowAccount', 'top'], 
            'sn': self.lname, 'gidNumber': self.gid,'cn': self.givenName,'mail':self.email,'shadowLastChange':0, 'shadowMax':99999, 'shadowMin':0, 'shadowWarning':14,
            'title': self.title,'homeDirectory' : '/home/'+self.uid, 'uid' : self.uid, 'uidNumber': self.gid,'gecos': self.givenName, 'mobile': self.mobile_number, 'o':self.orgName}

    def create_user(self):
        if self.conn is not None:
            if self.__check_if_user_already_exists():
                print("User Already Exist")
                return False
            else:
                self.__password_generator()
                self.__getNextAvailableGid()
                self.__generate_user_config()
                self.conn.add(self.userdn,attributes=self.attributes)
                self.modify_user_password()
                return self.password
        else:
            print("Please create connection first!")
            
class LDAPConnection():
    def __init__(self):
        self.conn = None
        self.search_base = None
        self.search_filter = None
        self.search_attrs= None

    def create_connection(self, servername,user, password,search_base,search_filter = '(objectClass=inetOrgPerson)',search_attrs=['*'],port="389"):
        server_uri = 'ldap://'+servername+':'+port
        server = ldap3.Server(server_uri, get_info=ALL)
        self.conn = ldap3.Connection(server, user, password, auto_bind=True)
        self.search_base = search_base
        self.search_filter = search_filter
        self.search_attrs= search_attrs

    def delete_connection(self):
        self.conn.unbind()
