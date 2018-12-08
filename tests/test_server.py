# -*- coding: utf-8 -*-

"""

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import requests
import unittest
import timeit

URL = 'http://localhost:3000'

def withcallback(params):
    callback = 'callback'
    if 'callback' in params:
        callback = params['callback']
    return "%s(%s);" % (callback, params['jsonp'])

class ServerTestCase(unittest.TestCase):

    def test_html(self):
        param_list = [
            {
                'html': 'blah blah',
            },
            {
                'html': 'blah blah',
                'delay': 0,
            },
            {
                'html': 'blah blah',
                'delay': 1,
            },
        ]
        for params in param_list:
            response = requests.post("%s/%s" % (URL, "echo/html"), data=params)
            self.assertEqual(response.headers['content-type'], 'text/html')
            self.assertEqual(response.content.decode(), params['html'])
        params = {
            'html': 'blah blah',
            'delay': 1,
        }
        start_time = timeit.default_timer()
        response = requests.post("%s/%s" % (URL, "echo/html"), data=params)
        elapsed = timeit.default_timer() - start_time
        self.assertLess(params['delay'], elapsed)

    def test_jsonp(self):
        param_list = [
            {
                'jsonp': 'blah blah',
                'callback': 'callback',
            },
            {
                'jsonp': 'blah blah',
                'delay': 0,
            },
            {
                'jsonp': 'blah blah',
                'callback': '_callback',
                'delay': 1,
            },
        ]
        for params in param_list:
            response = requests.get("%s/%s" % (URL, "echo/jsonp"), params=params)
            self.assertEqual(response.headers['content-type'], 'application/javascript')
            self.assertEqual(response.content.decode(), withcallback(params))
        params = {
            'jsonp': 'blah blah',
            'delay': 1,
        }
        start_time = timeit.default_timer()
        response = requests.get("%s/%s" % (URL, "echo/jsonp"), params=params)
        elapsed = timeit.default_timer() - start_time
        self.assertLess(params['delay'], elapsed)

    def test_html(self):
        param_list = [
            {
                'json': 'blah blah',
            },
            {
                'json': 'blah blah',
                'delay': 0,
            },
            {
                'json': 'blah blah',
                'delay': 1,
            },
        ]
        for params in param_list:
            response = requests.post("%s/%s" % (URL, "echo/json"), data=params)
            self.assertEqual(response.headers['content-type'], 'application/json')
            self.assertEqual(response.content.decode(), params['json'])
        params = {
            'json': 'blah blah',
            'delay': 1,
        }
        start_time = timeit.default_timer()
        response = requests.post("%s/%s" % (URL, "echo/json"), data=params)
        elapsed = timeit.default_timer() - start_time
        self.assertLess(params['delay'], elapsed)

    def test_xml(self):
        param_list = [
            {
                'xml': 'blah blah',
            },
            {
                'xml': 'blah blah',
                'delay': 0,
            },
            {
                'xml': 'blah blah',
                'delay': 1,
            },
        ]
        for params in param_list:
            response = requests.post("%s/%s" % (URL, "echo/xml"), data=params)
            self.assertEqual(response.headers['content-type'], 'text/xml')
            self.assertEqual(response.content.decode(), params['xml'])
        params = {
            'xml': 'blah blah',
            'delay': 1,
        }
        start_time = timeit.default_timer()
        response = requests.post("%s/%s" % (URL, "echo/xml"), data=params)
        elapsed = timeit.default_timer() - start_time
        self.assertLess(params['delay'], elapsed)

    def test_js(self):
        param_list = [
            {
                'js': 'blah blah',
            },
            {
                'js': 'blah blah',
                'delay': 0,
            },
            {
                'js': 'blah blah',
                'delay': 1,
            },
        ]
        for params in param_list:
            response = requests.get("%s/%s" % (URL, "echo/js"), params=params)
            self.assertEqual(response.headers['content-type'], 'application/javascript')
            self.assertEqual(response.content.decode(), params['js'])
        params = {
            'js': 'blah blah',
            'delay': 1,
        }
        start_time = timeit.default_timer()
        response = requests.get("%s/%s" % (URL, "echo/js"), params=params)
        elapsed = timeit.default_timer() - start_time
        self.assertLess(params['delay'], elapsed)

    def test_echo(self):
        delay = 1

        start_time = timeit.default_timer()
        response = requests.get("%s/%s?delay=%d" % (URL, "echo", delay))
        elapsed = timeit.default_timer() - start_time
        self.assertLess(delay, elapsed)

        start_time = timeit.default_timer()
        response = requests.post("%s/%s?delay=%d" % (URL, "echo", delay))
        elapsed = timeit.default_timer() - start_time
        self.assertLess(delay, elapsed)

        body = "blah blah"
        response = requests.post("%s/%s" % (URL, "echo"), data=body)
        self.assertEqual(response.content.decode(), body)

        # test content-type header

        body = "blah blah"
        headers = {'Content-Type': 'application/json'}
        response = requests.post("%s/%s" % (URL, "echo"), data=body, headers=headers)
        self.assertEqual(response.headers['content-type'], headers['Content-Type'])
