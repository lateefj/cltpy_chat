from datetime import datetime

import unittest

import model
model.build_tables()

import handlers
class TestMessageHandler(unittest.TestCase):

    def test_message(self):
        handlers.handle_message({'data':{'text':'it all good man'}})
        try:
            handlers.handle_message({'data':{'text':'why whould I say hipster?'}})
            assert False, 'Exception you now say hipster'
        except:
            pass

class TestHandleErrorCount(unittest.TestCase):

    def test_error_count(self):
        us = model.UserSession.find_or_create('test_foo')
        us.add_event({'type':'message', 'timestamp':datetime.now(), 'data':{'text':'hipster I am'}})
        model.Error.new(us.id, subject='Test Python Error', text='testing error')
        assert us.errors
        
