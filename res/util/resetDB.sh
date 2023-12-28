#!/bin/bash

docker run -v ~/coding/mypower/data_docker/postgresql:/var/lib/postgresql/data -ti arm32v7/postgres:11.1 /bin/su -c "/usr/lib/postgresql/11/bin/pg_resetwal -f /var/lib/postgresql/data" postgres


