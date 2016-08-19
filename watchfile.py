#!/bin/python
import time
import time, os
import httplib, urllib
import re
import sys, getopt
import syslog

filename = '/var/log/ruter.log'
regexp_pattern = 'Dropping frame due to full tx queue|error|warning|rebooting|shutdown'
user_token = ''
app_token = ''

def analyze_line(line):
    syslog.syslog("Analyzing this line: " + line)
    if re.search(regexp_pattern, line, re.IGNORECASE):
        send_notification(line)

def tail_file(filename):
    file = open(filename,'r')
    
    #Find the size of the file and move to the end
    st_results = os.stat(filename)
    st_size = st_results[6]
    file.seek(st_size)

    while 1:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            analyze_line(line)

def send_notification(line):
    syslog.syslog("This line triggered a notification: " + line)

    # Courtesy of https://github.com/raspberrycoulis/pushover
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.urlencode({
        "token": app_token,                       # Insert app token here
        "user": user_token,                       # Insert user token here
        "html": "0",                                # 1 for HTML, 0 to disable
        "title": "Rasberry Pi notification",                # Title of the message
        "message": line,     # Content of the message
        #"url": "http://IP.ADD.RE.SS",               # Link to be included in message
        #"url_title": "View live stream",            # Text for the link
        #"sound": "siren",                           # Define the sound played
        }), { "Content-type": "application/x-www-form-urlencoded" })
    response = conn.getresponse()

def main(argv):
   global app_token
   global user_token
   try:
      opts, args = getopt.getopt(argv,"a:u:",["app-token=","user-token="])
   except getopt.GetoptError:
      print 'Parameters: -a <apptoken> -u <usertoken>'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-a", "--app-token"):
         app_token = arg
      elif opt in ("-u", "--user-token"):
         user_token = arg

   tail_file("/var/log/ruter.log")

if __name__ == "__main__":
   main(sys.argv[1:])
