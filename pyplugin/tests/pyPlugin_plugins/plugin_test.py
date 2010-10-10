from pyplugin import plugin

class plugin_test(plugin.PyBasePlugin):
    def init(self):
        self.connect('hi', self.say_hi)
	self.connect('hi_and_write', self.say_hi_and_write_message)
	self.connect('work', self.add)

    def get_info(self):
	return 'Plugin for test process'

    def say_hi(self, *args, **kwds):
	print 'Reply from a plugin'
	print 'args: %s' % str(args)
	print 'kwds: %s' % kwds
	return True

    def say_hi_and_write_message(self, *args, **kwds):
        self.say_hi(*args, **kwds) 
        self.message_box.write('plugin_test', 'test', data=kwds)
        print 'Messages in message_box: %s' % len(self.message_box)
        return True
	
    def add(self, a, b):
        return a+b        
    
    def work(self):
        return self.service.work()
