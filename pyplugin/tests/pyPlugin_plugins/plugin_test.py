from pyplugin import plugin

class plugin_test(plugin.PyBasePlugin):
    def init(self):
	self.connect('hi', self.say_hi)
	self.connect('work', self.add)
	
    def say_hi(self, *args, **kwds):
	print "Reply from a plugin"
	print "args: %s" % str(args)
	print "kwds: %s" % kwds
	return True
	
    def add(self, a, b):
        return a+b        
    
    def work(self):
        return self.service.work()
