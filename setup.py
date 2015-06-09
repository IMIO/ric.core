# -*- coding: utf-8 -*-

version = '0.1.dev0'

from setuptools import setup, find_packages

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='ric.core',
      version=version,
      description='Core package for RIC',
      long_description=long_description,
      classifiers=[
          "Environment :: Web Environment",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
      ],
      keywords='',
      author='Affinitic',
      author_email='support@lists.affinitic.be',
      url='https://github.com/affinitic/ric.core',
      license='gpl',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'awesome-slugify',
          'collective.contact.core',
          'collective.contact.membrane',
          'collective.excelexport',
          'imio.helpers',
          'plone.app.dexterity',
          'plone.directives.dexterity',
          'Plone',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': [
              'Products.PloneTestCase',
              'collective.monkeypatcher',
              'mock',
              'plone.app.robotframework',
          ]
      },
      entry_points={},
)
