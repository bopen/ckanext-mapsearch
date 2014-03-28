from setuptools import setup, find_packages
import sys, os

version = '0.1.1'

setup(
    name='ckanext-mapsearch',
    version=version,
    description="extension adding mapsearch to ckan-spatial",
    long_description="""\
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='bopen srl',
    author_email='c.woerner@bopen.eu',
    url='http://bopen.eu',
    license='AGPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.mapsearch'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      # -*- Extra requirements: -*-
    ],
    entry_points=\
    """
        [ckan.plugins]
        mapsearch=ckanext.mapsearch.plugin:MapsearchPlugin
    """,
)
