### Micro-Blogging App similar to Twitter which has some following features. ###
* Login/SignUp
* User can follow many other users.
* User can see real time Tweets made by those whom he is following.
* User can tweet which will be posted on all followers wall in real time.
* User can check all tweets done by him.

# How do I get set up #
#Server side
* cd /path/to/tweet_app
* virtualenv env
* source env/bin/activate
* pip install -r requirements.txt

* cd /path/to/tweet_app/twitter
* python manage.py syncdb
* python manage.py migrate

* sh twitter/celery_start.sh   #runs celery workers
* python manage.py runserver   #runs servers

### To Stop celery workers: ###
* ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
* rm celery1.pid celery2.pid celery3.pid

### To Start celery workers: ###
* sh twitter/celery_start.sh

### To check open port for 8000 ###
* sudo netstat -lnp | grep 8000

#Client side
* visit http://127.0.0.1:8000/
* signup for some users
* follow other users
* tweet
* you will get tweet on your wall as soon some followed user tweets
