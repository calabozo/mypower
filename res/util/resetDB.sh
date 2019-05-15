#!/bin/bash

docker run -v ../../data_docker/data_docker/postgresql:/var/lib/postgresql/data -ti `docker images | grep postgres | cut -d ' ' -f1` /bin/su postgres /usr/lib/postgresql/11/bin/pg_resetwal -f /var/lib/postgresql/data


