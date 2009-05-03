from hackertalks.tests import *

class TestTalkController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='talk', action='index'))
        # Test response...
