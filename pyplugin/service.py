'''
service.py

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

from pyplugin import proxy



class ServiceCollection(object):
    '''
    This class hold the "services" that the App
    shares to the plugins, is like a ServiceLayer container.
    This class will not be subclassed.

    @author: Martin Alderete ( malderete@gmail.com )
    '''
    def __init__(self, proxy_factory=proxy.proxy_factory):
        '''
        Class constructor.

        @param proxy_factory: A function to Proxy objects(should not be ovewritten).
        '''
        self.services = {}
        self.proxy_factory = proxy_factory

    def add(self, name, service):
        '''
        Add a service to the collection.
        
        @param name: service name.
        @param service: instance or function to share.
        '''
        service = self.proxy_factory(service)
        self.services[name] = service

    def remove(self, service_name):
        '''
        Remove a service from collection.

        @Note: This method has to be called
        before share the service with any plugin.
        It is exception safe, before delete the service
        chekc if the service is in the collection.
        '''
        if service_name in self.services:
            del self.services[service_name]

    def __iter__(self):
        '''
        Magic method to allow iteration
        over the services.
        '''
        return self.services.iteritems()


