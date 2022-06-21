# Command handler By Bryce W

# External Imports
# TODO: Cleanup imports
import psycopg2
import bcrypt
from email_validator import validate_email
from pwinput import pwinput
import scripts.upgrades as upgrades
import time
from mail_handler import email_handler

class command_handler():
    def __init__(self, user_obj):
        self.user = user_obj
        self.upgrade_handler = upgrades.upgrades()
        self.connection = None
        self.pos = None

    def command_handler(self, cmd, cmd_list=[]):
        
        if cmd.lower() == 'help':
            for command in cmd_list:
                print(command[0] + "\t" + command[1])
                
                
                
        elif cmd.lower() == 'login':
            self.connect()
            try:
                user_email = input("Email: ")
                user_password = pwinput("Password: ")
                # Verify user creds
                self.verify_cred(user_email, user_password)
                # verify_email user data/see if user is truly already created
                self.verify_email(user_email)
                self.validatePassword(user_email, user_password)
                print("Logged in!")
            except:
                print("Error finding an account with these details (Username/Password incorrect).")
                
                
                
        elif cmd.lower() == 'register':

            self.connect()
            try:
                user_email = input("Email: ")
                user_password = pwinput("Password: ")
                # Verify user creds
                self.verify_cred(user_email, user_password)
                # See if user is already created
                created = self.verify_email(user_email)
                if created == True:
                    print("A user with this email already exists.")
                else: 
                    try:
                        self.create_account(user_email, user_password)
                        print("Account created!")
                        mailSender = email_handler()
                        mailSender.send_register_mail(user_email)
                    except:
                        print("Error creating account")
            except:
                print("A fatal error occured, please fix the problems listed.")
                
                
        elif cmd.lower() == 'upgrade':
            return
            
        else: 
            print("Oops! Something went wrong.")
            
    def connect(self):
        try:
            self.connection = psycopg2.connect(
            host="",
            port="",
            database="",
            user="",
            password="")
            self.pos = self.connection.cursor()
        except:
            print("Servers are currently down for maintenance.")
        
    def verify_cred(self, email, password):
        try:
            email = validate_email(email).email
            password = password.strip(" ")
            if len(password) >= 5:
                # Properly encode information
                email = email.encode('utf-8')
                password = password.encode('utf-8')
            else:
                print("Please enter a longer password. (Min 5 Characters)")
                password = input("Password: ")
                self.verify_cred(email, password)
        except:
            print("Please enter a valid email.")
            raise Exception

    def verify_email(self, email):
        self.pos = self.connection.cursor()
        query = "SELECT COUNT(*) FROM app.cmdidle_users_001 WHERE EMAIL=%s"
        self.pos.execute(query, (email, ))
        count = self.pos.verify_fetchone()
        for item in count:
            if str(count)[1] == '1':
                return True
            else: 
                return False
        self.pos.close()

    def create_account(self, email, password):
        self.pos = self.connection.cursor()
        password_salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), password_salt)
        insert = "INSERT INTO app.cmdidle_users_001 VALUES (%s, %s, %s, %s)"
        self.pos.execute(insert, (email, password_hash.decode('utf-8'), 0, "0, ", ))
        self.connection.commit()
        self.pos.close()
        # Write user config
        f = open("user.yml", "w")
        f.write("user:\n  email: {}\n  password_hash: {}".format(email, password_hash.decode('utf-8')))
        
    
    def loadUserData(self, email, password):
        data = list()
        self.pos = self.connection.cursor()
        query = "SELECT balance, upgrade_history FROM app.cmdidle_users_001 WHERE email=%s"
        self.pos.execute(query, (email, ))
        results = self.pos.verify_fetchone()
        for row in results:
            data.append(row)
        self.user.setBal(data[0])
        self.upgrade_handler.fetchUserUpgrades(self.user, data[1])
        self.pos.close()

    def validatePassword(self, email, password, config_flag=False):
        self.pos = self.connection.cursor()
        account_query = "SELECT password_hash FROM app.cmdidle_users_001 WHERE email=%s"
        self.pos.execute(account_query, (email, ))
        result = str(self.pos.verify_fetchone())[2:-3]
        if config_flag == True:
            self.connect()
            result = password
        if (bcrypt.checkpw(password.encode('utf-8'), result.encode('utf-8'))) == True:
            # self.loadUserData(email, password)
            self.pos.close()
        else:
            self.pos.close()
            raise Exception
        