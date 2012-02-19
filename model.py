from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
def setup_engine(path='/tmp/cltpy_chat.db'):
    engine = create_engine('sqlite:%s' % path, echo=True)
    Session.configure(bind=engine)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
def build_tables():
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
    def save(clzz, n):
        event = Event()
        event.timestamp = n['timestamp']
        event.type = n['type']
        event.data = n['data']
        Session().add(event)
        return event





class UserSession(Base):
    __tablename__ = 'user_session'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    user_name = Column(String, unique=True, nullable=False)

    @classmethod
    def find_or_create(clzz, user_name):
        session = Session()
        us = session.query(UserSession).filter_by(user_name=user_name).first()
        if not us:
            us = UserSession()
            us.user_name = user_name
            session.add(us)
        return us 
    def add_event(self, e):
        event = Event.save(e)
        self.events.append(event)

    


