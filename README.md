
<p  align="center"><img  src="django-docker.png"  alt="django-docker"  width="200"/></p>

# Django-Docker CLI

https://ronnasayd.github.io/django-docker/

![enter image description here](https://travis-ci.org/Ronnasayd/django-docker.svg?branch=master) [![enter image description here](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE.md)

System to automatically create development and production environments in django with docker and facilitate the development of applications.
## Required Programs
- [Python](https://www.python.org/) ^= 3
- [Docker](https://www.docker.com/)
- [Docker compose](https://docs.docker.com/compose/)
## How to use
The files (***config.py***, ***pydd.py*** e ***ddo.sh*** ) and the folder (***modules***) should be in the directory of your django project.

Modify the ***config.py*** settings as you wish, and then run the ***ddo.sh*** script. The ***pydd.py*** file will use ***config.py*** settings to mount the desired infrastructure on the system.

The choice of environment between development or production is made by the ***DEBUG*** variable located in the file ***config.py***

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details