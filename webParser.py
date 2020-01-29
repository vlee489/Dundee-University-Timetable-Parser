"""
This python script is responsible for parsing the Dundee Timetable system
This will generate a database of classes
(c) Vincent Lee 2020

"""

import bs4 as bs
import urllib.request
import urllib.error
import config
import event

objectArray = []


def main():
    try:
        source = urllib.request.urlopen(config.timetableURL).read()  # Requests HTML page
    except urllib.error.HTTPError as e:
        print("Unable to open timetable Website, aborting!")
        print('Error code: ', e.code)
        exit(2)
    except urllib.error.URLError as e:
        print("There's an error with the timetable like that's been given to me")
        print("Go into config/config.json and fix the `timetableURL` please")
        print('Error code: ', e.reason)
        exit(3)
    soup = bs.BeautifulSoup(source, 'lxml')  # loads into BS with the data type of lxml
    print('Crunching through EVision Timetable')
    table = soup.find_all('table', {"class": "spreadsheet"})  # finds all the tables in HTML with day data
    for day in range(5):  # For each day table
        # find the entries with info on classes
        dayData = table[day]
        activities = dayData.find_all('tr')
        # for each class/activity we get the data on it
        for activity in range(1, len(activities)):  # We ignore the first entry as it's a header used by the website.
            items = activities[activity]
            td = items.find_all('td')
            # This checks if the user is taking the module
            for pos, module in enumerate(config.modulesTaken):
                if module in td[0].text:
                    colour = config.colourID[pos]
                    weeks = td[6].text  # Obtains the weeks the class is on for
                    # Checks if entry is for multiple weeks
                    if '-' in weeks:
                        weeks = weeks.split('-')
                        # If event is for multiple weeks we make an event object for one
                        for week in range(int(weeks[0]), int(weeks[1]) + 1):
                            # Creates object
                            instance = event.Event(module, td[2].text, td[8].text, td[7].text, colour)
                            instance.addDate(week, day, td[3].text, td[4].text)
                            objectArray.append(instance)  # Add object to list

                    else:
                        # If the event doesn't, creates object
                        instance = event.Event(module, td[2].text, td[8].text, td[7].text, colour)
                        instance.addDate(int(weeks), day, td[3].text, td[4].text)
                        objectArray.append(instance)  # add to list


# for inital load of calendar
def initialLoad():
    main()
    for events in objectArray:
        events.addToDatabase()


# for updating load of calendar
def updateDatabase():
    main()
    for events in objectArray:
        events.checkAndUpdate()
