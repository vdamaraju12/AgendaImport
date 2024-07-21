import sys
from db_table import db_table
import sqlite3

VALID_COLUMN = ["date", "time_start", "time_end", "title", "location", "description", "speaker"]

def main():
    #open table
    agenda = db_table("agenda", {"id": "integer PRIMARY KEY",
                                 "parent_id": "integer",
                                 "date": "date NOT NULL",
                                 "time_start": "time NOT NULL",
                                 "time_end": "time NOT NULL",
                                 "session_type": "text NOT NULL",
                                 "title": "text",
                                 "location": "text",
                                 "description": "text",
                                 "speaker": "text"})
    
    #get/verify command line arguments
    column_requested = str(sys.argv[1])
    if column_requested not in VALID_COLUMN:
        print("Invalid column resquested.")
        return

    if len(sys.argv ) < 3:
        print("Invalid input parameter count.")
    value_requested = str(sys.argv[2])
    for i in range(3, len(sys.argv)):
        value_requested += " " + str(sys.argv[i])
    
    
    #'speaker' argument special request
    if column_requested == "speaker":
        results = agenda.select(["id", "date", "time_start", "time_end", "title", "location", "description", "speaker"],
                                {column_requested: '%{}%'.format(value_requested)}, ["LIKE"])
    else:
        results = agenda.select(["id", "date", "time_start", "time_end", "title", "location", "description", "speaker"],
                                {column_requested: value_requested}, [])
    #finding subsessions
    subsessions = []
    ids = []
    for result in results:
        ids.append(result["id"])

    for id in ids:
        subsessions += agenda.select(["id", "date", "time_start", "time_end", "title", "location", "description", "speaker"],
                                    {'parent_id': id})
    results += subsessions
    results = sorted(results, key = lambda d: d["id"])

    #printing out all results
    for result in results:
        out_string = ""
        if result['date'].strip() != "":
            out_string += "Date: {}\n".format(result['date'])
        if result['time_start'].strip() != "":
            out_string += "Time Start: {}\n".format(result['time_start'])
        if result['time_end'].strip() != "":
            out_string += "Time End: {}\n".format(result['time_end'])
        if result['title'].strip() != "":
            out_string += "Title: {}\n".format(result['title'])
        if result['location'].strip() != "":
            out_string += "Location: {}\n".format(result['location'])
        if result['speaker'].strip() != "":
            out_string += "Speaker: {}\n".format(result['speaker'])
        if result['description'].strip() != "":
            out_string += "Description: {}\n".format(result['description'])
        out_string += "---------------------------------------------------------------"
        print(out_string)

main()