# Chat App:
An app build on top of flask-restful framework coupled with Mysql and rabbitmq. I have used pika client to make the message publish async.

## Architecture:
The overall services are divided into 2 parts:
  - Api Layer
  - Business Layer
  
  1. Api layer: This layer is responsible for taking requests, parsing them, validating request parameters, exception handling, db commits and rollbacks and returning marshalled responses. This layer itself is just an entry and exit point for the entire application. Also, this is the exposed service to the world, any data, logic are not binded to this layer.
  
  2. Business layer: Bunisess logic, DB operations, calling other services etc are the part of Business layer. These services are accessible only via api layer, thus making them secure, also, while authentcation could be a part of api layer while authorization could be part of business layer. Althoug this applicaiton does not have any role/permission, but this layer would be the perfect place to implement this.
  
Async approach: I have used Rabbitmq and pika client to make the chat publish aysnc, why async, because its better. Altough in my case, the async call is not doing much, just a DB write, but large application can really use this technique to increase the throughput and can increase concurrnet requests.

## About:
  - User can signup and login and he will be by default subscribed to 'public' channel. 
  - User can publish and delete chat and can join, create unsubscribe channel.
  - Creation, Unsubscription and deletion are simple, a button is provided to do the same. However if you a trying to create a channel, that already exists, you will be automatically joined to that channel.


## Installation/Project setup:
Installing supervisor : 

    sudo apt-get install supervisor
    sudo spt-get install rabbitmq-server


  1. Clone project from github, https://github.com/Rahul91/healthify 
  2. Create virtualenv, activate it and install requriement using pip from healthify/backend/requirements.txt
  3 .Change db config in healthify/backend/healthify/config.py and healthify/backend/system-config/dev/alembic.ini 
  4. Execute script in healthify/backend/migrate_db.sh
  5. Make changes in healthify/backend/system-config/dev/supervisor/* and create softlinks for healthify/backend/system-config/dev/supervisor in /etc/supervisor/conf.d
        
        sudo ln -s healthify/backend/system-config/dev/supervisor/healthify.conf .
        sudo ln -s healthify/backend/system-config/dev/supervisor/worker.conf .
        sudo supervisor reread
        sudo supervisor update

      Or python app.py  and  python worker.stream_fetch.py, Make sure to add PYTHONPATH upto ~/healthify/backend/
      
  6. Make nginx conf in /etc/nginx/sites-enabled and restart service
        
            $ sudo service restart nginx
    
Or go to /doc and use SimpleHTTPServer to host the files
        
            $ python -m SimpleHTTPServer 8989
    
This will host the apidoc on localhost:8989
    
  7. Backend stack is ready to serve the request now.
