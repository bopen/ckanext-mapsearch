import json
import pylons.config as config
import ckan.plugins as plugins
from ckan.lib.base import BaseController, request, c
from ckanext.spatial.lib import bbox_query, validate_bbox, get_srid

#import logging
#log = logging.getLogger(__name__)


class ViewController(BaseController):
    def show(self):
        c.solr_url = config['solr_url']
        return plugins.toolkit.render('blank_search_app.html')

    def text_complete(self):
        """must autocomplete take the map-extent in consideration?"""
        text_results, geo_results = self._do_query(request)
        #print "geo:", geo_results["results"]
        #print "text:", [r['id'] for r in text_results['results']]

        return json.dumps([r["title"] for r in text_results['results']
                                          if r['id'] in geo_results['results']])

    def query_datasets(self):
        """the full query returning datasets"""
        text_results, geo_results = self._do_query(request)
        return json.dumps([r for r in text_results['results']
                               if r['id'] in geo_results['results']])

    def _do_query(self, request):
        package_search = plugins.toolkit.get_action('package_search')
        #print request.params.keys()
        q = request.params["q"]
        srid = get_srid(request.params.get('crs')) if 'crs' in request.params else None
        extents = bbox_query(validate_bbox(request.params["bbox"]), srid)
        ids = [extent.package_id for extent in extents]
        geo_results = dict(count=len(ids), results=ids)
        q_string = "title:*{0}* OR notes:*{0}*".format(q)
        text_results = package_search(None, {'q': q_string})
        return text_results, geo_results
