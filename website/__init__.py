## WhoIsInMySpot ##

from flask import Flask, render_template
from flask import request, redirect, g
import sqlite3
import time
import os
import glob
import ntpath
app = Flask(__name__, static_url_path='/static')

app.config["IMAGE_UPLOADS"] = "/var/www/FLASKAPPS/whoisinmyspot/static/who"

@app.route("/")
def index():
  
  datestr = time.strftime("%b %d %Y")

  list_of_files = glob.glob('/var/www/FLASKAPPS/whoisinmyspot/static/who/*.jpg')
  latest_file = ntpath.basename(max(list_of_files, key=os.path.getctime))

  # Setup Database connection
  cursor = get_db().cursor()

  # Get top 6 and write to "rows"
  cursor.execute("SELECT * FROM observations ORDER BY image DESC LIMIT 5")
  rows = cursor.fetchall()

  # Latest Picture Square
  latestPlate = rows[0][0]
  cursor.execute("SELECT count(*) FROM knowncars WHERE license = ?", (latestPlate,))
  latestKnownObject = cursor.fetchall()
  latestKnown = bool(latestKnownObject[0][0])
  latestDate = rows[0][1]

  # Use top 6 to get plates, confidence, and date
  plate1 = rows[0][0]
  plate2 = rows[1][0]
  plate3 = rows[2][0]
  plate4 = rows[3][0]
  plate5 = rows[4][0]
  confidence1 = rows[0][3]
  confidence2 = rows[1][3]
  confidence3 = rows[2][3]
  confidence4 = rows[3][3]
  confidence5 = rows[4][3]
  date1 = rows[0][1]
  date2 = rows[1][1]
  date3 = rows[2][1]
  date4 = rows[3][1]
  date5 = rows[4][1]

  # Statistics Logics.
  execute1 = "SELECT license, COUNT(license) AS `value_occurrence` FROM observations WHERE datetime LIKE '%"+datestr+"%' GROUP BY license ORDER BY `value_occurrence` DESC LIMIT 1"
  cursor.execute(execute1)
  licenseMostSeen = cursor.fetchall()
  execute2 = "SELECT count(license) FROM observations WHERE datetime LIKE '%"+datestr+"%' GROUP BY license"
  cursor.execute(execute2)
  licenseTotalTimes = cursor.fetchall()
  execute3 = "SELECT count(*) FROM observations WHERE datetime LIKE '%"+datestr+"%' AND license = "+"'"+latestPlate+"'"
  cursor.execute(execute3)
  licenseSeenTimes = cursor.fetchall()

  license1 = latestPlate
  minutes = int(licenseSeenTimes[0][0]) * 15

  try:
  	license2 = licenseMostSeen[0][0]
  except:
  	license2 = "None Found"

  try:
  	totalTimes = licenseTotalTimes[0][0]
  except:
  	totalTimes = "0"

  if license1 == 'None Found':
  	statistic1 = "No car has been parked in our spot for %i minutes today!" % (minutes)
  else:
  	statistic1 = "License %s has ben parked in our spot for %i minutes today!" % (license1, minutes)

  if license2 == 'None Found':
  	statistic2 = ""
  else:
  	statistic2 = "License %s has been the car most often parked in our spot. %i times in the last day!" % (license2, totalTimes)

  # Check to see if cars are known
  cursor.execute("SELECT count(*) FROM knowncars WHERE license = ?", (plate1,))
  known1object = cursor.fetchall()
  known1 = bool(known1object[0][0])
  cursor.execute("SELECT count(*) FROM knowncars WHERE license = ?", (plate2,))
  known2object = cursor.fetchall()
  known2 = bool(known2object[0][0])
  cursor.execute("SELECT count(*) FROM knowncars WHERE license = ?", (plate3,))
  known3object = cursor.fetchall()
  known3 = bool(known3object[0][0])
  cursor.execute("SELECT count(*) FROM knowncars WHERE license = ?", (plate4,))
  known4object = cursor.fetchall()
  known4 = bool(known4object[0][0])
  cursor.execute("SELECT count(*) FROM knowncars WHERE license = ?", (plate5,))
  known5object = cursor.fetchall()
  known5 = bool(known5object[0][0])

  imageFile = latest_file

  return render_template("index.html", imageFile=imageFile, latestPlate=latestPlate, latestKnown=latestKnown, latestDate=latestDate, plate1=plate1, plate2=plate2, plate3=plate3, plate4=plate4,
  plate5=plate5, confidence1=confidence1, confidence2=confidence2, confidence3=confidence3, confidence4=confidence4, confidence5=confidence5, date1=date1,
  date2=date2, date3=date3, date4=date4, date5=date5, known1=known1, known2=known2, known3=known3, known4=known4, known5=known5, statistic1=statistic1, statistic2=statistic2)

def get_db():
  DATABASE = '/var/www/FLASKAPPS/whoisinmyspot/static/carsinmyspot.db'
  db = getattr(g, '_database', None)
  if db is None:
      db = g._database = sqlite3.connect(DATABASE)
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
      db.close()

@app.route("/admin")
def admin():
  return 'Hello Admin!'

@app.route("/campost", methods=["POST"])
def campost():

    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            datestr = time.strftime("%Y-%m-%d_%H-%M-%S")

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], datestr +".jpg"))

            print("Image saved")
	return "Ok"

if __name__ == '__main__':
  app.run()