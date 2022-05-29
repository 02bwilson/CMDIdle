import os
import sys
import json
import easygui


class upgrades():
    def __init__(self):
        try:
            self.upgrades = json.loads("json_data/upgrades.json")
        except:
            easygui.msgbox("Error loading upgrades.")