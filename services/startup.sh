#!/bin/bash

mkdir /var/log/supervisord/

mkdir /tmp/logs/covid-19-tracker/

export FLASK_APP=app.py

# execute Supervisor to launch the wsgi app with gunicorn
exec /usr/local/bin/supervisord -c /etc/supervisor/supervisord.conf
