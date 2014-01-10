import ckan.plugins as plugins
from ckan.lib.base import BaseController

#import logging
#log = logging.getLogger(__name__)

class ViewController(BaseController):

    def show(self):
        return plugins.toolkit.render('blank_search_app.html')
