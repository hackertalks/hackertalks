from hackertalks.tests import *

class TestSpeakerController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='speaker', action='index'))
        # Test response...
