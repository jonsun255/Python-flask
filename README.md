# Python-flask
A repository for database managmenet through Python

In this repository im using the world database as my example.

Im using Python flask and psycopg 3 to communicate with the database.

My app.py file contains all the functions for selecting, updating, inserting and deleting from python to the database.
My .env file contains the necessary information to communicate with the database. Such as ports, username, passwords etc.

Im using Postman to send and retrieve all the API commands from the Flask programme to the database.
The database communicates through localhost/127.0.0.1/5000.

To setup the python programme, you need to install psycopg and Flask.

To install flask, you can write this line in the command terminal in VScode:
**pip install Flask**
To install psycopg, you can write this line in the command terminal in VScode:
**pip install "psycopg[binary]" python-dotenv**

To run the program, just type: flask run --debug
in the command terminal, and you can see the output either through Postman or the 127.0.0.1/5000 url. 
