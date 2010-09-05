'''
ejemplo_services.py

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


from types import FunctionType


'''
Applicacion
'''
class ServiceLayer(object):	
    def msg(self, msg):
        return "Mensaje: %s" % (msg)

    def bye(self):
        return "Bye Bye"


def auth():
    return "Metodo auth"


'''
Plugin
'''
class Plugin(object):
    def do_work1(self):
        return self.auth()

    def do_work2(self, msg):
        return self.service.msg(msg)

    def do_work3(self):
        return self.service.bye()


'''
Library
'''
class Proxy(object):
    def __init__(self, instance):
        self.__instance = instance
    
    def __getattr__(self, name):
        def wrapper(*args, **kwds):
            #get the proxy method and call it!
            method = getattr(self.__instance, name)
            return method(*args, **kwds)

        return wrapper


def build_proxy(instance):
    return Proxy(instance)


class ServiceCollection(object):
    def __init__(self):
        self.services = {}

    def add(self, name, service):
        self.services[name] = service

    def __iter__(self):
        return self.services.iteritems()


class PluginManager(object):
    def __init__(self, service_collection, proxy_factory=build_proxy):
        self.build_proxy = proxy_factory
	self.service_collection = service_collection
 
    def new_plugin(self, instance):
        for name, service in self.service_collection:
            if isinstance(service, FunctionType):
	        setattr(instance, name, service)
            else:
               setattr(instance, name, build_proxy(service))


if __name__ == '__main__':
    sp = ServiceCollection()
    sp.add("auth", auth)
    service = ServiceLayer()
    sp.add("service", service)
    pm = PluginManager(sp)
    p = Plugin()
    pm.new_plugin(p)
    print p.__dict__
    print p.do_work1()
    print p.do_work2("Martin Alderete")
    print p.do_work3()
	




