This repository contains the process for our CSCI2040U final project.

Members
- Michael Edmonds
- Amir Abou-El-Hassan
- Samir Chowdhury
- Christine Tran
- Asjad Mian

## Dev Setup
Clone the repo, and cd into the directory
Make sure you have Django installed, if not run `pip install Django`

In the terminal run the following commands
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py shell
```
Inside the shell run
```py
from import_csv import import_csv
import_csv()
```
Wait for the database to finish setting up, it might take a few mintues.

Once finished, to exit the shell type `quit()`

To access the Django admin panel you'll need to create a superuser.

In the terminal run
```sh
python manage.py createsuperuser
```
Remember the username and password you entered to login.

Run your local server with
```sh
python manage.py runserver
```
The terminal will display the address that you can open in your browser. It should look like this http://127.0.0.1:8000/

To view the admin panel, http://127.0.0.1:8000/admin