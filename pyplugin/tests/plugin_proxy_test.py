# -*- coding: utf-8 -*-

'''
Applicacion
'''
class Service(object):	
    def msg(self, msg):
        return "Mensaje: %s" % (msg)

    def bye(self):
        return "Bye Bye"

'''
Application's Plugin
'''
class Plugin(object):
    def do_work1(self):
        return self.service.bye()

    def do_work2(self, msg):
        return self.service.msg(msg)


'''
Library
'''
class Proxy(object):
    '''
    Proxy class to contain any kind
    of instance. Every instance of this
    class receives a method and redirect
    it to another instance.
    '''
    def __init__(self, instance):
        self.__instance = instance
    
    def __getattr__(self, name):
        def wrapper(*args, **kwds):
            #get the proxy method and call it!
            method = getattr(self.__instance, name)
            return method(*args, **kwds)

        return wrapper


def build_proxy(instance):
    '''
    Proxy factory.
    '''
    return Proxy(instance)


class PluginManager(object):
    def __init__(self, proxy_factory=build_proxy):
        self.build_proxy = proxy_factory
    
    
    def new_plugin(self, service_pack, instance):
        instance.service = self.build_proxy(service_pack)


if __name__ == '__main__':
    s = Service()
    p = Plugin()
    pm = PluginManager(proxy_factory=a)
    pm.new_plugin(s, p)
    print p.__dict__
    print p.do_work1()
    print p.do_work2("Martin Alderete")
	




