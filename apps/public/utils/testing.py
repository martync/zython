import json
import time
from datetime import datetime
from subprocess import call


def show_in_browser(response):
    """
    Write the response content into a temporary HTML file and
    open it into your default browser.

    > client = Client()
    > response = client.get('/some/page/')
    > show_in_browser(response)

    """
    file_path = '/tmp/django_test_show_in_browser_%s.html' % datetime.now().strftime('%Y%m%d%H%M%S')
    f = open(file_path, 'w')
    f.write('%s\n' % response.content)
    call(["open", file_path])
    time.sleep(5)
    call(["rm", file_path])


class AjaxCallsTestCaseBase(object):

    def is_ajax_response_correct(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers["content-type"], ('Content-Type', 'application/json'))
        json_response = json.loads(response.content)
        self.assertEqual(json_response["status"], "ok")

    def ajax_post_kwargs(self):
        return {"HTTP_X_REQUESTED_WITH": 'XMLHttpRequest'}
