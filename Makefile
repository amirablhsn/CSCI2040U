PYTHON=python
RM=rm -rf
GREEN  = \033[0;32m
RESET  = \033[0m


# Default target
.PHONY: all
all: migrate import_data admin run

# Install django
.PHONY: install
install:
	pip install Django

# Migrations for database
.PHONY: migrate
migrate:
	@python -c "print('$(GREEN)Setting up sqlite database...$(RESET)')"
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

# Import CSV data to database
.PHONY: import_data
import_data:
	@python -c "print('$(GREEN)Importing CSV data into database.. $(RESET)')"
	@echo "from import_csv import import_csv; import_csv()" | $(PYTHON) manage.py shell
	@python -c "print('$(GREEN)Importing complete.$(RESET)')"


# Create a superuser for admin panel
.PHONY: admin
admin:
	@python -c "print('$(GREEN)Creating admin..$(RESET)')"
	@echo "from create_admin import create_admin; create_admin()" | $(PYTHON) manage.py shell

# Run application on dev server
.PHONY: run
run:
	@python -c "print('$(GREEN)Running server..$(RESET)')"
	$(PYTHON) manage.py runserver

.PHONY: clean
clean:
	$(RM) db.sqlite3
	$(RM) __pycache__
	$(RM) */__pycache__
	$(RM) *.pyc *.pyo
