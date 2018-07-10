
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
