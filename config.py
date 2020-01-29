import json
jsonFile = 'config/config.json'

# Following config are help in config/config.json
googleAPIKeyFile = ""
CalendarID = 'primary'
timetableURL = ""
modulesTaken = []
colourID = []
year = ""
WeekDateJSON = ''

database = 'config/classesDB.json'  # This is the database file that holds the user's classes
# Used mainly for dev, allows the generation of a new set of ids so it doesn't clash with previous ones on google Cal
idAddition = ""

# OPens JSON file and loads configs
with open(jsonFile, "r") as configFile:
    jsonData = json.load(configFile)
    googleAPIKeyFile = 'config/{}'.format(jsonData['googleAPIKeyFile'])
    CalendarID = jsonData['CalendarID']
    timetableURL = jsonData['timetableURL']
    year = jsonData['year']
    modulesTaken = jsonData['modulesTaken']
    colourID = jsonData['colourID']
    WeekDateJSON = 'config/weekData/{}.json'.format(year)
    loadedData = jsonData['loaded']


# Displays config
def displayConfig():
    print('Google Calendar API Key: ' + googleAPIKeyFile)
    print('Google Calendar ID: ' + CalendarID)
    print('Timetable URL: ' + timetableURL)
    print('Start Academic Year: ' + year)
    print('Modules Taken: ' + str(modulesTaken))
    print('Colour ID: ' + str(colourID))


# Updates JSON file
def updateConfigExternal(googleAPI, timetableURLInput, yearInput, modulesInput, colourInput):
    file = open(jsonFile, "r")
    data = json.load(file)
    data['googleAPIKeyFile'] = googleAPI
    data['CalendarID'] = 'primary'
    data['timetableURL'] = timetableURLInput
    data['year'] = yearInput
    data['modulesTaken'] = modulesInput
    data['colourID'] = colourInput
    jsonData['loaded'] = False


    file.close()

    with open(jsonFile, "w") as output:
        output.write(json.dumps(data))


# Updates Google Calendar ID
def updateCalID(calInput):
    file = open(jsonFile, "r")
    data = json.load(file)
    data['CalendarID'] = calInput
    file.close()

    with open(jsonFile, "w") as output:
        output.write(json.dumps(data))


# Updated loaded field
def updateLoaded():
    file = open(jsonFile, "r")
    data = json.load(file)
    data['loaded'] = True
    file.close()

    with open(jsonFile, "w") as output:
        output.write(json.dumps(data))
