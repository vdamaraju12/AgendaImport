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
    value_requested = str(sys.argv[2])
    
    if column_requested not in VALID_COLUMN:
        print("Invalid column resquested.")
        return
    
    results = agenda.select(["date", "time_start", "time_end", "title", "location", "description", "speaker"], {column_requested: value_requested})
    for result in results:
        #print(result['description'])
        print("Date: {}\nTime Start: {}\nTime End: {}\nTitle: {}\nLocation: {}\nDescription: {}\nSpeaker: {}\n----------------------------------------------"
              .format(result['date'], result['time_start'], result['time_end'], result['title'], result['location'], result['description'], result['speaker']))

main()