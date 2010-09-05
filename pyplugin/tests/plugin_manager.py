import os
import unittest
from pyplugin.plugin_manager import PyPluginManager
from pyplugin.service import ServiceCollection


#Some simple services to plugin_test.
def dummy_function(a, b, *args, **kwds):pass

class ServiceTest(object):
    def work(self):
	return True


class PyPluginManagerTestCase(unittest.TestCase):
    def setUp(self):
	self.plugin_dirs = (os.path.abspath("pyPlugin_plugins"), )	
	self.services = ServiceCollection()
	self.services.add("connect", dummy_function)
	one_service = ServiceTest()
	self.services.add("service", one_service)

    def test_discover(self):
        pm = PyPluginManager(self.plugin_dirs, self.services)
	self.assertEqual(len(pm), 0)
	pm.discover()
	self.assertEqual(len(pm), 1)

    def test_autodiscover(self):
        pm = PyPluginManager(self.plugin_dirs, self.services, auto_init=True)
        self.assertEqual(len(pm), 1)

    def test_magic_methods(self):
        pm = PyPluginManager(self.plugin_dirs, self.services)
	self.assertEqual('plugin_test' in pm, False)
	self.assertEqual(pm['plugin_test'], None)
        pm.discover()
	self.assertEqual('plugin_test' in pm, True)
	for p in pm:
		self.assertTrue(pm[p])

    def test_call_from_plugin(self):
        pm = PyPluginManager(self.plugin_dirs, self.services, auto_init=True)
        p = pm['plugin_test']
        self.assertTrue(p.work())

    def test_load_one(self):
        pm = PyPluginManager(self.plugin_dirs, self.services, auto_init=True)
	pm.load('plugin_test')
	self.assertEqual(len(pm), 1)
	
        



if __name__ == '__main__':
    unittest.main()
