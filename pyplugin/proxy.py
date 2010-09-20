'''
proxy.py

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

import types



def proxy_factory(instance):
    '''
    Generic Proxy factory,
    using this factory you are
    programming with Dependency Injection
    on mind.

    @param instance: instance to proxy.
    
    @return: Proxy to instance
    '''
    if isinstance(instance, types.FunctionType):
        return ProxyToFunction(instance)

    return Proxy(instance)


class ProxyToFunction(object):
    '''
    Proxy implementation, to proxy
    functions object.
    
    @author: Martin Alderete ( malderete@gmail.com )
    '''
    def __init__(self, function_to_proxy):
        self._function = function_to_proxy
    
    def __call__(self, *args, **kwds):
        ret = self._function(*args, **kwds)
        return ret
    
    def __repr__(self):
        '''
        This method provides a representation
        of a proxied object
        
        @Note: Usefull for development process.
        '''
        func = self._function
        return '<%s@%s in %s>' % (type(self).__name__, func.__name__,\
                                    func.__module__)


class Proxy(object):
    '''
    Proxy class to contain any kind
    of instances. Every instance of this
    class receives a method and redirects
    the call to another instance.

    @author: Martin Alderete ( malderete@gmail.com )
    '''
    def __init__(self, instance):
        '''
        Proxy constructor.
        @param instance: instance to be proxied.
        '''
        self._instance = instance
    
    def __getattr__(self, name):
        def wrapper(*args, **kwds):
            #get the proxy method and call it!
            method = getattr(self._instance, name)
            return method(*args, **kwds)

        return wrapper

    def __repr__(self):
        '''
        This method provides a representation
        of a proxied object
        
        @Note: Usefull for development process.
        '''
        klass = self._instance.__class__
        return '<%s@%s in %s>' % (type(self).__name__, klass.__name__,\
                                    klass.__module__)

