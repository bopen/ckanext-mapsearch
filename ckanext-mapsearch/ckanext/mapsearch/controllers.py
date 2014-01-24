from re import findall
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
        return json.dumps([r["title"] for r in text_results['results']
                                          if r['id'] in geo_results['results']])


    # TODO: decide if autocomplete directly to SOLR is feasible or if we have to reanimate
    # the following method
    # NB: this method is not used, remove it when at the end of the development
    # there is still no need to do autocomplete from here
    def _do_query(self, request):
        package_search = plugins.toolkit.get_action('package_search')
        #print request.params.keys()
        q = request.params["q"]
        rows = request.params["rows"]
        srid = get_srid(request.params.get('crs')) if 'crs' in request.params else None
        extents = bbox_query(validate_bbox(request.params["bbox"]), srid)
        ids = [extent.package_id for extent in extents]
        geo_results = dict(count=len(ids), results=ids)
        if len(findall("(tags|res_format|title|notes)*:.+", q)) > 0:
            q_string = q
        else:
            q_string = "text:*{0}*".format(q)
        text_results = package_search(None, {'q': q_string, 'rows': rows})
        return text_results, geo_results
