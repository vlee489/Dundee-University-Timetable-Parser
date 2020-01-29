"""
Main python script to run program
(c) Vincent Lee
"""

import calender
import webParser
import config
import time
from os import system, name
import random

colours = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']


# function to clear screen
def ClearScreen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def setup():
    print("We're going to run through a setup wizard")
    print('Creating configs')
    time.sleep(3)
    ClearScreen()

    print('Please go onto https://evision.dundee.ac.uk/ then go to "View Your Personalised Timetable"')
    print('and Select the semester you want to import into Google Calendar.')
    print('We only suggest that you work with one semester at a time')
    print(' ')
    timetableURL = input('Then paste the URL/Website link you get into here: ')
    ClearScreen()

    print('What year did the Academic year being?')
    print('Example, if it\'s 2019-2020, enter 2019')
    year = input('Start of Academic Year: ')
    ClearScreen()

    print('What modules are you doing that are on the time table')
    print('This is the module code, such as AC22005')
    print('Enter the modules you are doing using a command "," to split each answer, and don\'t use spaces!!')
    print('Example: AC22005,AC22006,AC22007')
    modules = input('Modules: ')
    ClearScreen()

    print('Now we need to get a Google Calendar API key')
    print('Go to https://developers.google.com/calendar/quickstart/python and click on "Enable the Google Calendar API')
    print('Then click on "DOWNLOAD CLIENT CONFIGURATION" and save the downloaded file to the config folder')
    print('')
    print('Now tell me the name of the file your placed into the config folder, this is usually called credentials.json')
    print('I need the file ending as well e.g: json')
    googleAPI = input('credentials file name: ')
    ClearScreen()

    # Splits the modules up and places in list as well as assinging a colour to each module
    modules = modules.split(',')
    modulesList = []
    colourList = []
    for each in modules:
        modulesList.append(each)
        colourList.append(colours.pop(random.randrange(len(colours))))

    # Saves to config
    config.updateConfigExternal(googleAPI, timetableURL, year, modulesList, colourList)
    print('Updated configs')
    time.sleep(3)
    ClearScreen()

    print('Would you like the timetable to go into a different calendar other than you default one?')
    prompt = input('Yes/No: ')
    if 'Y' in prompt:
        print('We going to display the calendars you have on you account')
        print('Calendar Name : ID')
        calender.getCalID(calender.main())
        print('_______________________________________________________________________________________')
        print('Please paste in the calendar id of the calendar you want to use, use "primary" for your default one')
        calenderID = input('Calendar ID: ')
        config.updateCalID(calenderID)

    else:
        print("We're going to get the window up to ok this program's connection to Google Calendar")
        calender.main()
    ClearScreen()

    print('If no errors came up, you\'r ready!')
    print('IMPORTANT! The config folder holds personal info on you and your accounts and keys to access them!')
    print('Do not share these keys unless you know what you\'re handling!')
    print('==================================================================================================')
    print('Now run the program again now to start the import')


if __name__ == '__main__':
    if config.timetableURL == "":
        print("Starting setup")
        setup()
    else:
        if not config.loadedData:
            print('Starting initial import')
            webParser.initialLoad()
            print('Uploading to Google Calendar')
            calender.AddEvents(calender.main())
            config.updateLoaded()
        else:
            print("updating Entries")
            webParser.updateDatabase()
            print('Updating Google Calendar')
            calender.updateAndDeleteEvents(calender.main())
