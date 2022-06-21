# By Bryce W

# Python Imports
import os, sys
import yaml
import time
import threading
import shutil
import json


# Local Imports
import command_handler
import user

# External Imports
import easygui
from termcolor import colored


class game():
    
    def __init__(self):
        
        # Set window title
        self.set_window_title("CMDIdle")
       
        # Create vars
        self.user = user.user()
        self.user_data = dict()
        self.command_list = list()
        self.command_list.append(["help", "Helpful information for each command."])
        self.commandHandler = command_handler.command_handler(self.user)
        # Init the game 
        self.init_game()

        
        # Determine if user account saved
        if (self.user_data['user']['email'] not in {'', None,}) and (self.user_data['user']['password_hash'] not in {'', None}):
            try:
                print(self.user_data['user']['email'], self.user_data['user']['password_hash'])
                self.commandHandler.validatePassword(self.user_data['user']['email'], self.user_data['user']['password_hash'], config_flag=True)
                self.await_command()
            except Exception as e:
                print("There was a problem with your stored user info, please re-login.", e)
                self.execute_command("login")
            self.command_list.append(["mps", "Prints your current money per second"],
                                     ["ccolor", "Changes the color of your input cursor"])
            
            # Begin ticking
            self.tick_count = 0
            self.begin_ticking()
            
        else: 
            self.command_list.append(["login", "Login to your account."])
            self.command_list.append(["register", "Register for a new account."])
            self.present_welcome()
            # Begin ticking
            self.tick_count = 0
            self.begin_ticking()
    
    def init_game(self):
        # Load user config
        try:
            with open("user.yml") as user:
                try:
                    self.user_data = yaml.safe_load(user)
                except:
                    # If user.yml not found, create it
                    easygui.msgbox("User config error, user.yml has been rewritten")
                    f = open("user.yml", "w")
                    f.write('user:\n  email: \n  password_hash: ')
                    f.close()
                    self.present_welcome()
        except:
            # If user.yml not found, create it
            easygui.msgbox("FATAL ERROR LOADING USER DATA, A NEW USER FILE HAS BEEN CREATED")
            f = open("user.yml", "w")
            f.write('user:\n  email: \n  password_hash: ')
            f.close()
            self.present_welcome()
            
                
    def present_welcome(self):
        print(colored("===========================================================================================","red").center(shutil.get_terminal_size().columns))
        print(colored(" /$$      /$$ /$$$$$$$$ /$$        /$$$$$$   /$$$$$$  /$$      /$$ /$$$$$$$$","cyan").center(shutil.get_terminal_size().columns))
        print(colored("| $$  /$ | $$| $$_____/| $$       /$$__  $$ /$$__  $$| $$$    /$$$| $$_____/","cyan").center(shutil.get_terminal_size().columns))
        print(colored("| $$ /$$$| $$| $$      | $$      | $$  \__/| $$  \ $$| $$$$  /$$$$| $$      ","cyan").center(shutil.get_terminal_size().columns))
        print(colored("| $$/$$ $$ $$| $$$$$   | $$      | $$      | $$  | $$| $$ $$/$$ $$| $$$$$   ","cyan").center(shutil.get_terminal_size().columns))
        print(colored("| $$$$_  $$$$| $$__/   | $$      | $$      | $$  | $$| $$  $$$| $$| $$__/   ","cyan").center(shutil.get_terminal_size().columns))
        print(colored("| $$$/ \  $$$| $$      | $$      | $$    $$| $$  | $$| $$\  $ | $$| $$      ","cyan").center(shutil.get_terminal_size().columns))
        print(colored("| $$/   \  $$| $$$$$$$$| $$$$$$$$|  $$$$$$/|  $$$$$$/| $$ \/  | $$| $$$$$$$$","cyan").center(shutil.get_terminal_size().columns))
        print(colored("|__/     \__/|________/|________/ \______/  \______/ |__/     |__/|________/\n","cyan").center(shutil.get_terminal_size().columns))    
        self.printUpdateNotes() 
        print("\n")                                                                                                                        
        print(colored("===========================================================================================","red").center(shutil.get_terminal_size().columns))
        self.await_command()
        
    def await_command(self, flush_buffer_flag=False, color="red"):
        # Flush buffer if requested
        if flush_buffer_flag is True:
            sys.stdout.flush()

        next_command = input(colored("> ", color))
        for cmd in self.command_list:
            if next_command == cmd[0]:
                self.execute_command(next_command)
                break
        else:
            print("Invalid command, type help for a list of commands.")
            self.await_command()
        
    def execute_command(self, next_command):
        self.commandHandler.command_handler(next_command, self.command_list)
        self.await_command(flush_buffer_flag=True)
    
    def tick(self, mps):
        time.sleep(1)
        self.tick_count += 1
        self.set_window_title("CMDIdle", self.user.getBal(), self.user.getMps())
        self.bal += int((mps * (1.0 + self.mult)))
        print(self.tick_count)
        self.tick(self.mps)
    
    def begin_ticking(self):
        # Begin ticking
        ticking_thread = threading.Thread(target=self.tick, args=(self.mps, ))
        ticking_thread.daemon = True
        ticking_thread.start()
        
    def set_window_title(self, new_title, bal=0, mps=1):
        title = new_title
        if bal:
            title += " - ${}".format(str(bal))
        if mps:
            title += " - ${}/s"
        os.system('title %s' % (str(new_title)))
        
    def printUpdateNotes(self):
        try:
            json_file = open("json_data/latest.json")
            data = json.load(json_file)
            update_data = list()
            print(colored("+======================================================+\n","white").center(shutil.get_terminal_size().columns))
            for item in data:
                print(colored("\t" + item + "\t-\t" + data[item] + "\n", "green").center(shutil.get_terminal_size().columns).expandtabs(3))
            print(colored("+======================================================+","white").center(shutil.get_terminal_size().columns))
        except:
            easygui.msgbox("Couldnt find update notes.")
        
    
if __name__ == "__main__":
    main = game()
    
