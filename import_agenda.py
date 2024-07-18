import sys
import xlrd
import db_table

ROW_START = 15
DATE_ID = 0
TIME_START_ID = 1
TIME_END_ID = 2
SESSION_ID = 3
TITLE_ID = 4
LOCATION_ID = 5
DESCRIPTION_ID = 6
SPEAKER_ID = 7

def main():

    filename = sys.argv[1]
    filename = 'agenda.xls'
    if(filename[-3:] != "xls"):
        print("error: not an xls file.")
        return
    
    book = xlrd.open_workbook(filename)
    sh = book.sheet_by_index(0)
    db = db_table.create_table()
    
    print(sh.col_values(TITLE_ID, ROW_START))


main()