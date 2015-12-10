# uWSGI Section

## Description

This directory contains two parts, an Upstart script to regenerate uWSGI at boot, and the configuration files for the uWSGI server itself.

## Upstart script
The uwsgi script will be symlinked to `/etc/init/uwsgi.conf` to start at boot
