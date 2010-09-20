import os
from pyplugin.plugin_manager import PyPluginManager
from pyplugin.service import ServiceCollection


signals = {'work': [], 'hi': []}

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
    pm = PyPluginManager(plugin_dirs, services_to_plugins)
    pm.discover()
    pm.load_all()
    answer = True
    print 'Valid usernames to emit signals are: (admin, pyplugin)'
    while answer:
        key = str(raw_input("Username: \n"))
        if key == 'admin':
            emit('hi', 'Emitted by the app', password='pyplugin')
            answer = False
        elif key == 'pyplugin':
            emit('work', 10, 19)
            answer = False
    
    print "The end..."
