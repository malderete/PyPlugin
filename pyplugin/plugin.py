# -*- coding: utf-8 -*-

class PyBasePlugin(object):
    def __init__(self, *args, **kwds):
        self.args = args
        self.kwds = kwds

    def init(self, *args, **kwds):
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


class PyPlugin(PyBasePlugin): 
    def get_dependencies(self):
        return ()

    def get_info(self):	
        return "a simple plugin for testing purpose"

