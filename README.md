# User Creation Package

This script will help you to create users with LDAP and send email to user which is tested well with Ubuntu/Mac machine.

## USAGE:

Please make sure your machine have python3.x and pip3 installed.


This command will install all necessary python packages on your machine.
```
pip3 install -r requirements.txt --user
```

This command will show you necessary values for this script to run.
```
cat admin.cfg
```

Edit the file and add appropriate values.
```
vim admin.cfg 
```


This sets up the environment variables.

```
set -a; source admin.cfg; set +a
```


Example for single user creation - 

```
python3 createUsers.py --firstname FIRSTNAME --lastname LASTNAME --email user@example.com --title 'Mr/s' --org 'COMPANY'
```

Example for multiple user creation using CSV - 

```
python3 createUsers.py --csv PATH_TO_CSV
```

Example for multiple user creation usign Excel - 

```
python3 createUsers.py --xl PATH_TO_EXCEL --sheet NAME_OF_THE_SHEET
```

Sample EXCEL file and CSV is given.