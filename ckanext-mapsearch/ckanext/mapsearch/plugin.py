import ckan.plugins as plugins
from ckan.plugins import IRoutes
from ckan.plugins import IConfigurer
from pylons import config
from ckanext.spatial.lib import validate_bbox
from ckan.plugins import IPackageController


class MapsearchPlugin(plugins.SingletonPlugin):
    plugins.implements(IRoutes, inherit=True)
    plugins.implements(IConfigurer, inherit=True)
    plugins.implements(IPackageController, inherit=True)
    exclude_upper_bound = float(config.get('ckanext.mapsearch.exclude_upper_bound', 0.03))
    display_upper_bound = float(config.get('ckanext.mapsearch.display_upper_bound', 1.1))
    display_lower_bound = float(config.get('ckanext.mapsearch.display_lower_bound', 50))
    exclude_lower_bound = float(config.get('ckanext.mapsearch.exclude_lower_bound', 2500))

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
        return map

    def before_search(self, search_params):
        # TODO: decide if we really want to exclude other backends.
        backend = config.get('ckanext.spatial.search_backend', 666)
        if backend != 'solr':
            raise RuntimeError('{0} is not implemented. '.format(backend) +
                               'This extension needs \'solr\' as the search backend')
        scale = search_params['extras'].get('ext_scale')
        if 'ext_bbox' not in search_params['extras'].keys():
            return search_params
        bbox = validate_bbox(search_params['extras'].get('ext_bbox'))
        area_search = abs(bbox['maxx'] - bbox['minx']) * abs(bbox['maxy'] - bbox['miny'])
        area_string = 'div(%s,mul(sub(maxy,miny),sub(maxx,minx)))' % area_search
        scale_dict = {'too_small': ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                                    # only lower range means '>'
                                '{!frange incl=false l=%f}%s' % (self.exclude_lower_bound,
                                                                 area_string)],
                      'small': ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                                '{!frange incl=true l=%f u=%f}%s' % (self.display_lower_bound,
                                                                     self.exclude_lower_bound,
                                                                     area_string)],
                      'normal': ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                                 '{!frange incl=true l=%f u=%f}%s' % (self.display_upper_bound,
                                                                       self.display_lower_bound,
                                                                       area_string)],
                      'big': ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                              '{!frange incl=true l=%f u=%f}%s' % (self.exclude_upper_bound,
                                                                   self.display_upper_bound,
                                                                   area_string)],
                      'too_big': ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                               # only upper range means '<'
                              '{!frange incl=false u=%f}%s' % (self.exclude_upper_bound,
                                                                area_string)],
                      }
        if scale:
            search_params['fq_list'] = scale_dict[scale]
        else:
            search_params['fq_list'] = scale_dict['normal']
        return search_params
