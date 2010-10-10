'''
loader.py

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

def factory(module_obj, plugin_name, *args, **kwds):
    '''
    Create a instance from a module object,
    this is the factory used by PyBasePluginManager.
    
    Rule: Every candidate module should have inside 
    a class with the same name as itself.

    @param module_obj: module object.
    @param plugin_name: string with a plugin's name.

    @return: Plugins instance.

    @author: Martin Alderete ( malderete@gmail.com )
    '''
    #now APPLY the factory RULE, this case get 
    #a class with the same name like the module!
    class_name = getattr(module_obj, plugin_name)
    instance = class_name(*args, **kwds)
    return instance

