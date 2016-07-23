# Chat App:
I have used flask-restful framework coupled with Mysql and rabbitmq. I have used pika client to make the message publish async.

## About:
  - User can signup and login and he will be by default subscribed to 'public' channel. 
  - User can publish and delete chat and can join, create unsubscribe channel.
  - Creation, Unsubscription and deletion are simple, a button is provided to do the same. However if you a trying to create a channel, that already exists, you will be automatically joined to that channel.


## Installation:
Installing supervisor : 

    sudo apt-get install supervisor
    sudo spt-get install rabbitmq-server


  1. Clone project from github, https://github.com/Rahul91/healthify 
  2. Create virtualenv, activate it and install requriement using pip from healthify/backend/requirements.txt
  3 .Change db config in healthify/backend/healthify/config.py and healthify/backend/system-config/dev/alembic.ini 
  4. Execute script in healthify/backend/migrate_db.sh
  5. Make changes in healthify/backend/system-config/dev/supervisor/* and create softlinks for healthify/backend/system-config/dev/supervisor in /etc/supervisor/conf.d
        
        $ sudo ln -s healthify/backend/system-config/dev/supervisor/healthify.conf .
        $ sudo ln -s healthify/backend/system-config/dev/supervisor/worker.conf .
        $ sudo supervisor reread
        $ sudo supervisor update

      Or python app.py  and  python worker.stream_fetch.py, Make sure to add PYTHONPATH upto ~/healthify/backend/
      
  6. Make nginx conf in /etc/nginx/sites-enabled and restart service
        
            $ sudo service restart nginx
    
Or go to /doc and use SimpleHTTPServer to host the files
        
            $ python -m SimpleHTTPServer 8989
    
This will host the apidoc on localhost:8989
    
  7. Backend stack is ready to serve the request now.
