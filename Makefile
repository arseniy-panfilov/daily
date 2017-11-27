PIP=pip3
PYTHON=python3
YOUR_INSTANCE_CONNECTION_NAME=daily-186904:australia-southeast1:daily-instance
BUCKET_NAME=daily-186904

run: check-venv
	$(PYTHON) manage.py runserver

check-venv:
ifndef VIRTUAL_ENV
	echo "\033[1;91m\n❗  You don't appear to be in a virtual environment, did you remember to";\
	echo "\033[0m    source daily/bin/activate"; echo "\033[1;91m?\033[0m"; exit 1
endif

# Database management
	
start-proxy-server:
	./cloud_sql_proxy -instances="$(YOUR_INSTANCE_CONNECTION_NAME)"=tcp:5432
	
# Static file management
	
collect-static:
	$(PYTHON) manage.py collectstatic

upload-static:
	gsutil rsync -R static/ gs://$(BUCKET_NAME)/static

