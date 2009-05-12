from hackertalks.tests import *

class TestTalkController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='talk', action='index'))
        assert response.status == '200 OK'
    def test_display(self):
        response = self.app.get(url(controller='talk', action='display', id=1), status=200)
        assert response.status == '200 OK'
        response = self.app.get(url(controller='talk', action='display', id=9), status=404)
        assert response.status == '404 Not Found'
        response = self.app.get(url(controller='talk', action='display', id='foo'), status=400)
        assert response.status == '400 Bad Request'