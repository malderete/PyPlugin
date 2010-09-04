# -*- coding: utf-8 -*-


def factory(module_obj, plugin_name, *args, **kwds):
    '''
    Create a instance from a module object,
    this is the factory used by PyPluginManager.
    
    Rule: Every candidate module should have inside 
    a class with the same name as itself.
    '''
    #now APPLY the factory RULE, this case get 
    #a class with the same name like the module!
    class_name = getattr(module_obj, plugin_name)
    instance = class_name(*args, **kwds)
    return instance

