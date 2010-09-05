from pyplugin import plugin

class plugin_test(plugin.PyBasePlugin):
    def init(self):
	self.connect("1", self.say_hi, 'martin', "alderete", age=25)
	
    def say_hi(self, *args, **kwds):
	print "Hi from a plugin"
	print "args: %s" % str(args)
	print "kwds: %s" % kwds
	
    def work(self):
        return self.service.work()
