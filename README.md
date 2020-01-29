# Dundee-University-Timetable-Parser
Turn your Dundee EVision timetable to Google Calendar

This is a program used to upload University of Dundee's EVision generated semester timetable into events on Google 
Calendar.

I can not guarantee this will work for all Dundee student timetables, and has only been tested on 
Computer Science/Applied Computing timetables.

### Requirments
- Python 3.7+
- Google Calendar API (*You're walked through getting this*)

### Usage

1. Clone this repo and open it up

2. You'll need to install the Python requirements for this program by doing the following
```bash
pip install -r requirements.txt
```

3. Now you can run the main program itself
```bash
python main.py
```

4. Follow the prompts in the program to upload your timetable to Google Calendar

### Other bits

##### Delete all entries
You can run `calendar.py` on its own after setup to delete all the entries it has made with the following
```bash
python calendar.py
```

##### Use of each python file
- `config.py`: Used for holding the parsing configs used by each script
- `main.py`: Used to run setup and to run the other scripts
- `webParser.py`: Scrapes the timetable itself and places the entries into the database
- `event.py`: Class for holding event data before doing into the Database
- `calendar.py`: Handles all the communication with Google Calendar for uploading, updating and removing events/classes