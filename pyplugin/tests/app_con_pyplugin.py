# -*- coding: utf-8 -*-
import os
from pyplugin import plugin_manager

d = {'1':[], '2':[]}

def connect(name, method, *args, **kwds):
	global d
	d[name].append({"f": method, "a": args, "k": kwds} )


def emit(m_type):
	global d
	for callback in d[m_type]:
		f = callback["f"]
		a = callback["a"]
		k = callback["k"]
		return f(*a, **k)




if __name__ == "__main__":
	plugins_dir = os.path.abspath("pyPlugin_plugins")
	dirs = [plugins_dir]
	print dirs
	services = [plugin_manager.Service('connect', connect)]
	pm = plugin_manager.PyPluginManager(dirs, services)
	pm.discover()
	print "There are ( %s ) plugin(s)" % len(pm)
	pm.load_all()
	hecho = False
	while not hecho:
		r = str(raw_input("Enter a command: \n"))
		if r == "hello":
			print "Emiting a signal to all the plugins"
			emit("1")
		elif r == "quit":
			hecho = True





