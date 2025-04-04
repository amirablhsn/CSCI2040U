# Django Vehicle Catalogue Web App

## Project Information
This Vehicle Catalogue Website allows user to browse, search, filter and manage the catalogue of cars. It provides detailed information about each car, including make, model, year, price, and other vehicle specifications. 

### Key Features
- Browse vehicles in the catalogue
- Search and filter vehicles based on specific criteria
- View images and detailed information for each vehicle
- Create an account and sign in
- Admin interface to manage catalogue (add, edit, delete)


## Installation and Developer Setup
**Requirements**: Ensure you have `python` and `pip` installed

In the directory repository use the command line
If you do not have Django installed, run:
```bash
make install
```
Once Django is installed, to initalize the database, import data, create an admin account, and run the server:
```bash
make
```
To clean the repository and remove unwanted built files:
```bash
make clean
```

If changes are made to the database structure, to apply changes:
```bash
make migrate
```

After setting up the data base and creating an admin account, to run the server:
```bash
make run
```

Once the server is running, it can be accessed by the localhost address provided in the terminal.

## Testing
To run all tests:
```bash
make test
```

To run catalogue tests:
```bash
make test_catalogue
```

To run user tests:
```bash
make test_users
```

## Key Django Modules

### Key Project Directories/Files
```text
CSCI2040U/
├── autosearchapp/                 # Contains project settings
├── catalogue/                     # The core catalogue application
│   ├── static/                    # Styles for the templates
│   ├── templates/                 # Frontend for main catalogue pages 
│   │   └── *.html
│   ├── tests/                
│   │   ├── test_admin_views.py    # Tests for admin functionns - add,edit,delete
│   │   ├── test_form.py           # Tests for vehicle form
│   │   ├── test_model.py          # Tests for vehicle model
│   │   └── test_views.py          # Test for non-admin functions - search, filter, fetching vehicle details, adding favourites
│   ├── forms.py                   # Contains Vehicle form for add and edit
│   ├── models.py                  # Contains Vehicle & Favourites Models
│   ├── urls.py                    # Contains paths for the main catalogue pages, maps urls to views
│   └── views.py                   # Functions for main features (add, edit, delete, search, filter etc.)
└── users/                         # App that handles user related features
    ├── templates/                 # Frontent for registration, login, and profile page
    │   └── *.html
    ├── tests/                  
    │   ├── test_admin.py          # Tests adding/removing adming, and restricting access
    │   ├── test_registration.py   # Tests for registering a new user
    │   └── test_user.py           # Tests for login/logout and fetching users favourites                      
    ├── forms.py                   # Login & Registration forms
    ├── urls.py                    # Contains paths for user related pages 
    └── views.py                   # User related functions - register/login/logout/profile/admin
```

### Models
- `Vehicle`
- `Favourite`
- `User`

### Views 
#### Guest Views
- `search`
- `filter`
- `detials`
- `register`
- `login_view`

#### User Views
- `logout`
- `profile_view`
- `request_admin`
- `remove_admin`
- `toggle_favourite`

#### Admin Views
- `add`
- `edit`
- `delete`

## Future Improvements/Features 
TODO: Add features we didn't complete

## Tech Stack
- **Framework**: Django
- **Language**: Python
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript

## Dependencies
- Bootstrap 5.3.3
- Google Fonts - Roboto
- Fontawesome 6.7.2

## Contributors
- Michael Edmonds
- Amir Abou-El-Hassan
- Samir Chowdhury
- Christine Tran
- Asjad Mian


