#!/bin/bash
docker exec -ti -e PGPASSWORD=passwdb  `docker ps | grep db | cut -d ' ' -f1` psql -U userdb consumption
