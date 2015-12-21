# Lost & Found Recovery Service

By Daniel Balagula, Chisom Mba, Avash Rao, and Jason Yao

## Description

This repository is for our final project in CSCI-UA 480 Large Scalability, and is to contain all planning documents, 
the development pipeline setup scripts, along with the actual codebase for our application.

The application implements an anonymous lost & found service, where:

- Users can register to the site

- Users can register items they own

	- The application will create unique QR codes for them to print out and stick to their item

- If the object is lost & recovered, QR code can be scanned

	- Application will be notified of event & who recovering party was

	- Application will co-ordinate return of the lost item (simulated)

## Goals

- Create a full-fledged scalable web application

- Showcase security & scalability in design & planning of application

## Virtualenv Requirements: 
- Django==1.9
- enum34==1.1.1
- idna==2.0
- ipaddress==1.0.15
- MySQL-python==1.2.5
- Pillow==3.0.0
- pyasn1==0.1.9
- pycparser==2.14
- qrcode==5.1
- six==1.10.0
- uWSGI==2.0.11.2
- wheel==0.24.0

## Technology Stack

Tech Stack Design (metal up):
 
	[Operating System]	Ubuntu 14.04 x86_64

	[Load Balancer]		Amazon ELB

	[Application Server]	uWSGI + nginx

	[Application Framework]		Django

	[Relational Database]	MySQL

## License

This repository is licensed under the GNU General Public License (v2), found [here](LICENSE)
