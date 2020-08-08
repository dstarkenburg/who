####################################

	CS50x Final Project
	  "WhoIsInMySpot"
       By: Duncan Starkenburg

####################################

Hi, I am Duncan Starkenburg, I am 15, I live in Orange County, California, 
and this is my CS50 final project.


#######
SUMMARY
#######

My Dad and I wanted a way to log who and when people
parked in the space in front of our house. During the school
year various cars take the space we normally park in, so we
decided we should investigate exactly who is parking there.

The project is called WhoIsMySpot

The main idea is to have a camera setup facing the back license
plate of the car parked in the spot, then log when and what license
is parked in that spot throughout the day.

#######
DETAILS
#######

There is a python script, a Flask/HTML website, and a FTP server that the
camera posts to. 

The camera, in position, takes a photo every 15 minutes. It then names the file with a time stamp and
transfers the photo to a mounted drive on our webserver. Every minute, a python script called collector.py
reads the the directory of the images to check if a new image has been created. If it finds a new image, it
runs the image through OpenALPR (to check a license plate). Then, it takes the output from ALPR and inputs it into
a SQLite3 database. 

The website, running Flask and using an HTML template, updates every time the page is reloaded checking the SQLite
database for new entries or new photos. The website shows the latest photo, the time stamp, and declares whether or
not the car is in the 'known-cars' database.

A live website of this project is viewable at whoisinmyspot.com
