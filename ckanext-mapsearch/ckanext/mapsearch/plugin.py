import ckan.plugins as plugins
from ckan.plugins import IRoutes
from ckan.plugins import IConfigurer


class MapsearchPlugin(plugins.SingletonPlugin):
    plugins.implements(IRoutes, inherit=True)
    plugins.implements(IConfigurer, inherit=True)

    ## IConfigurer
    def update_config(self, config):
        # add template directory
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_public_directory(config, 'public')
        plugins.toolkit.add_resource('fanstatic', 'mapsearch_js')

    ## IRoutes
    def before_map(self, map):
        controller = 'ckanext.mapsearch.controllers:ViewController'
        map.connect('map_viewer', '/mapsearch', controller=controller, action='show')
        map.connect('map_viewer', '/mapsearch/text_complete', controller=controller, action='text_complete')
        map.connect('map_viewer', '/mapsearch/query_datasets', controller=controller, action='query_datasets')
        #map.redirect('/', '/dataset')
        return map
