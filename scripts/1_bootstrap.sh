#!/bin/bash
# Bootstraps with the most current, up to date settings

set -e

$APP_NAME=qFindr

# Sets up the python environment required
	BASEDIR=`dirname $0`/..
	$DATABASE_ROOT_PASSWORD=ChangeMeToALongRandomlyGeneratedPasswordBeforeRun
	$DATABASE_USER_PASSWORD=ChangeMeToALongRandomlyGeneratedPasswordBeforeRun

if [ ! -d "$BASEDIR/.env" ]; then
	apt-get install virtualenv -y
    virtualenv -p python3.5 -q $BASEDIR/.env --no-site-packages
    echo "Virtualenv created."
fi

if [ ! -f "$BASEDIR/.env/updated" -o $BASEDIR/requirements.pip -nt $BASEDIR/.env/updated ]; then
    source $BASEDIR/.env/bin/activate
	pip-3.5 install -r $BASEDIR/requirements.pip --upgrade

	pip-3.5 freeze > $BASEDIR/.env/updated
	touch $BASEDIR/.env/updated
	deactivate
    echo "Requirements installed."
fi

# Sets up the database tables & roles
	echo '$DATABASE_ROOT_PASSWORD' | sudo su - postgres
	psql
	CREATE DATABASE $APP_NAME;
	CREATE USER $APP_NAME WITH PASSWORD '$DATABASE_USER_PASSWORD';

	ALTER ROLE $APP_NAME SET client_encoding TO 'utf8';
	ALTER ROLE $APP_NAME SET default_transaction_isolation TO 'read committed';
	ALTER ROLE $APP_NAME SET timezone TO 'UTC';

	GRANT ALL PRIVILEGES ON DATABASE $APP_NAME TO $APP_NAME;
	\q
	exit

	service postgresql reload

	cd $BASEDIR/web/$APP_NAME

	source $BASEDIR/.env/bin/activate
	python manage.py makemigrations
	python manage.py migrate
	deactivate

	chown -R ubuntu:ubuntu $BASEDIR
	chown ubuntu:ubuntu /tmp/db.debug.log

## Start the dev server
# python manage.py runserver 0.0.0.0:8000
