#!/bin/sh

cd /mypower
/usr/sbin/crond
/usr/local/bin/flask run --host=0.0.0.0
