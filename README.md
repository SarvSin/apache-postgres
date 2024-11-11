To run this, just execute docker-compose up --build

It should use the requirements file in the python-app directory to print out the message and put it in the correct database.



# FLAWS

- no separation between consumer and producer code. They could be refactored out to be a bit prettier

- lots of plaintext connections, they could be in a .env file 


