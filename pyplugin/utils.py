# -*- coding: UTF-8 -*-

class Proxy(object):
	def __init__(self, subject):
		self.__subject = subject
	
	def __getattr__(self, attr_name):
		proxy_method = getattr(self.__subject, attr_name)
		return proxy_method 


class Factory(object):
	def build_proxy(self, instance):
		return Proxy(instance)

class A(object):
	def say(self, msg):
		return "Hello %s" % msg


if __name__ == "__main__":
	obj = Factory().build_proxy(A())
	print obj.say("Martin")
