PYTHON=python
RM=rm -rf

# Default target
.PHONY: all
all: migrate import_data createsuperuser runserver

# Install django
.PHONY: install
install:
	pip install Django

# Migrations for database
.PHONY: migrate
migrate:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

# Import CSV data to database
.PHONY: import_data
import_data:
	echo "from import_csv import import_csv; import_csv()" | $(PYTHON) manage.py shell

# Create a superuser for admin panel
.PHONY: createsuperuser
createsuperuser:
	$(PYTHON) manage.py createsuperuser

# Run application on dev server
.PHONY: runserver
runserver:
	$(PYTHON) manage.py runserver

.PHONY: clean
clean:
	$(RM) db.sqlite3
	$(RM) __pycache__
	$(RM) */__pycache__
	$(RM) *.pyc *.pyo
