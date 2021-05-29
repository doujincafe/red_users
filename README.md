# red_users
A simple python script that collects per user data of snatched torrents from Redacted. It collects the user, ratio, uploaded amount, downloaded amount of each snatched torrent 1 minute after it completed downloading. The purpose is to find users which consistently give you bad ratio when auto snatching. The data is stored in csv file which can be easily imported into Excel or Google Sheets to do further analysis.

## Configuration
Edit the script to enter the host, port, username and password of your Deluge daemon. Create an API key on Redacted and enter it into the script too. You might also want to change the path to the csv file.

Install the [Execute](https://dev.deluge-torrent.org/wiki/Plugins/Execute) plugin in your Deluge client. Then go the settings of Execute and create a new command. As event select "Torrent Completed" and for Command enter the path of the script. Make sure the script is executable.
