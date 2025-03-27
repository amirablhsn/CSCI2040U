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
TODO: Add descriptions
### Models
`Vehicle`

### Views
`add`

`details`

`edit`

`delete`

### Templates
`base`

## Future Improvements/Features 
TODO: Add features we didn't complete

## Tech Stack
- **Framework**: Django
- **Language**: Python
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript

## Contributors
- Michael Edmonds
- Amir Abou-El-Hassan
- Samir Chowdhury
- Christine Tran
- Asjad Mian


