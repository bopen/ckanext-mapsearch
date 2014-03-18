========================
CKAN Mapsearch extension
========================

ABOUT
=====

Mapsearch is a CKAN-extension to add an immersive, map-centered search to the *CKAN spatial extension* `(ckanext-spatial) <https://github.com/ckan/ckanext-spatial>`_.

.. image:: https://bitbucket.org/bopen/ckanext-mapsearch/raw/master/ckanext-mapsearch/ckanext/mapsearch/public/mapsearch_shot.png
    :alt: Screenshot
    :align: center


FEATURES
========

Its main distinguishing factor is the scale-awareness of the search-engine.

It let's you see how many results there are on different scales for the same geographic area of interest, by using an extra area field during indexing. see `this <#schema>`_ paragraph below.

INSTALLATION
============
*ckanext-mapsearch* is installed like any ckan extension. However, as it depends on *ckanext-spatial* to be installed, make sure mapsearch comes after ckanext-spatial in the plugin list (see `below <#add-the-plugin>`_).

1. install the extension with pip
---------------------------------
.. code:: bash

    pip install -e  git+https://bitbucket.org/bopen/ckanext-mapsearch.git#egg=ckanext-mapsearch

.. _add-the-plugin:

2. add the extension as a plugin
--------------------------------
add the plugin to the plugins-line in your configuration *.ini* file.

**NB. It must be included with, but after *spatial_query***

.. code:: python

    ckan.plugins = stats text_preview resource_proxy recline_preview spatial_metadata spatial_query harvest csw_harvester ckan_harvester mapsearch

3. configure the extension
--------------------------
- set the initial mapextent

  add a line to your ini-file specifying the initial map extent (i.e. the geographical area shown on pageload)

.. code:: python

      ckanext.mapsearch.initial_map_extent = [[32.3957, -26.0339], [32.8129, -25.7732]] # Maputo, Moçambique

- make sure the spatial extension uses solr-spatial field as the backend.

  **NB.: the search-backend of the spatial extension *must* be set to 'solr-spatial-field', as with simple 'solr' the extension will work poorly and with 'postgis' it will not work at all!**

.. code:: python

    ckanext.spatial.search_backend = solr-spatial-field

.. _schema:

4. prepare the schema for the extension
---------------------------------------

the extension needs an extra field in the solr index, add the following line to the `schema.xml` file in the '<fields>' section.

.. code:: xml

    <fields>
        <!-- ... -->
        <field name="spatial_area" type="float" indexed="true" stored="true" />
    </fields>

5. restart solr
---------------

TESTS
=====

there a few basic selenium webdriver tests in the `tests` folder.
