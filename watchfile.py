#!/bin/python
import time
import time, os
import httplib, urllib
import re
import sys, getopt
import syslog
import tailer
import atexit

user_token = ''
app_token = ''
pid_file = '/run/watchfile.pid'

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

def write_pid_file():
    pid = str(os.getpid())
    print "PID: " + pid
    f = open(pid_file, "w")
    f.write(pid)
    f.close()

def all_done():
    pid = str(pid_file)
    os.remove(pid)

if __name__ == "__main__":
    
    try:    
        atexit.register(all_done) # Courtesy of https://coderwall.com/p/fudnxq/keep-your-python-app-running
        write_pid_file()
        main(sys.argv[1:])
        all_done()
    except KeyboardInterrupt:
        sys.exit(0)

