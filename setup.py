#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    


setup(
    # metadata
    name = 'pyplugin',
    version = '0.1',
    maintainer = 'Martin Alderete',
    maintainer_email = 'malderete@gmail.com',
    description = 'It is a small library to get a simple plugin architecture.',
    license = 'GPL v3',
    keywords = ['plugins', 'software pattern', 'library'],
    url = 'http://github.com/malderete/PyPlugin/',
    
    classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        
    ],

    # content
    packages = ['pyplugin', 'pyplugin.tests'],
    long_description=read('README'),
                
    # dependencies
    requires = [
    ],
)
