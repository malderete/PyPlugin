from pyplugin.plugin_manager import PyPluginManager

dirs_to_scan = ("/home/tincho/",)
services = []
plugin_manager = PyPluginManager(dirs_to_scan, services)
#discover plugins
plugin_manager.discover()
#list the plugins
for plugin_name in plugin_manager:
	print "Plugin: %s" % plugin_name

#ask for a plugin
my_plugin = 'pyplugintest' in plugin_manager
if my_plugin:
	print plugin_manager["pyplugintest"]
	#Get the plugin Info
	print plugin_manager.get_plugin_info("pyplugintest")
	print my_plugin.get_info()
else:
	print "El plugin ( %s ) no fue encontrado." % 'pyplugintest'

if my_plugin:
	print my_plugin.is_active()
	print plugin_manager.is_plugin_active("pyplugintest")
	plugin_manager.connect("pyplugintest",  say_bye, "unload")
	my_plugin.connect(say_bye,  "unload")

#re-discover for new plugins
plugin_manager.discover()

#list the plugins again
for plugin_name in plugin_manager:
	print "Plugin: %s" % plugin_name

