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
    display_upper_bound = config.get('ckanext.mapsearch.upper_bound', 1.1)
    display_lower_bound = config.get('ckanext.mapsearch.lower_bound', 50)

    ## IConfigurer
    def update_config(self, config):
        # add template directory
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_public_directory(config, 'public')
        plugins.toolkit.add_resource('fanstatic', 'mapsearch_js')

    ## IRoutes
    def before_map(self, map):
        controller = 'ckanext.mapsearch.controllers:ViewController'
        map.connect('map_viewer', '/mapsearch',
                    controller=controller, action='show')
#        map.connect('map_viewer', '/mapsearch/text_complete',
#                    controller=controller, action='text_complete')
        return map

    def before_search(self, search_params):
        # TODO: decide if we really want to exclude other backends.
        backend = config.get('ckanext.spatial.search_backend', 666)
        if backend != 'solr':
            raise RuntimeError('{0} is not implemented. '.format(backend) +
                               'This extension needs \'solr\' as the search backend')
        scale = search_params['extras'].get('ext_scale')
        bbox = validate_bbox(search_params['extras'].get('ext_bbox'))
        area_search = abs(bbox['maxx'] - bbox['minx']) * abs(bbox['maxy'] - bbox['miny'])
        area_string = 'div(%s,mul(sub(maxy,miny),sub(maxx,minx)))' % area_search
        scale_dict = {'smaller' : ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                                    # only lower range means '>'
                                   '{!frange incl=false l=%f}%s' % (self.display_lower_bound,
                                                                    area_string)],
                      'normal' : ['{!frange incl=false l=0 u=1}%s' % search_params['bf'],
                                  '{!frange incl=true l=%f u=%f}%s' % (self.display_upper_bound,
                                                                       self.display_lower_bound,
                                                                       area_string)],
                      'bigger' : ['{!frange incl=true l=0 u=1}%s' % search_params['bf'],
                                    # only upper range means '<'
                                  '{!frange incl=false u=%f}%s' % (self.display_upper_bound,
                                                                   area_string)],
                      }
        if scale:
            search_params['fq_list'] = scale_dict[scale]
        else:
            search_params['fq_list'] = scale_dict['normal']
        print search_params['fq_list']
        return search_params
