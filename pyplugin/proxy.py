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


def proxy_factory(instance):
    '''
    Generic Proxy factory,
    using this factory you are
    programming with Dependency Injection
    on mind.
    '''	
    return Proxy(instance)


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
        self.__instance = instance
    
    def __getattr__(self, name):
        def wrapper(*args, **kwds):
            #get the proxy method and call it!
            method = getattr(self.__instance, name)
            return method(*args, **kwds)

        return wrapper

    def __repr__(self):
	klass = self.__instance.__class__
        return '<%s@%s in %s>' % (type(self).__name__, klass.__name__,\
				   klass.__module__)

