# api_client_python
Some examples to show how to interact with the OfficeSpace API using Python

# Prerequisites

## External libraries
This script depends on the python library `requests` to work. Make sure
it is installed before running.

A quick way install `requests` if it isn't yet:
```bash
sudo easy_install pip
sudo pip install --upgrade pip
pip install requests
```

## Optional: Scheduling via `crontab`

If you wish to schedule the script to run at specific intervals,
you have to set up a cron job.

1) Decide the frequency at which you want to run the script and note the cron
   expression for it. For example, if you want to run it every hour, 
   the cron expression would look like "0 * * * *".  
   Use https://crontab.guru/ as reference.
2) Run `crontab -e` to edit the cron file.
3) Put in a new line: `<crontab expression> <full path to python> <full path to script>`  
   For example, a new line could be `30 * * * * /usr/bin/python /Users/johndoe/projects/bamboo_to_officespace.py`  
   Save the file and exit the editor.
4) `crontab -l` to check if the new settings apply. You should see the latest task in the list.
