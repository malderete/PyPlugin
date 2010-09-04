# -*- coding: utf-8 -*-


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

