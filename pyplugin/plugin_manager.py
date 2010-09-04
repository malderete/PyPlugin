# -*- coding: utf-8 -*-

import os
import sys
import imp
from pyplugin import importer



class PyBasePluginManager(object):
    '''
    Base class (abstract)
    subbclass MUST override some methods
    to work correctly if not NotImplemented
    will be raised.
    '''
    
    def __init__(self, plugin_dirs, services, auto_init=False,
                importer=importer.factory):
        '''
        @param plugin_dirs: A list with paths to search plugins.
        @param services: A ServicePack object.
        @param auto_init: A boolean to auto load or nor plugins.
        @param importer: A callable object who know how to instanciate a plugin.
        '''	
        #plugin importer method
        self.importer = importer
        self.services = services
        #discovered plugins by directory
        self.plugins_by_dir = {}
        for dir_name in plugin_dirs:
            self.add_plugin_dir(dir_name)

        #found plugins
        #example: ["logger", "my_plugin"]
        self.found_plugins = []
        #active plugins
        #example: {"logger": LoggerIntance, "my_plugin": MyPluginInstance}
        self.active_plugins = {}

    def get_actives_plugins(self):
        '''
        Return a list the instances
        '''
        return self.active_plugins.values()

    def add_plugin_dir(self, plugin_dir):
        '''
        Add a new directory to search plugins.
        '''
        if not plugin_dir in self.plugins_by_dir:
            self.plugins_by_dir[plugin_dir] = []
        if not plugin_dir in sys.path:	
            #inser the dir in the sys.path
            sys.path.insert(0, plugin_dir)

    def __getitem__(self, plugin_name):
        if plugin_name in self.found_plugins:
            if not plugin_name in self.active_plugins:
                self.load(plugin_name)
                
            return self.active_plugins[plugin_name]
        return None

    def __contains__(self, plugin_name):
        '''
        Return whether the PluginManager contains
        a plugin with a given name.
        '''
        return plugin_name in self.found_plugins

    def __iter__(self):
        '''
        Iterate over the names of all plugins
        '''
        return iter(self.found_plugins)

    def __len__(self):
        '''
        Return the number of plugins
        '''
        return len(self.found_plugins)

    def get_plugin_name(self, file_name):
        '''
        Get the plugin's name from a file name
        '''
        plugin_file_name, file_ext = os.path.splitext(file_name)
        return plugin_file_name

    def is_valid_plugin_name(self, plugin_name):
        '''
        Return True or False depends on
        if the file plugin_name is or not
        a valid plugin name

        @Note: Subclass MUST re-implement this to
        make another checks.
        '''
        raise NotImplemented

    def list_plugin(self, dir_name):
        '''
        Return a list of plugin's files.
        '''
        return [ f[:-3] for f in os.listdir(dir_name) if self.is_valid_plugin_name(f) ]

    def is_plugin_active(self, plugin_name):
        '''
        Check if a plugin is or not active

        @return: True or False
        '''
        return plugin_name in self.active_plugins

    def import_module(self, plugin_name, path_to_file):
        '''
        Get a module from his name.
        This method should not be override.
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

    def attach_services(self, plugin_object):
        '''
        Attach the service pack to an instance.

        @param plugin_object: A plugin instance.
        '''
        for service in self.services:
            setattr(plugin_object, service.get_name(), service.get_func())


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
        the instance
        '''
        raise NotImplemented

    def unload_all(self):
        '''
        This method remove ALL the plugin
                from active_plugins and delete
                the instances
        '''
        raise NotImplemented



class PyPluginManager(PyBasePluginManager):
    '''
    PyPluginManager implementation
    This is a concrete plugin manager
    for almost all the projects is a
    good manager, if it is not you
    should re-implement some methods
    from "PyBasePluginManager":
    
    is_valid_plugin_name(self, plugin_name)
    discover(self)
    load(self, plugin_name)
    load_all(self)
    unload(self, plugin_name)
    unload_all(self)

    see the documentation for further information.
    '''
    def __init__(self, dirs, services, auto_init=False,
            importer=factory):
        #call parent's __init__
        super(PyPluginManager, self).__init__(dirs, services,
                auto_init=auto_init, importer=importer)
        
    def discover(self):
        '''
        Search all files in a directory
        and get the valid plugin's names.
        '''
        for dir_name in self.plugins_by_dir:
            for file_name in self.list_plugin(dir_name):
                plugin_name = self.get_plugin_name(file_name)
                self.found_plugins.append(plugin_name)
                self.plugins_by_dir[dir_name].append(plugin_name)

    def is_valid_plugin_name(self, plugin_name):
        return plugin_name.endswith(".py") and plugin_name != "__init__.py"

    def load(self, plugin_name):
        for dir_name, plugin_list in self.plugins_by_dir.iteritems():
            if plugin_name in plugin_list:
                #get the module
                module_obj = self.import_module(plugin_name, dir_name)
                #get the instance
                plugin_obj = self.importer(module_obj, plugin_name,
                                           self.services)
                #attach the services
                self.attach_services(plugin_obj)
                #call a special method init in the plugin!
                plugin_obj.init()
                #set as active
                self.active_plugins[plugin_name] = plugin_obj
                return

    def load_all(self):
        for plugin_name in self.found_plugins:
            self.load(plugin_name)

    def unload(self, plugin_name):	
        for dir_name, plugin_list in self.plugins_by_dir.iteritems():
            if plugin_name in plugin_list:
                #set as inactive
                if plugin_name in self.active_plugins:
                    del self.active_plugins[plugin_name]
                    return

    def unload_all(self):
        for plugin_name in self.found_plugins:
            self.unload(plugin_name)

class Service(object):
    def __init__(self, name, func,  extra=None):
        self.name = name
        self.func = func
        self.extra = extra

    def get_name(self):
        return self.name

    def get_func(self):
        return self.func
    
    def get_extra(self):
        return self.extra


if __name__ == "__main__":
    def greet():
        print "SALUDANDO DESDE EL PLUGIN"

    dirs = ["/home/tincho/pyPlugin_plugins", "/home/tincho/extra_home"]
    services = [Service('greet', greet)]
    
    pm = PyPluginManager(dirs, services)
    print "Discovering plugins..."
    pm.discover()
    print "Found %s plugins" % len(pm)
    print "Checkin if the 'a' plugin is in: %s" % ('a' in pm)
    print "The found plugins are: "
    for plugin_name in pm:
        print plugin_name

    print "load.."
    pm.load("a")
    print "is ( a ) active: %s" % pm.is_plugin_active("a")

    for p in pm.get_actives_plugins():
        p.greet()

    print pm["a"]
