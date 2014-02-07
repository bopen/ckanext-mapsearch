import json

import pylons.config as config
import ckan.plugins as plugins
from ckan.lib.base import BaseController, request, c
from ckan.lib.search.common import make_connection
from solr import SearchHandler

import logging

log = logging.getLogger(__name__)


class ViewController(BaseController):
    def show(self):
        c.solr_url = config['solr_url']
        c.initial_map_extent = config.get(
            'ckanext.mapsearch.initial_map_extent', "false")
        return plugins.toolkit.render('blank_search_app.html')

    def textcomplete(self):
        """proxies an textcomplete query to the solr suggest search-handler"""

        # TODO: must autocomplete take the map-extent in consideration?
        conn = make_connection()
        suggest = SearchHandler(conn, '/suggest')
        q = request.params["q"]
        res = suggest(q=q, wt='json')
        if q in res.spellcheck['suggestions'].keys():
            payload = res.spellcheck['suggestions'][q]['suggestion']
        else:
            payload = []
        return json.dumps(payload)
