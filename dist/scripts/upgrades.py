import json
import easygui


class upgrades():
    def __init__(self):
        try:
            f = open("json_data/upgrades.json")
            self.upgrades = json.load(f)
        except Exception as e:
            easygui.msgbox("Error loading upgrades. %s" % e)
        
        
    def fetchUserUpgrades(self, user_obj, update_string):
        for i in range(0, len(self.upgrades - 1)):
            iter = str(i) + ","
            if iter in update_string():
                self.loadUpgrade(i, user_obj)
    
    def loadUpgrade(self, id, user_obj):
        for item in self.upgrades:
            if item['id'] == id:
                if item['effect'] == 'mps':
                    user_obj.mps += int(item['effect_magnitude'])
                elif item['effect'] == 'mult':
                    user_obj.mult += item['effect_magnitude']
                break

    
    def checkPrereq(self, id, user_obj, update_string):
        return
    
            
        
        

if __name__ == "__main__":
    upgrades()