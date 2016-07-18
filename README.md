# healthify

<h2>Problem Statement</h2>
Anyone visiting the website should be asked for login/signup.
Once logged in, they should join a public channel where all users can send messages.
Messages sent by one person should be received by all the other users who are currently logged into the public channel. And this messaging should be realtime.
There should be an option for the user to clear chat, which should only clear the chat for that user, others should still be able to see all the messages.
Any new feature that you can think of in addition to the above requirements. Document this in README when you are submitting.

<h2>My approach</h2>

Technological Stack:
		
		1. Flask(Flask-Restful) + MySql(db) + sqlAlchemy(ORM) + Alembic(DB Migration) 
		2. Angularjs(Js) + Bootstrap(CSS)
		3.  RabbitMq (broker) + Pika (MessagingClient)
		4. Apidoc(Documentation) 
	 


<h2>Project Setup</h2>
  1. Clone project from github, https://github.com/Rahul91/healthify 
  2. Create virtualenv, activate it and install requriement using pip from healthify/backend/requirements.txt
  3 .Change db config in healthify/backend/healthify/config.py and healthify/backend/healthify/models/alembic/alembic.ini 
  4. Execute script in healthify/backend/migrate_db.sh
  5. Now run the healthify/backend/app.py
  6.Do npm install in healthify/frontend, make sure you have package.json in your current directory
  7. Change constant in healthify/frontend/src/mainApp.js to point to your flask api
