#!/usr/bin/env python

import dbus
proxy = dbus.SessionBus().get_object('a.com', '/com/a/Test')
i = dbus.Interface(proxy, dbus_interface='com.a.Test')

i.hi()
print(i.stringify(123))
