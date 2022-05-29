# Game By Bryce W

import os
import easygui

def main():
    try:
        os.system("start py controller.py")
    except:
        try:
            os.system("start python controller.py")
        except:
            easygui.msgbox("Failed to find python installation!") 

    
if __name__ == "__main__":
    main()