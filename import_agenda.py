import sys
import xlrd
from db_table import db_table
import sqlite3

ROW_START = 15
DATE_COL = 0
TIME_START_COL = 1
TIME_END_COL = 2
SESSION_COL = 3
TITLE_COL = 4
LOCATION_COL = 5
DESCRIPTION_COL = 6
SPEAKER_COL = 7

def main():

    #clear old table
    DB_NAME = "interview_test.db"
    db_conn = sqlite3.connect(DB_NAME)
    db_conn.execute("DROP TABLE IF EXISTS agenda")


    #open file
    filename = str(sys.argv[1])
    if(filename[-3:] != "xls"):
        print("error: not an xls file.")
        return
    
    #open book/sheet
    book = xlrd.open_workbook(filename)
    sh = book.sheet_by_index(0)
    tot_rows = sh.nrows

    #create SQL table
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
    
    sid = 1
    row = ROW_START
    while row < tot_rows:
        #constants
        date = sh.cell_value(row, DATE_COL)
        time_start = sh.cell_value(row, TIME_START_COL)
        time_end = sh.cell_value(row, TIME_END_COL)
        session_type = sh.cell_value(row, SESSION_COL)

        #apostrophe delimiter handling
        title = sh.cell_value(row, TITLE_COL).replace("'", "''")
        location = sh.cell_value(row, LOCATION_COL).replace("'", "''")
        description = sh.cell_value(row, DESCRIPTION_COL).replace("'", "''")
        speaker = sh.cell_value(row, SPEAKER_COL).replace("'", "''")
        
        #connecting sub sessions to parent rows
        if session_type == "Sub":
            pid = sid - 1
            while session_type == "Sub":
                agenda.insert({"id": str(sid),
                       "parent_id": str(pid),
                       "date": date,
                       "time_start" : time_start,
                       "time_end": time_end,
                       "session_type": session_type,
                       "title": title,
                       "location": location,
                       "description": description,
                       "speaker": speaker})
                sid += 1
                row += 1

                date = sh.cell_value(row, DATE_COL)
                time_start = sh.cell_value(row, TIME_START_COL)
                time_end = sh.cell_value(row, TIME_END_COL)
                session_type = sh.cell_value(row, SESSION_COL)

                title = sh.cell_value(row, TITLE_COL).replace("'", "''")
                location = sh.cell_value(row, LOCATION_COL).replace("'", "''")
                description = sh.cell_value(row, DESCRIPTION_COL).replace("'", "''")
                speaker = sh.cell_value(row, SPEAKER_COL).replace("'", "''")

        else:
            agenda.insert({"id": str(sid),
                        "parent_id": str(-1),
                        "date": date,
                        "time_start" : time_start,
                        "time_end": time_end,
                        "session_type": session_type,
                        "title": title,
                        "location": location,
                        "description": description,
                        "speaker": speaker})
            sid += 1
            row += 1
    #print(agenda.select(['parent_id'], {'session_type': "Sub"}))
    
main()
