from unittest import TestCase

import os
import types
import datetime
import time

from bitter import utils
from bitter.crawlers import TwitterQueue, TwitterWorker
from bitter import config as c

class TestUtils(TestCase):

    def setUp(self):
        self.wq = TwitterQueue.from_credentials(os.path.join(os.path.dirname(__file__), 'credentials.json'))

    def test_create_worker(self):
        assert len(self.wq.queue)==1

    def test_get_limits(self):
        w1 = list(self.wq.queue)[0]
        print(w1.limits)
        limitslook = w1.get_limit(['statuses', 'lookup'])
        assert limitslook['remaining'] == limitslook['limit']

    def test_set_limits(self):
        w1 = list(self.wq.queue)[0]
        w1.set_limit(['test', 'test2'], {'remaining': 0})
        assert w1.get_limit(['test', 'test2']) == {'remaining': 0}

    def test_await(self):
        w1 = list(self.wq.queue)[0]
        w1.set_limit(['test', 'wait'], {'remaining': 0, 'reset': time.time()+2})
        assert w1.get_wait(['test', 'wait']) > 1
        time.sleep(2)
        assert w1.get_wait(['test', 'wait']) == 0
        assert w1.get_wait(['statuses', 'lookup']) == 0

    def test_is_limited(self):
        w1 = list(self.wq.queue)[0]
        assert not w1.is_limited(['statuses', 'lookup'])

    def test_call(self):
        w1 = list(self.wq.queue)[0]
        l1 = w1.get_limit(['users', 'lookup'])
        resp = self.wq.users.lookup(screen_name='balkian')
        l2 = w1.get_limit(['users', 'lookup'])
        assert l1['remaining']-l2['remaining'] == 1
