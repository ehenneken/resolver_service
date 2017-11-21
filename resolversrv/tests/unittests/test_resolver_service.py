# -*- coding: utf-8 -*-

import sys
import os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(PROJECT_HOME)

from flask_testing import TestCase
import unittest

import resolversrv.app as app
from resolversrv.views import LinkRequest

class TestResolver(TestCase):
    def create_app(self):
        self.current_app = app.create_app()
        return self.current_app

    # the following four types' links are created on the fly
    def test_fetchingAbstract(self):
        response = LinkRequest('1987gady.book.....B', 'ABSTRACT', self.current_app.config['RESOLVER_GATEWAY_URL_TEST']).process_request()
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.response[0], '/resolver/1987gady.book.....B/ABSTRACT/https://ui.adsabs.harvard.edu/#abs/1987gady.book.....B/abstract')
    def test_fetchingCitations(self):
        response = LinkRequest('1987gady.book.....B', 'CITATIONS', self.current_app.config['RESOLVER_GATEWAY_URL_TEST']).process_request()
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.response[0], '/resolver/1987gady.book.....B/CITATIONS/https://ui.adsabs.harvard.edu/#abs/1987gady.book.....B/citations')
    def test_fetchingCoRead(self):
        response = LinkRequest('1987gady.book.....B', 'COREADS', self.current_app.config['RESOLVER_GATEWAY_URL_TEST']).process_request()
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.response[0], '/resolver/1987gady.book.....B/COREADS/https://ui.adsabs.harvard.edu/#abs/1987gady.book.....B/coreads')
    def test_fetchingReferences(self):
        response = LinkRequest('1998ARA&A..36..189K', 'REFERENCES', self.current_app.config['RESOLVER_GATEWAY_URL_TEST']).process_request()
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.response[0], '/resolver/1998ARA&A..36..189K/REFERENCES/https://ui.adsabs.harvard.edu/#abs/1998ARA&A..36..189K/references')


    # the following three tests support of legacy type EJOURNAL
    def test_fetchingEJOURNAL(self):
        link_request = LinkRequest('1668RSPT....3..863M', 'EJOURNAL', self.current_app.config['RESOLVER_GATEWAY_URL_TEST'])
        self.assertEqual(link_request.link_type, 'ARTICLE')
        self.assertEqual(link_request.link_sub_type, 'PUB_HTML')
    def test_fetchingPreprint(self):
        link_request = LinkRequest('1991hep.th...10030D', 'PREPRINT', self.current_app.config['RESOLVER_GATEWAY_URL_TEST'])
        self.assertEqual(link_request.link_type, 'ARTICLE')
        self.assertEqual(link_request.link_sub_type, 'EPRINT_HTML')
    def test_fetchingGIF(self):
        link_request = LinkRequest('1990ARA&A..28..215D', 'GIF', self.current_app.config['RESOLVER_GATEWAY_URL_TEST'])
        self.assertEqual(link_request.link_type, 'ARTICLE')
        self.assertEqual(link_request.link_sub_type, 'ADS_SCAN')


    def test_route(self):
        """
        Tests for the existence of a /v1/resolver route, and that it returns
        properly formatted JSON data
        """
        r = self.client.get('/v1/resolver/1987gady.book.....B/ABSTRACT')
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
  unittest.main()