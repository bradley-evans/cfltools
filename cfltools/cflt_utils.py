# Global Variables #
from cfltools.settings import *

def listIncidents():
    import sqlite3
    db_loc = APPFOLDER+'/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    c.execute('SELECT incident_name FROM incidents')
    result = c.fetchall()
    print("Incidents currently in stored in the database:")
    for incident_name in result:
        print(incident_name)
    conn.close()

def getmd5hash(file):
    import hashlib
    hash_md5 = hashlib.md5()
    with open(file,"rb") as f:
        for chunk in iter(lambda: f.read(4096),b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def checkIncidentNameUnique(incident_name):
    import sqlite3
    db_loc =  APPFOLDER+'/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    c.execute('SELECT incident_name FROM incidents WHERE incident_name = ?',(incident_name,))
    data = c.fetchall()
    if len(data) == 0:
        conn.close()
        return True
    conn.close()
    return False

def generateIncident(incident_name):
    import sqlite3
    from pathlib import Path
    from os import makedirs
    db_loc =  APPFOLDER+'/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    incident_description = input('Please enter a description of the incident: ')
    folder_loc = APPFOLDER+'/'+incident_name
    if not Path(folder_loc).is_dir():
        makedirs(folder_loc)
    c.execute('INSERT INTO incidents(incident_name,folder_loc,description) VALUES(?,?,?)',(incident_name,folder_loc,incident_description))
    conn.commit()
    conn.close()

def checkforDB(loc):
    from pathlib import Path
    incident_db = Path(loc+'/incident.db')
    if not incident_db.exists():
        print('Incident database was not found at {}. Initializing the database.'.format(str(incident_db)))
        return False
    print('All required files were detected.')
    return True

def createDatabase(loc):
    from shutil import copyfile
    from os import getcwd
    print("In cfl_utils.createDatabase(). loc={}".format(loc))
    print("Script current working directory is {}".format(getcwd()))
    incident_db_default = getcwd() + '/cfltools/default/default.db'
    incident_db_target = loc+'/incident.db'
    copyfile(incident_db_default,incident_db_target)
