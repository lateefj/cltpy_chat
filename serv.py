import random
import json
from datetime import datetime

from beaker.middleware import SessionMiddleware

import flask
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import model
model.setup_engine()
import handlers
############################# CATCH ALL ERROR HANDLER ###########################
import traceback
from StringIO import StringIO
@app.errorhandler(Exception)
def defualt_error_handler(errr):
    """
    This could be any framework it doesn't matter flask just happend to be quick 
    the point is to store errors for the future debugging.
    """
    s = StringIO()
    traceback.print_exc(file=s)
    text = s.getvalue()
    print(text)
    us = get_user_session()
    model.Error.new(us.id, subject='Python Error', text=text)



################ Recieve and store all events ##################################
@app.route('/s', methods=['POST'])
def send():
    """
    Assuming this is the central portal for all application event that must pass
    though here. This way every event can be replayed if something happens
    """
    event = request.form['event']
    if event:
        event = json.loads(event)
        # Parse timstamp from javascript
        event['timestamp'] = datetime.fromtimestamp(float(event['timestamp'])/1000.0)
        us = get_user_session()
        if us is not None:
            us.add_event(event)
        else:
            model.Event.save(event)
        r = handlers.publish(event)
        if r: 
            return jsonify(r)
    return jsonify({'success':True})

########################### NOTHING TO SEEE HERE REALLY!! ########################


def get_user():
    session = request.environ['beaker.session']
    if session.has_key('user_name'):
        return session['user_name']
    return None
def set_user(un):
    us = model.UserSession.find_or_create(un)
    session = request.environ['beaker.session']
    session['user_name'] = un
    session['sid'] = us.id

def get_user_session():
    session = request.environ['beaker.session']
    return model.UserSession.by_id(session['sid'])



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat')
def chat():
    un = get_user()
    print('username is form session %s' % un)
    return render_template('chat.html')

@app.route('/l/<user_name>')
def login(user_name):
    set_user(user_name)
    return jsonify({'success':True})

@app.route('/u')
def user():
    un = request.args.get('user_name')
    session = request.environ['beaker.session']
    session['user_name'] = un
    session.save()
    return jsonify({'success':True})

@app.route('/q')
def get_user():
    session = request.environ['beaker.session']
    un = session['user_name']
    return jsonify({'user_name':un})

@app.route('/err')
def error():
    event = request.form['event']
    if event:
        event = json.loads(event)
        us = get_user_session()
        model.Error.new(us.id, subject='Javscript Error', text=event['text'])

    return jsonify({'success':True})


def start_server():
    session_opts = {
            'session.auto': True,
            'session.data_dir':'/tmp/session/data',
            'session.lock_dir':'/tmp/sesssion/lock',
            'session.key': 'cltpy',
            'session.secret':'oooh_big_secret'
            }
    app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
    app.run(debug=True)

if __name__ == "__main__":
    start_server()



