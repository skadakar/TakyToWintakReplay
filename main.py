import datetime
import glob
import re
import sqlite3
from operator import itemgetter
from re import search
from dateutil import parser

path = './logs'
dbname = 'TakyExport-' + str(datetime.date.today())

con = sqlite3.connect(dbname + ".cpr")
con.execute(
    "CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT, type TEXT, message TEXT, source TEXT, time INTEGER)")
con.execute(
    "CREATE TABLE IF NOT EXISTS initialState (id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT, type TEXT, message TEXT, source TEXT, time INTEGER)")


def list_cots_from_folder(path):
    cotlist = [f for f in glob.glob(path + "/*.cot")]
    return cotlist


def extract_cots_from_files():
    cotlist = [f for f in glob.glob("logs/*.cot")]
    unsorted_cots = []
    for elem in cotlist:
        content = (open(elem, 'r').read())
        poop = content.split("</event>")
        for thing in poop:
            if len(thing) > 10:
                thing = thing + str("</event>")
                thing = str("""<?xml version="1.0" encoding="utf-8" standalone="yes"?>""") + thing
                thing = thing.strip()
                uid = str(re.findall('(?<=uid=")(.*?)(?=")', thing))
                uid = uid.replace("[", "").replace("'", "").replace("]", "")
                time = str(re.findall('(?<=time=")(.*?)(?=")', thing))
                time = time[2:26]
                epoch = parser.parse(time).timestamp() * 1000
                epoch = int(round(epoch))
                thing = thing.replace("\n", "").replace("  ", "")
                newlist = [epoch, uid, thing]
                # Discard geochat
                # Discard everything before 2005 because that has to be junk data..
                if not search("GeoChat", uid):
                    if epoch > 1124749097000:
                        unsorted_cots.append(newlist)
    return unsorted_cots


def sort_unsorded_cots():
    input = extract_cots_from_files()
    sortedinput = sorted(input, key=itemgetter(0))
    return sortedinput


def insert_events_database(list_of_lists):
    print("Export started")
    seq = 0
    for elem in list_of_lists:
        dbseq = str(seq)
        dbepoch = elem[0]
        dbuid = str(elem[1])
        dbcot = str(elem[2])
        dbtype = str("cot")
        dbsource = str("*:4242:tcp")
        print(dbseq, dbepoch, dbuid, dbcot[0:15], dbtype, dbsource)
        pooplist = [str(dbuid), str(dbtype), str(dbcot), str(dbsource), str(dbepoch)]
        con.execute("INSERT OR REPLACE INTO events values (NULL,?,?,?,?,?)", pooplist)
        seq = int(seq) + 1
    con.commit()
    print("Export done, " +str(seq) + " events added.")

(insert_events_database((sort_unsorded_cots())))
