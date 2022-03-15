# -*- coding: utf-8 -*-
import logging
from django.test.runner import DiscoverRunner


class ZythonTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        logging.basicConfig(level=logging.WARNING)

        if not test_labels:
            test_labels = ['brew', 'stocks']
        return super(ZythonTestRunner, self).run_tests(test_labels, extra_tests, **kwargs)
