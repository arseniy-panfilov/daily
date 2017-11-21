PIP=pip3
PYTHON=python3

run: check-venv
	$(PYTHON) manage.py runserver

check-venv:
ifndef VIRTUAL_ENV
	echo "\033[1;91m\n❗  You don't appear to be in a virtual environment, did you remember to";\
	echo "\033[0m    source daily/bin/activate"; echo "\033[1;91m?\033[0m"; exit 1
endif

test: check-venv
	$(PYTHON) manage.py test
	
