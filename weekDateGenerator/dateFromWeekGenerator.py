"""
This is a tool used to generate dates from the week data handed to it
that's inline with Dundee Universities week system, so that the parser
can tie dates to each event on the timetable.

You do not need this to run the program as the program will grab the data from
the online file with this that has been checked. Hence this wasn't intended to
be easily read by users.
"""
import datetime
import json

startDate = "16/09/2019"  # This defines the date which the Dundee Uni starts (DD/MM/YYYY)
endDate = "29/05/2020"  # This defines the date which the Dundee Uni ends(DD/MM/YYYY)
academicYear = "2019-2020"  # The Academic Year it ties to

dataStruct = []

startDate = datetime.datetime.strptime(startDate, '%d/%m/%Y')
endDate = datetime.datetime.strptime(endDate, '%d/%m/%Y')

while startDate <= endDate:
    weekStruct = []
    for day in range(7):
        inputString = '"{}":"{}"'.format(day, startDate.strftime('%d/%m/%Y'))
        weekStruct.append(inputString)
        startDate += datetime.timedelta(days=+1)
    weekdata = '{' + ', '.join(weekStruct) + ' },'
    dataStruct.append(weekdata)
    weekStruct = []

print(' '.join(dataStruct))
