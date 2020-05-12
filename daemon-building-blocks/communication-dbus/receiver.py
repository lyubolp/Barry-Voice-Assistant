#!/usr/bin/python

# dbus example by stylesuxx

import dbus
import dbus.service
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

class Test(dbus.service.Object):
    def __init__(self, bus_name, object_path):
        dbus.service.Object.__init__(self, bus_name, object_path)

    @dbus.service.method(dbus_interface='com.a.Test')
    def hi(self):
        print("Hello")

    @dbus.service.method(dbus_interface='com.a.Test', in_signature='v', out_signature='s')
    def stringify(self, variant):
        return str(variant)

    @dbus.service.method(dbus_interface='com.a.Test',
        in_signature='', out_signature='s', sender_keyword='sender')
    def SayHello(self, sender=None):
        return 'Hello, %s!' % sender

loop = GLib.MainLoop()
bus = dbus.SessionBus()
bus_name = dbus.service.BusName('a.com', bus=bus)
obj = Test(bus_name, '/com/a/Test')
loop.run()
