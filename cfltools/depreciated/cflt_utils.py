# Global Variables #
from cfltools.settings import APPFOLDER, INSTALLPATH
from cfltools.config import log_generator


# Instantiate the logger.
logger = log_generator(__name__)


def safeprompt(question, qtype):
    """Some custom input validation for prompts.
    """
    valid = False
    answer = input(question)
    if qtype == 'YN':
        # Verify a yes/no question got a yes/no answer. #
        while not valid:
            answer = answer.strip()
            if (answer == 'Y') or (answer == 'y'):
                return 'Y'
            if (answer == 'N') or (answer == 'n'):
                return 'N'
            answer = input('Please enter [Y/N]: ')
    if qtype == 'csv':
        while not valid:
            if answer.endswith('.csv'):
                return answer
            print('Filename {} is not a valid .csv file.'.format(answer))
            answer = input('Please enter a filename ending in .csv: ')
    raise InputError('Failed to validate input. {}, response was {}'.format(question,answer))


def listIncidents(conn):
    import sqlite3
    c = conn.cursor()
    c.execute('SELECT incident_name FROM incidents')
    result = c.fetchall()
    print("Incidents currently in stored in the database:")
    for incident_name in result:
        print(' * ' + incident_name[0])


def getmd5hash(file):
    # Get the MD5 hash of <file> to uniquely
    # identify it.
    import hashlib
    hash_md5 = hashlib.md5()
    with open(file,"rb") as f:
        for chunk in iter(lambda: f.read(4096),b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def markFileAsSeen(filename, incident_name, config):
    import sqlite3
    db_loc =  config['USER']['db_loc']
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    md5hash = getmd5hash(filename)
    c.execute('INSERT INTO seenFiles(filename,md5,incident_id) VALUES(?,?,?)',(filename,md5hash,incident_name))
    conn.commit()
    conn.close()


def checkFileWasSeen(filename, config):
    import sqlite3
    db_loc = config['USER']['db_loc']
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    md5hash = getmd5hash(filename)
    c.execute('SELECT filename FROM seenFiles WHERE md5 = ?',(md5hash,))
    data = c.fetchall()
    if len(data) == 0:
        conn.close()
        return False
    conn.close()
    return True


def checkIncidentNameExists(incident_name, config):
    import sqlite3
    db_loc = config['USER']['db_loc']
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    try:
        c.execute('SELECT incident_name FROM incidents WHERE incident_name = ?',(incident_name,))
    except sqlite3.Error as e:
        print('Database error: {}'.format(e))
        print('Using database located at {}'.format(db_loc))
    except:
        print('Error in checkIncidentNameExists()')
        print('Using database located at {}'.format(db_loc))
    data = c.fetchall()
    if len(data) == 0:
        conn.close()
        return False
    conn.close()
    return True


def generateIncident(incident_name, config):
    import sqlite3
    from pathlib import Path
    from os import makedirs
    db_loc = config['USER']['db_loc']
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    incident_description = input('Please enter a description of the incident: ')
    folder_loc = APPFOLDER+'/'+incident_name
    if not Path(folder_loc).is_dir():
        makedirs(folder_loc)
    c.execute('INSERT INTO incidents(incident_name,folder_loc,description) VALUES(?,?,?)',(incident_name,folder_loc,incident_description))
    conn.commit()
    conn.close()


def checkforDB(config):
    from pathlib import Path
    incident_db = Path(config['USER']['db_loc'])
    if not incident_db.exists():
        print('Incident database was not found at {}. Initializing the database.'.format(str(incident_db)))
        return False
    print('All required files were detected.')
    return True


def createDatabase(config):
    from shutil import copyfile
    from os import getcwd
    logger.debug("Script current working directory is {}".format(getcwd()))
    incident_db_default = INSTALLPATH + '/default/default.db'
    copyfile(incident_db_default,config['USER']['db_loc'])
