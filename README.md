# File Event Notification

This script tail a file watching for defined events, and triggers a Pushover notification. 

My current use case is this: I've set my router up to forward syslog messages to a Raspberry Pi. On the Pi I'm running the script to tail the file containing the router syslog messages, and trigger a Pushover event upon certain events. 

# Usage

Create a Pushover account (https://pushover.net/), and fetch your application token and user token. 

Check out the script to for example /home/pi/scripts/file-event-notification. In the script, adjust the "filename" variable and "regexp_pattern" variable according to your needs. 

To make the script start at boot, add a line like this in /etc/rc.local:
```
python /home/pi/scripts/file-event-notification/watchfile.py -a "<pushover-app-token>" -u "pushover-user-token" &
```

