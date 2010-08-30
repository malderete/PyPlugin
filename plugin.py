#!/usr/bin/python
# -*- coding: utf-8 -*-

# Distributed under license GNU/GPL 3
# Contact: Martin N. Alderete | Email:malderete@gmail.com

# Módulo de Python
import os
import sys
import imp


class PluginLoadError(Exception): pass
class PluginUnloadError(Exception): pass
class PluginDirError(Exception): pass


class PluginManager(object):
	"""
	Main class 
	"""
	def __init__(self, plugin_dirs=None, load=True):
		self.__pluginDir = plugin_dirs or {}
		# Modulos encontrados
		self.__foundModules = []
		# Plugins activos
		self.__pluginActives = {}
		# Plugins inactivos
		self.__pluginInactives = {}
		# Modulos activos
		self.__modulesActives = {}
		# Modulos  Inactivos
		self.__modulesInactives = {}
		#Plugin con Auto-Start
		self.pluginsAutoStart = get_plugins_to_autostart()
		
		if not self.pluginDirExist():
			raise PluginDirError
		
		if load:
			self.__insertPluginsPaths()
			self.__searchPlugins()
			self.__loadPlugins()

	def turnOff(self):
		"""Escribe la configuracion de los plugins
		"""
		#print "Salvando info de plugins"
		set_plugins_to_autostart(QStringList(self.pluginsAutoStart))

	def pluginDirExist(self):
		"""Verifica que exista los directorios de plugins
		e intenta crearlos si es posible
		retorna True o False
		"""
		#Buscamos el archivo ~user/.Opencoffee/plugins/__init__.py
		initFile = os.path.join(self.__pluginDir['user'],  '__init__.py')
		if not os.path.exists(initFile):
			#Buscamos directorio user/.Opencoffee/plugins
			if not os.path.exists(self.__pluginDir['user']):
				#Creamos el directorio
				os.mkdir(self.__pluginDir['user'],  0755)
			try:
				#Creamos __init__.py
				f = open(initFile,  'wb')
				f.close()
			except IOError:
				#No fue posible crear el directorio
				return False
		return True

	def isValidPluginName(self, pluginName):
		"""Verifica que pluginName sea de la forma Plugin<Name>.py
		Retorna True o False
		"""
		return pluginName.startswith("Plugin") and pluginName.endswith(".py")
	
	def __insertPluginsPaths(self):
		"""Agrega los path al path del sistema
		"""
		for key, val in self.__pluginDir.iteritems():
			if not val in sys.path:
				sys.path.append(val)

	def __getPluginFiles(self):
		"""Retorna los nombres de los archivos(plugins)
		Nota: PluginTest.py es considerado como PluginTest
		"""
		user_plugins = [ f[:-3] for f in os.listdir(self.__pluginDir['user']) if self.isValidPluginName(f) ]
		core_plugins = [ f[:-3] for f in os.listdir(self.__pluginDir['core']) if self.isValidPluginName(f) ]
		return user_plugins + core_plugins
	
	def __searchPlugins(self):
		"""Busca posibles plugins
		"""
		self.__foundModules = self.__getPluginFiles()
	
	def __loadPlugins(self):
		"""Carga los plugins
		"""
		for pluginName in self.__foundModules:
			#self.loadPlugin(pluginName,  self.__pluginDir['user'])
			self.loadPlugin(pluginName)

	def loadPlugin(self,  name):
		try:
			try:
				fname = "%s.py" % os.path.join(self.__pluginDir['user'], name)
				module = imp.load_source(name, fname)
			except:
				fname = "%s.py" % os.path.join(self.__pluginDir['core'], name)
				module = imp.load_source(name, fname)
			# agregamos algunos datos...
			module.OCPluginModuleName = name
			module.OCPluginModuleFilename = fname
			# marcamos el modulo como inactivo
			self.__modulesInactives[name] = module
		except PluginLoadError , e:
			print unicode(e)
			raise
	
	def activatePlugins(self):
		"""Activa todos los plugins
		que estan marcados para arrancar
		al inicio
		"""
		#self.pluginsAutoStart = get_plugins_to_autostart()
		for plugin_name in self.pluginsAutoStart:
			self.activatePlugin(unicode(plugin_name))
	
	def activatePlugin(self,  name):
		try:
			try:
				module = self.__modulesInactives[name]
			except KeyError:
				return None

			if not self.canActivatePlugin(module):
				raise PluginLoadError('No fue posible activar el plugin: %s' % name)
			version = getattr(module,  'version')
			className = getattr(module,  'className')
			pluginClass = getattr(module,  className)
			pluginObject = None
			if name in self.__pluginInactives:
				pluginObject = self.__pluginInactives[name]
			else:
				pluginObject = pluginClass(self.__ui)
			try:
				ret = pluginObject.initialize()
				if self.__debug:
					print "Plugin [ %s ] activado" % name
			except TypeError, e:
				print "Error en activatePlugin: [ %s ] error: [ %s ]" % (name, e)
				ret = None
			except Exception, e:
				print "Falla grave: [ %s ] en plugin: %s" % (e,  name)
				return None
			
			pluginObject.OCPluginModule = module
			pluginObject.OCPluginName = className
			pluginObject.OCPluginVersion = version
			
			#Eliminamos el modulo de los inactivos
			self.__modulesInactives.pop(name)
			try:
				#Eliminamos el plugin de los inactivos
				self.__pluginInactives.pop(name)
			except KeyError:
				pass
			#Agregamos la instancia del plugin a los activados
			self.__pluginActives[name] = pluginObject
			#Agregamos el modulo a los activados
			self.__modulesActives[name] = module			
			return ret
		except PluginLoadError, e:
			print unicode(e)
			return None
	
	def canActivatePlugin(self,  module):
		"""Verifica si es posible activar el modulo
		"""
		try:
			if not hasattr(module, "version"):
				raise PluginLoadError('Falta el atributo version')
			if not hasattr(module, "className"):
				raise PluginLoadError('Falta el atributo className')
			className = getattr(module, "className")
			pluginClass = getattr(module, className)
			if not hasattr(pluginClass, "__init__"):
				raise PluginLoadError('Falta el constructor __init__')
			if not hasattr(pluginClass, "initialize"):
				raise PluginLoadError('Falta el atributo initialize')
			if not hasattr(pluginClass, "shutdown"):
				raise PluginLoadError('Falta el atributo shutdown')
			return True
		except PluginLoadError, e:
			print unicode(e)
			return False

	def deactivatePlugin(self,  name):
		try:
			module = self.__modulesActives[name]
		except KeyError:
			return
		
		pluginObject = None
		if self.canDeactivatePlugin(name):
			pluginObject = self.__pluginActives[name]
		
		if pluginObject:
			#apagamos el plugin
			pluginObject.shutdown()
			#Eliminamos el modulo de los activos
			self.__modulesActives.pop(name)
			#Eliminamos el plugin de los activos
			self.__pluginActives.pop(name)
			#Marcamos el plugin como inactivo
			self.__pluginInactives[name] = pluginObject
			#Marcamos el modulo como inactivo
			self.__modulesInactives[name] = module
	
	def canDeactivatePlugin(self,  name):
		object = self.getPluginObject(name)
		return hasattr(object,  'shutdown')

	def isPluginActive(self,  name):
		"""Verifica si el plugin esta activado(cargado)
		"""
		return name in self.__pluginActives
	
	def isPluginLoaded(self,  name):
		"""Verifica si el plugin esta en los 
		plugins conocidos hasta el momento
		"""
		return name in self.__modulesActives.keys() or\
			name in self.__modulesInactives.keys() or\
			name in self.__pluginActives.keys() or\
			name in self.__modulesInactives.keys()

	def getPluginsDetails(self):
		"""Retorna una lista la informacion de los plugins
		"""
		infoList = [self.getPluginDetails(pluginName) for pluginName in self.__foundModules]
		return infoList

	def getPluginDetails(self,  name):
		"""Retorna un diccionario con las claves
		'name', 'description', 'version', 'author',
		'moduleFile', 'status', 'autoStart'
		con la informacion de del plugin
		"""
		if name in self.__modulesActives:
			module = self.__modulesActives[name]
		elif name in self.__modulesInactives:
			module = self.__modulesInactives[name]
		else:
			#Ooops! no debemos llegar aca...
			return None

		details = {}
		details["moduleName"] = name
		details["moduleFileName"] = getattr(module, "OCPluginModuleFilename", "")
		details["pluginName"] = getattr(module, "name", "")
		details["version"] = getattr(module, "version", "")
		details["author"] = getattr(module, "author", "")
		details["description"] = getattr(module, "description", "")
		details['status'] = (name in self.__pluginActives) and "Yes" or "No"
		details['autoStart'] = self.isAutoStart(name) and "Yes" or "No"
		
		return details

	def setPluginAutoStart(self, name,  flag):
		if flag:
			if name not in self.pluginsAutoStart:
				self.pluginsAutoStart.append(name)
		else:
			if name in self.pluginsAutoStart:
				self.pluginsAutoStart.remove(name)

	def isAutoStart(self,  name):
		return name in self.pluginsAutoStart

	def getPluginObject(self,  name):
		"""Retorna la instancia del plugin
		"""
		if name in self.__pluginActives:
			return self.__pluginActives[name]
		if name in self.__pluginInactives:
			return self.activatePlugin(name)



if __name__ ==  '__main__':
	pm = PluginManager(None)
	pm.activatePlugins()
	plugin = pm.getPluginObject('PluginTest')
	print "Obtenemos el plugin para utilizarlo: '%s'" % plugin
	
	
