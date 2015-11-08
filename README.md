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

## Technology Stack

Tech Stack Design (metal up):
 
	[Operating System]		TBD

	[Load Balancer]			TBD

	[Application Server]	TBD

	[Application Framework]	Django

	[Relational Database]	PostgreSQL

## License

This repository is licensed under the GNU General Public License (v2), found [here](LICENSE)
