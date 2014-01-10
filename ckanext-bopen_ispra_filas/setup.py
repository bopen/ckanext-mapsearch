from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-bopen_ispra_filas',
	version=version,
	description="extension to handle bopen's filas-opendata needs",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='bopen srl',
	author_email='c.woerner@bopen.eu',
	url='http://bopen.eu',
	license='AGPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.bopen_ispra_filas'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
	# myplugin=ckanext.bopen_ispra_filas:PluginClass
	""",
)
