from sqlalchemy import Table, Column
class Occupation(object):
    def __init__(self,masterid,slaveid, time):
        self.masterid=masterid
        self.slaveid=slaveid
	self.time = time
