#!/bin/bash
# Setup an EC2 development environment (with virtual env).

virtual_envs=largescale
install_dir=/home/ubuntu/${virtual_envs}

set -e

# Updates and upgrades server
	apt-get update -y
	apt-get dist-upgrade -y

# Installs underlying packages
	apt-get install git -y					# Used in general project upkeep
	apt-get install wget -y					# Used in downloading python
	apt-get install checkinstall -y			# Used in checking in python to apt-get
	apt-get install build-essential -y		# Used in compiling python

# Installs database specifics (postgreSQL)
	apt-get install libpq-dev postgresql postgresql-contrib -y
	# Uncomment if using mySQL
	#apt-get install libmysqlclient-dev -y
	#export DEBIAN_FRONTEND=noninteractive
	#apt-get -q -y install mysql-server -y

# Sets up filesystem
	mkdir -p $install_dir
	chown ubuntu:ubuntu $install_dir

# Install python v3.5
	cd $install_dir
	wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tar.xz
	tar xvfJ Python-3.5.0.tar.xz
	cd $install_dir/Python-3.5.0
	
	# Compilation steps
    ./configure
    make
	sudo make install # `sudo checkinstall` is better due to being able to keep track of the package through apt-get, but isn't fully non-interactive

	# Cleanup
	cd $install_dir
	rm -rf Python-3.5.0/ Python-3.5.0.tar.xz

# Downloads the source files
    git clone https://github.com/JasonYao/Large-Scale-Final-Project-Lost-and-Found-Recovery-Service.git .

# Installs clean project-specific virtual environment (venv)
	pyvenv $install_dir/.env
	
echo ''
echo 'Main ec2 setup is complete, please run ./1_bootstrap.sh for machine specific run instructions [REMEMBER TO CHANGE THE PASSWORD!]'
