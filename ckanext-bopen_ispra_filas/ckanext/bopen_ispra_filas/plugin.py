import ckan.plugins as plugins
from ckan.plugins import IRoutes
from ckan.plugins import IConfigurer


class BopenIspraFilasPlugin(plugins.SingletonPlugin):
    plugins.implements(IRoutes, inherit=True)
    plugins.implements(IConfigurer, inherit=True)

    ## IConfigurer
    def update_config(self, config):
        # add template directory
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_public_directory(config, 'public') 
        plugins.toolkit.add_resource('fanstatic', 'bopen_js')

    ## IRoutes
    def before_map(self, map):
        controller = 'ckanext.bopen_ispra_filas.controllers:ViewController'
        map.connect('map_viewer', '/viewer', controller=controller, action='show')
        #map.redirect('/', '/dataset')
        return map
