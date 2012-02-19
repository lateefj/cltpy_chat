from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)
def setup_engine(path='/tmp/cltpy_chat.db'):
    engine = create_engine('sqlite:%s' % path, echo=True)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
def build_tables():
    Base.metadata.create_all(engine) 


from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    type = Column(String)
    data = Column(String)


user_session_event = Table('user_session_event', Base.metadata, 
        Column('event_id', Integer, ForeignKey('event.id')),
        Column('user_session_id', Integer, ForeignKey('user_session.id'))
        )

class UserSession(Base):
    __tablename__ = 'user_session'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    user_name = Column(String, nullable=True)
    events = relationship('Event', secondary=user_session_event, backref='user_session')

    


