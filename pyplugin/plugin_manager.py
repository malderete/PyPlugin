'''
plugin_manager.py

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

import os
import sys
import imp

from pyplugin import loader



class PyBasePluginManager(object):
    '''
    Base class (abstract)
    subbclass MUST ovewrite some methods
    to work correctly if not NotImplemented
    will be raised.
    
    @author: Martin Alderete ( malderete@gmail.com )
    '''
    
    def __init__(self, plugin_dirs, services, auto_init=False,
                loader=loader.factory):
        '''
        @param plugin_dirs: list or tuple  with paths to search plugins.
        @param services: ServiceCollection object.
        @param auto_init: boolean to auto load or nor plugins.
        @param loader: callable object who know how to instanciate a plugin.
        '''
        #plugin importer method
        self._instance_loader = loader
        self._services = services
        #discovered plugins by directory
        self._plugins_by_dir = {}
        for dir_name in plugin_dirs:
            self.add_plugin_dir(dir_name)

        #found plugins
        #example: ["logger", "my_plugin"]
        self._found_plugins = []
        #active plugins
        #example: {"logger": LoggerIntance, "my_plugin": MyPluginInstance}
        self._active_plugins = {}
        if auto_init:
            self.discover()

    def get_actives_plugins(self):
        '''
        Return a list the instances
        '''
        return self._active_plugins.values()

    def add_plugin_dir(self, plugin_dir):
        '''
        Add a new directory to search plugins.

        @param plugin_dir: absolute path.
        '''
        if not plugin_dir in self._plugins_by_dir:
            self._plugins_by_dir[plugin_dir] = []
        if not plugin_dir in sys.path:	
            #inser the dir in the sys.path
            sys.path.insert(0, plugin_dir)

    def __getitem__(self, plugin_name):
        '''
        Magic method to get a plugin instance 
        from a given name.
        
        @Note: This method has the logic below.
        Check if the plugin is known,
        if it is active return it,
        otherwise, active it and return it.
        It is exception safe, if the plugin
        is not known return None.

        @param plugin_name: plugin name.

        @return: Plugin instance or None
        
        '''
        if plugin_name in self._found_plugins:
            if not plugin_name in self._active_plugins:
                self.load(plugin_name)
                
            return self._active_plugins[plugin_name]
        return None

    def __contains__(self, plugin_name):
        '''
        Magic method to know whether the 
        PluginManager contains
        a plugin with a given name.

        @param plugin_name: plugin name.

        @return: True or False.
        '''
        return plugin_name in self._found_plugins

    def __iter__(self):
        '''
        Magic method to iterate over all
        the plugin's names.

        @return: iterator.
        '''
        return iter(self._found_plugins)

    def __len__(self):
        '''
        Magic method to know the plugins
        quantity.
        
        @return: length.

        '''
        return len(self._found_plugins)

    def get_plugin_name(self, file_name):
        '''
        Get the plugin's name from a file name.
        
        @param file_name: A file object name.
        
        @return: A plugin name from a file.
        '''
        plugin_file_name, file_ext = os.path.splitext(file_name)
        return plugin_file_name

    def _is_valid_plugin_name(self, plugin_name):
        '''
        Check if the file plugin_name 
        is or not a valid plugin name.

        @Note: Subclass MUST implement it
        to make behavior.
        
        @param plugin_name: A plugin name.
        
        @return: True or False.
        '''
        raise NotImplemented

    def list_plugin(self, dir_name):
        '''
        Crawl a directory and collect plugins.
        
        @Note: This method colaborate with
        is_valid_plugin_name to decide which
        files are valids plugin.
        
        @return: List with plugin names.
        '''
        return [ f[:-3] for f in os.listdir(dir_name) \
                if self._is_valid_plugin_name(f) ]

    def is_plugin_active(self, plugin_name):
        '''
        Check if a plugin is or not active

        @param plugin_name: Plugin name to check.

        @return: True or False
        '''
        return plugin_name in self._active_plugins

    def _import_module(self, plugin_name, path_to_file):
        '''
        Get and instanciate a module from his name.
        This method SHOULD NOT be overwritten.
        
        @param plugin_name: A plugin name (file name).
        @param path_to_file: Absolute path to the plugin.
        
        @return: module object.
        '''
        path_to_file = "%s.py" % os.path.join(path_to_file, plugin_name)
        module_obj = imp.load_source(plugin_name, path_to_file)
        return module_obj

    def discover(self):
        '''
        Search all files in a directory
        and get the valid plugin's names.
        '''
        raise NotImplemented

    def _attach_services(self, plugin_obj):
        '''
        Attach the shared services to a 
        plugin's instance.
        
        @Note: Services are the way to share
        objects and functions between the app
        and the plugins.

        @param plugin_obj: A plugin instance.
        '''
        for name, service in self._services:
                setattr(plugin_obj, name, service)

    def load(self, plugin_name):
        '''
        This method instanciate the plugin
        and add it to active_plugins
        '''
        raise NotImplemented

    def load_all(self):
        '''
        This method instanciate ALL
        the plugins in found_plugins
        '''
        raise NotImplemented

    def unload(self, plugin_name):
        '''
        This method remove the plugin
        from active_plugins and delete
        the instance.
        '''
        raise NotImplemented

    def unload_all(self):
        '''
        This method remove ALL the plugin
        from active_plugins and delete
        the instances.
        '''
        raise NotImplemented



class PyPluginManager(PyBasePluginManager):
    '''
    PyPluginManager implementation
    This is a concrete plugin manager.
    This class should be a good plugin manager
    for almost all the projects.
    If you need subclass you are free to do it.
    
    @author: Martin Alderete ( malderete@gmail.com )
    '''
    def __init__(self, dirs, services, auto_init=False, loader=loader.factory):
        #call parent's __init__
        super(PyPluginManager, self).__init__(dirs, services, auto_init=auto_init,\
                loader=loader)
        
    def discover(self):
        '''
        Search all files in a directory
        and get the valid plugin's names.
        '''
        for dir_name in self._plugins_by_dir:
            for file_name in self.list_plugin(dir_name):
                plugin_name = self.get_plugin_name(file_name)
                if not plugin_name in self._found_plugins:
                    self._found_plugins.append(plugin_name)
                    self._plugins_by_dir[dir_name].append(plugin_name)

    def _is_valid_plugin_name(self, plugin_name):
        return plugin_name.endswith(".py") and plugin_name != "__init__.py"

    def load(self, plugin_name):
        for dir_name, plugin_list in self._plugins_by_dir.iteritems():
            if plugin_name in plugin_list:
                #get the module
                module_obj = self._import_module(plugin_name, dir_name)
                #get the instance
                plugin_obj = self._instance_loader(module_obj, plugin_name)
                #attach the services
                self._attach_services(plugin_obj)
                #call a special method *init* in the plugin!
                plugin_obj.init()
                #set as active
                self._active_plugins[plugin_name] = plugin_obj
                return

    def load_all(self):
        for plugin_name in self._found_plugins:
            self.load(plugin_name)

    def unload(self, plugin_name):	
        for dir_name, plugin_list in self._plugins_by_dir.iteritems():
            if plugin_name in plugin_list:
                #set as inactive
                if plugin_name in self._active_plugins:
                    del self._active_plugins[plugin_name]
                    return

    def unload_all(self):
        for plugin_name in self._found_plugins:
            self.unload(plugin_name)


