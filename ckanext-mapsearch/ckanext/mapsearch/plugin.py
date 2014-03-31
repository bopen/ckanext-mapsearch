from logging import getLogger

from shapely.geometry import asShape, polygon
from pylons import config
import ckan.plugins as plugins
from ckan.lib.helpers import json
from ckan.lib.base import request
from ckanext.spatial.lib import validate_bbox

log = getLogger(__name__)


def clip_bbox(bbox):
    return {'minx': max(-180, bbox['minx']),
            'miny': max(-90, bbox['miny']),
            'maxx': min(180, bbox['maxx']),
            'maxy': min(90, bbox['maxy'])}


class MapsearchPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    exclude_upper_bound = float(
        config.get('ckanext.mapsearch.exclude_upper_bound', 0.02))
    display_upper_bound = float(
        config.get('ckanext.mapsearch.display_upper_bound', 1.0))
    display_lower_bound = float(
        config.get('ckanext.mapsearch.display_lower_bound', 50))
    exclude_lower_bound = float(
        config.get('ckanext.mapsearch.exclude_lower_bound', 2500))
    # intersecting areas count as relevant if they are completely inside an
    # extended bbox.
    # this multiplier defines the extent:
    # 1 => 4 times bigger
    # 2 => 9 times bigger
    # 3 => 16 times
    # (i.e. (n + 1) ** 2)
    buffer_mult = 2

    ## IConfigurer
    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_public_directory(config, 'public')
        plugins.toolkit.add_resource('fanstatic', 'mapsearch_js')

    ## IRoutes
    def before_map(self, map):
        controller = 'ckanext.mapsearch.controllers:ViewController'
        map.connect('map_viewer', '/mapsearch',
                    controller=controller, action='show')
        map.connect('textcomplete', '/mapsearch/textcomplete',
                    controller=controller, action='textcomplete')
        return map

    def before_search(self, search_params):
        """overwrites the search parameters of the spatial extension

        we support only solr and solr-spatial-field backends.
        """
        # we treat only our own requests:
        if not request.referer or \
           not "/" in request.referer or \
           not request.referer.split("/")[-1] == 'mapsearch':
            return search_params
        # only requests with bbox
        if 'ext_bbox' not in search_params['extras'].keys():
            return search_params
        backend = config.get('ckanext.spatial.search_backend', 0)
        supported_backends = ['solr', 'solr-spatial-field']
        if not backend in supported_backends:
            raise RuntimeError('{0} is not implemented. '.format(backend) +
                               'This extension needs one of ' +
                               '{0} as the search backend'.format(
                                   supported_backends))
        scale = search_params['extras'].get('ext_scale', 'normal')
        # solr-spatial-field backend requires clipped coordinates
        raw_bbox = search_params['extras'].get('ext_bbox')
        bbox = clip_bbox(validate_bbox(raw_bbox))
        if backend == 'solr-spatial-field':
            search_params = self._params_for_solr_spatial_field_search(
                bbox, search_params, scale)
        elif backend == 'solr':
            search_params = self._params_for_solr_search(
                bbox, search_params, scale)
        return search_params

    def _params_for_solr_search(self, bbox, search_params, scale):
        area_search = (abs(bbox['maxx'] - bbox['minx']) *
                       abs(bbox['maxy'] - bbox['miny']))
        area_string = 'div(%s,mul(sub(maxy,miny),sub(maxx,minx)))' % area_search
        scale_dict = {
            'too_small': ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                          '{!frange incl=false l=%f}%s' %
                          (self.exclude_lower_bound, area_string)],
            'small': ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                      '{!frange incl=true l=%f u=%f}%s' %
                      (self.display_lower_bound, self.exclude_lower_bound,
                       area_string)],
            'normal': ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                       '{!frange incl=true l=%f u=%f}%s' %
                       (self.display_upper_bound, self.display_lower_bound,
                        area_string)],
            'big': ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                    '{!frange incl=true l=%f u=%f}%s' %
                    (self.exclude_upper_bound, self.display_upper_bound,
                     area_string)],
            'too_big': ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                        '{!frange incl=false u=%f}%s' %
                        (self.exclude_upper_bound, area_string)],
        }
        search_params['fq_list'] = scale_dict[scale]
        return search_params

    def _params_for_solr_spatial_field_search(self, bbox,
                                              search_params, scale):
        search_params['fq_list'] = []
        scale_bool_dict = {
            'too_small': '+spatial_geom:"IsWithin({minx} {miny} {maxx} {maxy})"',
            'small': '+spatial_geom:"IsWithin({minx} {miny} {maxx} {maxy})"',
            'normal': '+spatial_geom:"Intersects({minx} {miny} {maxx} {maxy})"',
            'big': '+spatial_geom:"Intersects({minx} {miny} {maxx} {maxy})"',
            'too_big': '+spatial_geom:"Contains({minx} {miny} {maxx} {maxy})"'
        }
        search_area = abs(bbox['maxx'] - bbox['minx']) * \
            abs(bbox['maxy'] - bbox['miny'])
        area_prop_string = "div({0},spatial_area)".format(search_area)
        scale_prop_dict = {
            'too_small': '{!frange incl=false l=%f}%s' %
            (self.exclude_lower_bound, area_prop_string),

            'small':  '{!frange incl=false l=%f u=%f}%s' %
            (self.display_lower_bound, self.exclude_lower_bound,
                area_prop_string),

            'normal': '{!frange incl=false l=%f u=%f}%s' %
            (self.display_upper_bound, self.display_lower_bound,
                area_prop_string),

            'big':  '{!frange incl=false l=%f u=%f}%s' %
            (self.exclude_upper_bound, self.display_upper_bound,
                area_prop_string),

            'too_big':  '{!frange incl=false u=%f}%s' %
            (self.exclude_upper_bound, area_prop_string)
        }

        search_params['fq_list'].append(scale_bool_dict[scale].format(
            minx=bbox['minx'], miny=bbox['miny'],
            maxx=bbox['maxx'], maxy=bbox['maxy']))
        search_params['fq_list'].append(scale_prop_dict[scale])
        if scale == 'normal':
            width_buffer = (bbox['maxx'] - bbox['minx']) * \
                self.buffer_mult * 0.5
            height_buffer = (bbox['maxy'] - bbox['miny']) * \
                self.buffer_mult * 0.5
            extended_bbox = {'minx': bbox['minx'] - width_buffer,
                             'miny': bbox['miny'] - height_buffer,
                             'maxx': bbox['maxx'] + width_buffer,
                             'maxy': bbox['maxy'] + height_buffer}
            cbbox = clip_bbox(extended_bbox)
            filter_str = '+spatial_geom:"IsWithin({minx} {miny} {maxx} {maxy})"'
            search_params['fq_list'].append(filter_str.format(
                minx=cbbox['minx'], miny=cbbox['miny'],
                maxx=cbbox['maxx'], maxy=cbbox['maxy']))
        return search_params

    def before_index(self, pkg_dict):
        """sets the area of a polygon for the *solr-spatial-field* backend"""
        log.debug('mapsearch index: new dataset')
        backend = config.get('ckanext.spatial.search_backend', 0)
        if pkg_dict.get('extras_spatial', None) and \
           backend == 'solr-spatial-field':
            try:
                geometry = json.loads(pkg_dict['extras_spatial'])
            except ValueError, e:
                msg = 'Geometry not valid GeoJSON, not indexing: {0}'.format(e)
                log.error(msg)
                return pkg_dict
            area = None

            # Check potential problems with bboxes
            if geometry['type'] == 'Polygon' \
               and len(geometry['coordinates']) == 1 \
               and len(geometry['coordinates'][0]) == 5:

                # Check wrong bboxes (4 same points)
                xs = [p[0] for p in geometry['coordinates'][0]]
                ys = [p[1] for p in geometry['coordinates'][0]]

                if xs.count(xs[0]) == 5 and ys.count(ys[0]) == 5:
                    # is a point: no area
                    return pkg_dict
                else:
                    # Check if coordinates are defined counter-clockwise,
                    # otherwise we'll get wrong results from Solr
                    lr = polygon.LinearRing(geometry['coordinates'][0])
                    if not lr.is_ccw:
                        lr.coords = list(lr.coords)[::-1]
                    poly = polygon.Polygon(lr)
                    area = poly.area

            if not area:
                shape = asShape(geometry)
                if not shape.is_valid:
                    log.error('Invalid geometry, not indexing')
                    return pkg_dict
                area = shape.area

            log.debug("area: {0}".format(area))
            pkg_dict['spatial_area'] = area
        return pkg_dict
