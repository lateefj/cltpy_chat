from datetime import datetime

import unittest


import model
model.build_tables() # Build in memory tables ;)

class TestEvent(unittest.TestCase):

    def test_create(self):
        n = {'type': 'test_create', 'timestamp':datetime.now(), 'data':{'foo':'yo', 'bar':'dude'}}
        e = model.Event.save(n)
        assert e.type == n['type']
        assert e.timestamp == n['timestamp']
        assert e.data['foo'] == n['data']['foo']


class TestSession(unittest.TestCase):

    def test_create(self):
        user_name = 'foo'
        us = model.UserSession.find_or_create(user_name)

        us2 = model.UserSession.find_or_create(user_name)
        assert us.id == us2.id
        n = {'type': 'test_create', 'timestamp':datetime.now(), 'data':{'foo':'yo', 'bar':'dude'}}
        us.add_event(e)

        us3 = model.UserSession.find_or_create(user_name)
        assert us3.events
        assert us3.events[0]['type'] == 'test_create'






