from sqlalchemy import Table, Column
class Battle(object):
    def __init__(self,uid,enemy_id,left_time,timeneed,power,powerin,powerca,allypower, catapult):
        self.uid=uid
        self.enemy_id=enemy_id
        self.left_time=left_time
        self.timeneed=timeneed
        self.powerin=powerin
        self.powerca=powerca
        self.power=power
        self.allypower=allypower
        self.catapult = catapult
        
