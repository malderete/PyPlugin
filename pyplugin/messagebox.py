'''
messagebox.py

Copyright 2010 Martin Alderete

This file is part of pyPlugin, http://github.com/malderete/PyPlugin.

pyPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

pyPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyPlugin; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

<<END_LICENSE>>
'''

import random

MESSAGEBOX_NAME = 'messagebox'
MAX = 1 << 31

def generate_name():
    return "%s_%s" % (MESSAGEBOX_NAME, random.randrange(0, MAX))


class MessageBox(object):
    '''
    Data structure useful to load and unload
    stuff, it was designed and inspired in the
    classic messages box IPC method.

    The main idea is store messages from an emitter.
    Each message has an emitter and optional data.
    Example:
         >>> mb = MessageBox()
         >>> mb.write("me", "hello", {"to": "everybody"})

    The example above create a "hello" message emitted by "me"
    with the optional data {"to": "everybody"}.

    To read messages you have to ask for an emitter or an
    emitter plus a message.
    Example:
        >>> mb = MessageBox()
        >>> mb.get("me")
        >>> {"hello": {"to": "everybody"}}
        >>>
        >>> mb.get("me", message="hello")
        >>> {"to": "everybody"}

    Author: Martin Alderete (malderete@gmail.com)
    '''
    def __init__(self, name=None):
        self._name = name and name or generate_name()
	self._data = {}

    def get_name(self):
        return self._name

    def __contains__(self, sender):
        return sender in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __nonzero__(self):
        return True

    def get(self, sender, message=None):
        if sender in self._data:
            if message:
                if message in self._data[sender]:
                    return self._data[sender][message]
            else:
                return self._data[sender]
        return {}

    def write(self, sender, message, data=None):
        if not data:
            data = {}
        if not sender in self._data:
            self._data[sender] = {}
        
        self._data[sender][message] = data

    def delete(self, sender, message=None):
        if sender in self._data:
            if message:
                if message in self._data[sender]:
                    del self._data[sender][message]
            else:
                del self._data[sender]


if __name__ == '__main__':
    print "MessageBox class testing\n"
    mb = Blackboard(name='pyplugin_blackboard')
    print "MessageBox's name: %s" % mb.get_name()
    mb.write('test_plugin', 'hi', data={'name': 'martin', 'last': 'alderete'})
    mb.write('test_plugin', 'bye')
    print "Is there any message from test_plugin?: %s" % ('test_plugin' in b,)
    test_all_msg = mb.get('test_plugin')
    print "All messages from test_plugin: %s" % test_all_msg
    test_msg = mb.get('test_plugin', message='hi')
    print "Hi message from test_plugin: %s" % test_msg

