#!/bin/bash
docker exec -ti -e PGPASSWORD=passwdb  `docker ps | grep postgres | cut -d ' ' -f1` /usr/bin/psql -U userdb consumption
