#!/bin/bash
# Bootstraps with the most current, up to date settings

set -e

$APP_NAME=finder

# Sets up the python environment required
	BASEDIR=`dirname $0`/..
	$DATABASE_ROOT_PASSWORD=u50wAl7bfIKGgwseMPeGxgOGJ7PxSkiDa&vZdzQ&NzyU5hmMAiQnDyTI*yE7LtcfBZM#5Wz2@x^ouK1!Mdeqd^hFrlr^#SJuBFu
	$DATABASE_USER_PASSWORD=wQeYU!3qZdfOJ6iu&UWI4rNyjB4AA3y&35OgY7Mr!blyL*ZSXo2KSTH^Wbj1f4347kn@MkBQxB6Hg3kjd^jC2@KnAF6#Xlib

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
	echo 'Setting up database tables, roles, users & migrations'
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

	cd $BASEDIR/web

	source $BASEDIR/.env/bin/activate
	# Creates & populates tables
	python manage.py makemigrations
	python manage.py migrate

	# Creates administrative accounts for django
    python manage.py createsuperuser
	deactivate

	chown -R ubuntu:ubuntu $BASEDIR
	chown ubuntu:ubuntu /tmp/db.debug.log

# Final reminders
	echo 'Please remember to CHANGE THE APP PASSWORD in web/$APP_NAME/settings.py'

## Start the dev server
# python manage.py runserver 0.0.0.0:8000
