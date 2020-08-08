import glob
import subprocess
import os
import json
import sqlite3
from datetime import datetime
import time
import urllib.request

IMAGE_DIRECTORY = "/var/www/FLASKAPPS/whoisinmyspot/static/who/" # Please use a trailing slash. Leave blank if running in image directory.
DATABASE_PATH = "/var/www/FLASKAPPS/whoisinmyspot/static/carsinmyspot.db"
URL = "" # For use in HTTP image request

### THIS SECTION IS IF YOU ARE USING AN EXTERNAL CAMERA BY HTTP REQUEST ###

# Get image and save it 
#print("Getting image")
#passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
#passman.add_password(None, URL, "admin", "mstarken")
#authhandler = urllib.request.HTTPBasicAuthHandler(passman)
#opener = urllib.request.build_opener(authhandler)
#urllib.request.install_opener(opener)
#datestr = time.strftime("%Y-%m-%d_%H-%M-%S")
#try:
#   urllib.request.urlretrieve(URL, datestr + ".jpg")
#except:
#   print("Image could not be accessed/saved. Using most recent image!")

###########################################################################




### THIS SECTION IS USED FOR EVERY OTHER IMAGE SAVING METHOD ###

# Look at jpg files in current directory, get latest created file
list_of_files = glob.glob(IMAGE_DIRECTORY + '*.jpg')
latest_file = max(list_of_files, key=os.path.getctime)

# Parse name of file for date and time
basename = os.path.basename(latest_file)
filename = os.path.splitext(basename)[0]
dateTime_object = datetime.strptime(filename, "%Y-%m-%d_%H-%M-%S")
date = datetime.strftime(dateTime_object, "%b %d %Y %I:%M%p")

#Create a function to get latest observation image file
def getLatestObsImg():
    sqliteConn = sqlite3.connect(DATABASE_PATH)
    cursor = sqliteConn.cursor()
    cursor.execute("SELECT image FROM observations ORDER BY image DESC LIMIT 1")
    latest_obsimg = cursor.fetchall()
    return latest_obsimg
# Create a function to run OpenALPR on latest picture and get license and confidence
def runALPR(latest_file):
    alprCmd = ("alpr -j %s" % latest_file)
    alprOut = subprocess.run([alprCmd], shell=True, stdout=subprocess.PIPE)
    alprJson = json.loads(alprOut.stdout.decode('utf-8'))
    try:
        license = alprJson['results'][0]['plate']
        confidence = alprJson['results'][0]['confidence']
    except IndexError:
        license = "None Found"
        confidence = "N/A"
    return license, confidence
# Create a function to write the information to the Sqlite3 DB
def writeToDatabase(license, confidence, dateTime, image):
    sqliteConn = sqlite3.connect(DATABASE_PATH)
    cursor = sqliteConn.cursor()
    cursor.execute("insert into observations (license, datetime, image, confidence) values (?, ?, ?, ?)", (license, dateTime, image, confidence))
    sqliteConn.commit()
    print(license, confidence, dateTime, image)
    print("Written to database!")


# Check for duplicate image, then execute the functions
latest_obsimg = getLatestObsImg()
if latest_obsimg[0][0] != basename:
    print("Ooooh a new image! :0 (New image)")
    alprTuple = runALPR(latest_file)
    writeToDatabase(alprTuple[0], alprTuple[1], date, basename)
else:
    print("File was kinda boring :/ (Duplicate image)")
#################################################################