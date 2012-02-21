

Installation:

pip install virtualenvwrapper

mkvirtualenv cltpy_chat

pip install sqlalchemy

pip install beaker

pip install flask

# Build all the database in /tmp (sorry windows didn't test)
 
python bootstrap.py

# Start the web server

python serv.py 

open http://localhost:5000/

# enter name and click login

# enter random text into send a couple times

# enter hipster in random text and see error rate go up

# ctrl-c server to stop it from running

# Run the replay command to see first error

python replay.py

# fix the code in handlers.handle_message

# Run replay again seeing no errors :)

python replay.py

# WOOT done

