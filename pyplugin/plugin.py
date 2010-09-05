'''
plugin.py

Copyright 2010 Martin Alderete

This file is part of pyPlugin, http://github.com/malderete/PyPlugin.

pyPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

pyPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyPlugin; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

<<END_LICENSE>>
'''


class PyBasePlugin(object):
    '''
    Base class for every plugin.
    @author: Martin Alderete ( malderete@gmail.com )
    '''
    def __init__(self, *args, **kwds):
        self.args = args
        self.kwds = kwds

    def init(self, *args, **kwds):
	'''
	Every plugin HAVE to implemente
	this method to initialize.
	'''
        raise NotImplemented

    def get_name(self):
        '''
        Return the plugin name.
        '''
        return self.__class__.__name__

    def finish(self):
        '''
        Utility method for cleanup.
        '''
        pass
    
    def get_dependencies(self):
        '''
        Subclasses MUST re-implement this method.
        '''
        raise NotImplemented

    def get_info(self):	
        '''
        Subclasses MUST re-implement this method.
        '''
        raise NotImplemented
	
    def get_type(self):
        return "plugin"


