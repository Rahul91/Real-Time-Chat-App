# Chat App:
An app build on top of flask-restful framework coupled with Mysql and rabbitmq. I have used pika client to make the message publish async.

## Architecture:
The overall services are divided into 2 parts:
  - Api Layer
  - Business Layer
  
  1. Api layer: This layer is responsible for taking requests, parsing them, validating request parameters, exception handling, db commits and rollbacks and returning marshalled responses. This layer itself is just an entry and exit point for the entire application. Also, this is the exposed service to the world, any data, logic are not binded to this layer.
  
  2. Business layer: Bunisess logic, DB operations, calling other services etc are the part of Business layer. These services are accessible only via api layer, thus making them secure, also, while authentcation could be a part of api layer, authorization could be part of business layer. Althoug this applicaiton does not have any role/permission, but this layer would be the perfect place to implement this.
  
~~Async approach: I have used Rabbitmq and pika client to make the chat publish aysnc, why async, because its better. Altough in my case, the async call is not doing much, just a DB write, but large application can really use this approacg to increase the throughput and can increase concurrunt requests.~~

Async approach: [RabbitMq (broker) + Pika (MessagingClient)] This  approach was dropped because of the extra overhead of rabbitmq and pika, Also it increase your point of failures. In our case, async worker was not much but an DB write, so I have moved the async part and made the db call synchronous.

## About/Expexted Behaviour:
  - User can signup and login and he will be by default subscribed to 'public' channel. 
  - User can publish and delete chat and can join, create unsubscribe channel.
  - User can unsubscribe any channel, expect for Public channel.
  - User can delete chat for any channel, however any conversation after deletion will be displayed in the feed.
  - Creation, Unsubscription and deletion are simple, a button is provided to do the same. However if you a trying to create a channel, that already exists, you will be automatically joined to that channel.
  - New feature for inviting user has been added, once an invitation is sent, requested user can see the request for approval(checkout invite_feature branch for this feature). If the requested user has not yet signed-up, he will get the invitation, once signed-in. Please note that you are sending invitation to join a particular channel, and the requested user will join that channel only, if he opts to. Type of channel doesnot matter here.
  - You can join a public channel by creating it, but if the channel you want to join is Private, then the owner of that channel gets an request for approval, once approved, you will be joined to that channel. (checkout invite_feature branch)


## Installation/Project setup:
Installing supervisor : 

    sudo apt-get install supervisor
    sudo apt-get install rabbitmq-server


  1. Clone project from github, https://github.com/Rahul91/healthify and checkout invite_feature branch.
  2. Create virtualenv, activate it and install requriement using pip from healthify/backend/requirements.txt
  3 .Change db config in healthify/backend/healthify/config.py and healthify/backend/system-config/dev/alembic.ini 
  4. Execute script in healthify/backend/migrate_db.sh fot DB migration, make sure you have PYTHONPATH corrrect i.e upto ~/healthify/backend/
  5. Make changes in healthify/backend/system-config/dev/supervisor/* and create softlinks for healthify/backend/system-config/dev/supervisor in /etc/supervisor/conf.d
        
        sudo ln -s healthify/backend/system-config/dev/supervisor/healthify.conf .
        sudo supervisor reread
        sudo supervisor update

      Or python app.py  and  ~~python worker.stream_fetch.py~~, Make sure to add PYTHONPATH upto ~/healthify/backend/
      
  6. Make nginx conf in /etc/nginx/sites-enabled and restart service
        
            $ sudo service restart nginx
    
Or go to /doc and use SimpleHTTPServer to host the files
        
            $ python -m SimpleHTTPServer 8989
    
This will host the apidoc on localhost:8989
    
  7. Backend stack is ready to serve the request now.
