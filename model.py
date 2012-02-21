from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)

def setup_engine(path='/tmp/cltpy_chat.db'):
    global engine
    engine = create_engine('sqlite:///%s' % path, echo=True)
    Session.configure(bind=engine)
    session = Session()
session = None
def get_session():
    global session
    if session is None or not session:
        session = Session()
    return session

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
def build_tables():
    global engine
    Base.metadata.create_all(engine) 

from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref

user_session_event = Table('user_session_event', Base.metadata, 
        Column('event_id', Integer, ForeignKey('event.id')),
        Column('user_session_id', Integer, ForeignKey('user_session.id'))
        )

import json
class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    type = Column(String)
    json_data = Column(String)
    user_session = relationship('UserSession', secondary=user_session_event, 
            backref=backref('events', order_by=timestamp))
    
    def get_data(self):
        return json.loads(self.json_data)
    def set_data(self, d):
        self.json_data = json.dumps(d) 
    def del_data(self):
        self.json_data = None
    data = property(get_data, set_data, del_data, 'Property for jsonifying data')


    @classmethod
    def count(clzz):
        return get_session().query(Event).count()
    @classmethod
    def message_events(clzz):
        return get_session().query(Event).filter_by(Event.type == 'message')


    @classmethod
    def save(clzz, n):
        event = Event()
        event.timestamp = n['timestamp']
        event.type = n['type']
        event.data = n['data']
        get_session().add(event)
        get_session().commit()

        return event



class Error(Base):

    __tablename__ = 'error'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('user_session.id'))
    created = Column(DateTime, default=datetime.now())
    subject = Column(String)
    text = Column(String)
    json_data = Column(String)

    user_session = relationship('UserSession', backref=backref('errors', order_by=created))

    @classmethod
    def count(clzz):
        return get_session().query(Error).count()

    @classmethod
    def new(clzz, us_id, subject=None, text=None, data=None):
        e = Error()
        e.session_id = us_id
        e.subject = subject
        e.text = text
        e.data = data
        session = get_session()
        session.add(e)
        session.commit()
        return e
    def get_data(self):
        return json.loads(self.json_data)
    def set_data(self, d):
        self.json_data = json.dumps(d) 
    def del_data(self):
        self.json_data = None
    data = property(get_data, set_data, del_data, 'Property for jsonifying data')



class UserSession(Base):
    __tablename__ = 'user_session'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    user_name = Column(String, unique=True, nullable=False)
    
    @classmethod
    def by_id(clzz, id):
        session = get_session()
        return session.query(UserSession).filter_by(id=id).first()
    @classmethod
    def find_or_create(clzz, user_name):
        session = get_session()
        us = session.query(UserSession).filter_by(user_name=user_name)
        if not us or not us.first():
            us = UserSession()
            us.user_name = user_name
            session.add(us)
            session.commit()
        else:
            us = us.first()
        return us 
    def add_event(self, e):
        event = Event.save(e)
        self.events.append(event)


    


