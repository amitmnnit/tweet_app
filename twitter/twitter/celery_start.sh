#!/bin/bash
ENV  = $ENV1
NAME="twitter_celery"                                  # Name of the application
DJANGODIR=$(pwd)             # Django project directory

USER=$(whoami)                                      # the user to run as
GROUP=$(whoami)                                      # the group to run as

NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn
LOGFILE=celery.log

echo "Starting $NAME celery"
 
cd $DJANGODIR

PARENTDIR="$(dirname "$DJANGODIR")"

source ${PARENTDIR%%/}/venv/bin/activate

export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export PYTHON_EGG_CACHE=/home/${USER%%/}/.python-egg-cache

exec python manage.py celeryd_multi start  3 -Q:1 web -Q:2 web -Q:3 web -P eventlet -c 200 --loglevel=INFO --logfile=$LOGFILE