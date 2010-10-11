import os
from pyplugin.plugin_manager import PyPluginManager
from pyplugin.service import ServiceCollection
from pyplugin.messagebox import MessageBox


signals = {'work': [], 'hi': [], 'hi_and_write': []}

def connect(signal_name, func_to_call):
    global signals
    if signal_name in signals:
        signals[signal_name].append({'method': func_to_call})
    

def emit(signal_name, *args, **kwds):
    global signals
    if signal_name in signals:
        for data in signals[signal_name]:
            method = data['method']
            #Call the method
            print method(*args, **kwds)



if __name__ == '__main__':
    plugin_dirs = (os.path.abspath("pyPlugin_plugins"), )  
    services_to_plugins = ServiceCollection()
    #provide a SERVICE to the plugins
    services_to_plugins.add("connect", connect)
    mb = MessageBox('pyplugin_message_box')
    pm = PyPluginManager(plugin_dirs, services_to_plugins, message_box=mb)
    pm.discover()
    pm.load_all()
    if len(pm):
        print "Listing all the plugins:"
	print "========================"
	for p in pm:
            print "    %s - %s" % (p, pm[p].get_info())
        print "\n"
    answer = True
    print 'Valid usernames to emit signals are: (admin, pyplugin)'
    while answer:
        key = str(raw_input("Username: \n"))
        if key == 'admin':
            print ''
            print 'Inside the plugin'
            print '================='
            emit('hi_and_write', 'Emitted by the app', password='pyplugin')
            print ''
            print 'Again in the App'
            print '================'
            print 'Getting data written by plugin inside the mailbox'
            print 'Get the message recently added: %s' % mb.get('plugin_test')
            answer = False
        elif key == 'pyplugin':
            emit('work', 10, 19)
            answer = False
    
    print "The end..."
