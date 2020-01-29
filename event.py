# Event Class
# This file holds the data necessary for the Events Object used to hold data on classes as we make them
import json
import config
from tinydb import TinyDB, Query

database = TinyDB(config.database)


class Event:
    module = ""
    classtype = ""
    date = ""
    starttime = ""
    endtime = ""
    location = ""
    staff = ""
    id = ""
    colourID = ""

    def __init__(self, module, classtype, location, staff, colourID):
        self.colourID = colourID
        self.staff = staff
        self.location = location
        self.classtype = classtype
        self.module = module
        self.endtime = ""
        self.starttime = ""
        self.date = ""

    # Adds the date to the object using week and day data
    def addDate(self, week, day, starttime, endtime):
        # following if statements make it into 24h time
        if len(starttime) < 5:
            starttime = '0' + starttime
        if len(endtime) < 5:
            endtime = '0' + endtime

        self.endtime = endtime
        self.starttime = starttime
        with open(config.WeekDateJSON, "r") as read_file:
            data = json.load(read_file)
            week = data['weeks'][week - 1]
            self.date = week[str(day)]

    # Displays fields
    def DisplayEvent(self):
        print('=======================')
        print('Module: ' + self.module)
        print('ClassType: ' + self.classtype)
        print('Staff: ' + self.staff)
        print('Location: ' + self.location)
        print('Date: ' + self.date)
        print('Time: ' + self.starttime + ' - ' + self.endtime)

    # Adds itself to database
    def addToDatabase(self):
        if self.date is not None:
            # ID generation
            id = (self.module + self.date + self.starttime + self.module + config.idAddition)
            for char in id:
                self.id = self.id + str(ord(char))
            item = Query()
            if database.search(item.UUID == self.id):
                print('Duplicate found, that is:')
                print('{} {} at {} {}-{}'.format(self.module, self.location, self.date, self.starttime, self.endtime))
                exit(1)
            else:
                database.insert({'UUID': self.id, 'Module': self.module, 'ClassType': self.classtype,
                                 'Staff': self.staff, 'Location': self.location, 'Date': self.date,
                                 'start': self.starttime, 'end': self.endtime, 'colourID': self.colourID,
                                 'updated': True, 'Checked': True, 'added': False})
                print('Added event of:')
                self.DisplayEvent()
        else:
            print('Error: Object field not filled before adding to DB')

    # Updates database entry of itself
    def checkAndUpdate(self):
        if self.date is not None:
            # We generate a UUID for the event so we can update it
            id = (self.module + self.date + self.starttime + self.module + config.idAddition)
            for char in id:
                self.id = self.id + str(ord(char))
            item = Query()
            if database.search(item.UUID == self.id):
                result = database.get(item.UUID == self.id)
                if result['ClassType'] != self.classtype:
                    database.update({'ClassType': self.classtype, 'updated': True}, item.UUID == self.id)
                    print('Updated event of:')
                    self.DisplayEvent()

                if result['Location'] != self.location:
                    database.update({'Location': self.location, 'updated': True}, item.UUID == self.id)
                    print('Updated event of:')
                    self.DisplayEvent()
                database.update({'Checked': True}, item.UUID == self.id)
            else:
                self.addToDatabase()
