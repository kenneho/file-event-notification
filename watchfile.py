#!/bin/python
import time
import time, os
import httplib, urllib
import re
import sys, getopt
import syslog
import tailer

user_token = ''
app_token = ''

def analyze_line(line):
    syslog.syslog("Analyzing this line: " + line)
    if re.search(regexp_pattern, line, re.IGNORECASE):
        send_notification(line)

def tail_file(filename): 
    for line in tailer.follow(open(filename)): 
        analyze_line(line)

def send_notification(line):
    syslog.syslog("This line triggered a notification: " + line)

    try:
        # Courtesy of https://github.com/raspberrycoulis/pushover
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.urlencode({
            "token": app_token,                       # Insert app token here
            "user": user_token,                       # Insert user token here
            "html": "0",                                # 1 for HTML, 0 to disable
            "title": "Rasberry Pi notification",                # Title of the message
            "message": line,     # Content of the message
            }), { "Content-type": "application/x-www-form-urlencoded" })
        response = conn.getresponse()
    except:
        syslog.syslog("Connecting to Pushover failed. Could not send notification.")

def main(argv):
   global app_token
   global user_token
   global regexp_pattern

   try:
      opts, args = getopt.getopt(argv,"a:u:r:",["app-token=","user-token=","regexp="])
   except getopt.GetoptError:
      print 'Parameters: -a <apptoken> -u <usertoken> -r <regexp>'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-a", "--app-token"):
         app_token = arg
      elif opt in ("-u", "--user-token"):
         user_token = arg
      elif opt in ("-r", "--regexp"):
         regexp_pattern = arg

   tail_file("/var/log/ruter.log")

if __name__ == "__main__":
   main(sys.argv[1:])
