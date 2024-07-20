import sys
from db_table import db_table
import sqlite3

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
    column_requested = sys.argv[1]
    value_requested = sys.argv[2]